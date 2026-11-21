"""Fetch 2026 FBS season game results + today's game metadata from the public ESPN API.

No API keys required. Writes:
  data/raw/scoreboards/<date>.json   (raw scoreboard JSON, all dates Aug 28 - Nov 15)
  data/results.csv                   (one row per game: date, teams, scores, venue, records)
  data/raw/today_<eventid>.json      (full summary JSON for the 15 slate games on Nov 21)
  data/slate_games.json              (slate game index: id, time, venue, teams, ESPN odds snapshot)
  data/manifest.jsonl                (url, fetched_at_utc, sha256, bytes for every download)
"""
import hashlib
import json
import os
import sys
import time
import urllib.request
from datetime import date, timedelta

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(BASE, 'data', 'raw')
UA = {'User-Agent': 'dspaid-bnty0706-research/1.0 (bounty research; contact: dspaid on GitHub)'}
SB = 'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard'
SUM = 'https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary'

SLATE = [
    ('UCLA', 'Michigan'), ('Arkansas', 'Texas'), ('Indiana', 'Washington'),
    ('LSU', 'Tennessee'), ('Texas Tech', 'Baylor'), ('Texas A&M', 'Oklahoma'),
    ('Maryland', 'USC'), ('Virginia Tech', 'Miami (FL)'), ('Arizona', 'Kansas State'),
    ('Georgia', 'South Carolina'), ('SMU', 'Notre Dame'), ('Kentucky', 'Missouri'),
    ('Pittsburgh', 'Louisville'), ('Utah', 'TCU'), ('San Diego State', 'Boise State'),
]


def fetch(url, tries=4):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            body = urllib.request.urlopen(req, timeout=40).read()
            return body
        except Exception as e:
            if i == tries - 1:
                raise
            time.sleep(2 * (i + 1))


def log(manifest, url, body):
    manifest.append({
        'url': url,
        'fetched_at_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'sha256': hashlib.sha256(body).hexdigest(),
        'bytes': len(body),
    })


def main():
    os.makedirs(RAW, exist_ok=True)
    os.makedirs(os.path.join(RAW, 'scoreboards'), exist_ok=True)
    manifest = []
    rows = []
    d = date(2026, 8, 28)
    end = date(2026, 11, 15)
    while d <= end:
        ds = d.strftime('%Y%m%d')
        url = f'{SB}?dates={ds}'
        body = fetch(url)
        log(manifest, url, body)
        data = json.loads(body)
        keep = d in (date(2026, 11, 14), date(2026, 8, 29)) or d.weekday() == 5 and d >= date(2026, 11, 7)
        if keep:
            with open(os.path.join(RAW, 'scoreboards', f'{ds}.json'), 'wb') as f:
                f.write(body)
        for ev in data.get('events', []):
            comp = ev['competitions'][0]
            home = away = None
            for c in comp['competitors']:
                rec = {r['name']: r.get('summary') for r in c.get('records', [])}
                t = c['team']
                row = {
                    'event_id': ev['id'], 'date': ev['date'], 'state': comp['status']['type']['completed'],
                    'name': ev.get('name'), 'team_id': t['id'], 'team': t['displayName'],
                    'abbr': t['abbreviation'], 'homeaway': c.get('homeAway'),
                    'score': c.get('score'), 'venue': comp.get('venue', {}).get('fullName'),
                    'city': comp.get('venue', {}).get('address', {}).get('city'),
                    'state_abbr': comp.get('venue', {}).get('address', {}).get('state'),
                    'rec_overall': rec.get('overall'), 'rec_home': rec.get('Home'),
                    'rec_road': rec.get('Road'), 'rec_conf': rec.get('vs. Conf.'),
                }
                if c.get('homeAway') == 'home':
                    home = row
                else:
                    away = row
            if home and away:
                rows.append((home, away))
        d += timedelta(days=1)
        print('fetched', ds, flush=True)

    with open(os.path.join(BASE, 'data', 'results.csv'), 'w', encoding='utf-8') as f:
        cols = list(rows[0][0].keys())
        f.write(','.join(cols) + '\n')
        for pair in rows:
            for side in pair:
                f.write(','.join(str(side[c]).replace(',', ';') if side[c] is not None else '' for c in cols) + '\n')

    # today's slate: match by short names against ESPN home/away
    sb_body = fetch(f'{SB}?dates=20261121')
    log(manifest, f'{SB}?dates=20261121', sb_body)
    with open(os.path.join(RAW, 'scoreboards', '20261121.json'), 'wb') as f:
        f.write(sb_body)
    today = json.loads(sb_body)
    slate_games = []
    for ev in today['events']:
        comp = ev['competitions'][0]
        home = next(c for c in comp['competitors'] if c.get('homeAway') == 'home')
        away = next(c for c in comp['competitors'] if c.get('homeAway') == 'away')
        hn, an = home['team']['displayName'], away['team']['displayName']
        for visitor, host in SLATE:
            host_n = host.replace(' (FL)', '')
            if host_n in hn and visitor in an:
                odds = (comp.get('odds') or [{}])[0]
                slate_games.append({
                    'event_id': ev['id'], 'date_utc': ev['date'], 'name': ev['name'],
                    'away_team': away['team'], 'home_team': home['team'],
                    'venue': comp.get('venue'), 'broadcast': [b['names'] for b in comp.get('broadcasts', [])],
                    'odds_provider': odds.get('provider', {}).get('name'), 'spread_details': odds.get('details'),
                    'over_under': odds.get('overUnder'),
                    'ml_home_close': (odds.get('moneyline', {}).get('home') or {}).get('close', {}).get('odds'),
                    'ml_home_open': (odds.get('moneyline', {}).get('home') or {}).get('open', {}).get('odds'),
                    'ml_away_close': (odds.get('moneyline', {}).get('away') or {}).get('close', {}).get('odds'),
                    'ml_away_open': (odds.get('moneyline', {}).get('away') or {}).get('open', {}).get('odds'),
                })
                surl = f'{SUM}?event={ev["id"]}'
                sb2 = fetch(surl)
                log(manifest, surl, sb2)
                with open(os.path.join(RAW, f'today_{ev["id"]}.json'), 'wb') as f:
                    f.write(sb2)
                break
    assert len(slate_games) == 15, f'matched {len(slate_games)} slate games'
    with open(os.path.join(BASE, 'data', 'slate_games.json'), 'w', encoding='utf-8') as f:
        json.dump(slate_games, f, indent=1)
    with open(os.path.join(BASE, 'data', 'manifest.jsonl'), 'a', encoding='utf-8') as f:
        for m in manifest:
            f.write(json.dumps(m) + '\n')
    print('DONE results rows(pairs):', len(rows), 'slate games:', len(slate_games))


if __name__ == '__main__':
    main()
