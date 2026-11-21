"""Rebuild data/slate_games.json from the saved Nov-21 scoreboard snapshot, fetch the one
missing game summary, and append honest manifest rows (mtime-based fetched_at for files
already on disk from the earlier run)."""
import hashlib, json, os, time, urllib.request

BASE = r'C:\workspace\tasks\bnty_0706\src'
RAW = os.path.join(BASE, 'data', 'raw')
UA = {'User-Agent': 'dspaid-bnty0706-research/1.0 (bounty research; contact: dspaid on GitHub)'}
SB_PATH = os.path.join(RAW, 'scoreboards', '20261121.json')
SB_URL = 'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261121'
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
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read()
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(2 * (i + 1))


def mtime_utc(path):
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(os.path.getmtime(path)))


def manifest_row(url, path=None, body=None):
    if body is None:
        body = open(path, 'rb').read()
    return {'url': url,
            'fetched_at_utc': mtime_utc(path) if path else time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            'sha256': hashlib.sha256(body).hexdigest(), 'bytes': len(body)}


def main():
    body = open(SB_PATH, 'rb').read()
    today = json.loads(body)
    slate_games = []
    new_rows = [manifest_row(SB_URL, path=SB_PATH)]
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
                spath = os.path.join(RAW, f'today_{ev["id"]}.json')
                if os.path.exists(spath):
                    new_rows.append(manifest_row(surl, path=spath))
                else:
                    sb2 = fetch(surl)
                    with open(spath, 'wb') as f:
                        f.write(sb2)
                    new_rows.append(manifest_row(surl, body=sb2))
                    print('fetched missing summary', ev['id'])
                break
    assert len(slate_games) == 15, f'matched {len(slate_games)}'
    with open(os.path.join(BASE, 'data', 'slate_games.json'), 'w', encoding='utf-8') as f:
        json.dump(slate_games, f, indent=1)
    with open(os.path.join(BASE, 'data', 'manifest.jsonl'), 'a', encoding='utf-8') as f:
        for r in new_rows:
            f.write(json.dumps(r) + '\n')
    print('slate games:', len(slate_games), 'manifest rows appended:', len(new_rows))


if __name__ == '__main__':
    main()
