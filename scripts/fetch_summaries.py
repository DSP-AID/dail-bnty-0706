"""Fetch per-game team box scores (ESPN summary API) for every 2026 game involving a slate team.

Reads data/results.csv + data/slate_games.json, writes:
  data/team_games.csv   one row per (game, team): yards, plays est, TOs, 3rd/4th down conv,
                        possession time, punting (no/yds/tb/in20), top QB/WR/RB names & lines
  data/raw/summary_samples/<eventid>.json  a handful of raw snapshots for verification
No API keys. Idempotent: skips event ids already present in data/raw/summaries/.
"""
import csv
import hashlib
import json
import os
import time
import urllib.request

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(BASE, 'data', 'raw')
SUMDIR = os.path.join(RAW, 'summaries')
DRDIR = os.path.join(RAW, 'drive_slices')
UA = {'User-Agent': 'dspaid-bnty0706-research/1.0 (bounty research; contact: dspaid on GitHub)'}
SUM = 'https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary'


def fetch(url, tries=4):
    for i in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read()
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(2 * (i + 1))


def team_stats(bx_team):
    out = {}
    for c in bx_team.get('statistics', []):
        out[c['name']] = c.get('displayValue')
    return out


def parse_eff(v):
    if v and '-' in str(v):
        a, b = str(v).split('-')[:2]
        try:
            return int(a), int(b)
        except ValueError:
            pass
    return None, None


def players_cat(stats_list, catname):
    for cat in stats_list:
        if isinstance(cat, dict) and cat.get('name') == catname:
            return cat
    return {}


def athlete_row(cat, ath):
    """ESPN player categories are positional: cat['keys'] lines up with ath['stats'] strings."""
    keys = cat.get('keys') or []
    stats = ath.get('stats') or []
    if stats and isinstance(stats[0], dict):
        return {s['name']: s.get('value') for s in stats}
    out = {}
    for k, v in zip(keys, stats):
        try:
            out[k] = float(v)
        except (TypeError, ValueError):
            out[k] = None
    return out


def cat_totals(cat, keys):
    tot = {k: 0.0 for k in keys}
    for ath in cat.get('athletes', []):
        st = athlete_row(cat, ath)
        for k in keys:
            if isinstance(st.get(k), (int, float)):
                tot[k] += st[k]
    return tot


def top_athlete(cat, yards_key, attempts_key=None):
    best = None
    for ath in cat.get('athletes', []):
        st = athlete_row(cat, ath)
        val = st.get(yards_key)
        if not isinstance(val, (int, float)):
            continue
        if best is None or val > best[1]:
            best = (ath['athlete'].get('displayName'), val,
                    st.get(attempts_key) if attempts_key else None)
    return best


def qb_leader(cat):
    """Starting QB = most pass attempts in that game; also his ESPN adjQBR for that game."""
    best = None
    for ath in cat.get('athletes', []):
        st = athlete_row(cat, ath)
        att = st.get('completions/passingAttempts')
        att = float(str(att).split('/')[1]) if att and '/' in str(att) else 0
        if best is None or att > best[1]:
            best = (ath['athlete'].get('displayName'), att, st.get('adjQBR'))
    return best


def main():
    os.makedirs(SUMDIR, exist_ok=True)
    os.makedirs(DRDIR, exist_ok=True)
    slate_ids = set()
    for g in json.load(open(os.path.join(BASE, 'data', 'slate_games.json'), encoding='utf-8')):
        slate_ids.add(g['away_team']['id'])
        slate_ids.add(g['home_team']['id'])
    events = {}
    with open(os.path.join(BASE, 'data', 'results.csv'), encoding='utf-8') as f:
        for row in csv.DictReader(f):
            if row['team_id'] in slate_ids and row['state'] == 'True':
                events.setdefault(row['event_id'], set()).add(row['team_id'])
    print('unique games to fetch:', len(events))
    manifest_path = os.path.join(BASE, 'data', 'manifest.jsonl')
    rows_out = []
    n = 0
    for eid in sorted(events):
        path = os.path.join(SUMDIR, eid + '.json')
        if os.path.exists(path):
            body = open(path, 'rb').read()
        else:
            url = f'{SUM}?event={eid}'
            body = fetch(url)
            with open(path, 'wb') as f:
                f.write(body)
                n += 1
            with open(manifest_path, 'a', encoding='utf-8') as mf:
                mf.write(json.dumps({'url': f'{SUM}?event={eid}',
                                     'fetched_at_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                                     'sha256': hashlib.sha256(body).hexdigest(), 'bytes': len(body)}) + '\n')
            if n % 25 == 0:
                print('fetched', n, flush=True)
        s = json.loads(body)
        drives = (s.get('drives') or {}).get('previous') or []
        with open(os.path.join(DRDIR, eid + '.json'), 'w', encoding='utf-8') as df:
            json.dump([{k: dr.get(k) for k in ('team', 'start', 'end', 'result', 'displayResult',
                                               'offensivePlays', 'yards', 'isScore')} for dr in drives],
                      df, separators=(',', ':'))
        bx = s.get('boxscore') or {}
        hdr_scores = {c['team']['id']: c.get('score')
                      for c in s.get('header', {}).get('competitions', [{}])[0].get('competitors', [])}
        stat_teams = {t['team']['id']: t for t in bx.get('teams', [])}
        play_teams = {t['team']['id']: t for t in bx.get('players', [])}
        for tid, bt in stat_teams.items():
            st = team_stats(bt)
            c3a, c3t = parse_eff(st.get('thirdDownEff'))
            c4a, c4t = parse_eff(st.get('fourthDownEff'))
            ca, ct = parse_eff(st.get('completionAttempts'))
            try:
                rush = int(st.get('rushingAttempts'))
            except (TypeError, ValueError):
                rush = None
            plays_est = (ct or 0) + (rush or 0)
            pt = st.get('possessionTime', '')
            poss_min = None
            if ':' in str(pt):
                mm, ss = str(pt).split(':')
                try:
                    poss_min = round(int(mm) + int(ss) / 60.0, 1)
                except ValueError:
                    pass
            pk = play_teams.get(tid, {})
            pk_stats = pk.get('statistics', []) if isinstance(pk, dict) else []
            punt = cat_totals(players_cat(pk_stats, 'punting'),
                              ['punts', 'puntYards', 'touchbacks', 'puntsInside20'])
            qb = qb_leader(players_cat(pk_stats, 'passing')) or ('', None, None)
            rb = top_athlete(players_cat(pk_stats, 'rushing'), 'rushingYards', 'rushingAttempts') or ('', None, None)
            if rb[0] == qb[0]:  # QB led rushing; take the next-best ball carrier from the same category
                others = [a for a in (top_athlete_n(players_cat(pk_stats, 'rushing'), 'rushingYards', skip=qb[0]),)]
                rb = others[0] or rb
            wr = top_athlete(players_cat(pk_stats, 'receiving'), 'receivingYards', 'receptions') or ('', None, None)
            rows_out.append({
                'event_id': eid, 'date': s.get('header', {}).get('competitions', [{}])[0].get('date', ''),
                'team_id': tid, 'team': bt['team']['displayName'],
                'points': hdr_scores.get(tid) or bt['team'].get('score'),
                'total_yards': st.get('totalYards'), 'pass_yards_net': st.get('netPassingYards'),
                'rush_yards': st.get('rushingYards'),
                'pass_att': ct, 'comp': ca, 'rush_att': rush, 'plays_est': plays_est,
                'first_downs': st.get('firstDowns'), 'third_conv': c3a, 'third_att': c3t,
                'fourth_conv': c4a, 'fourth_att': c4t,
                'turnovers': st.get('turnovers'), 'int_thrown': st.get('interceptions'),
                'fumbles_lost': st.get('fumblesLost'), 'penalties': st.get('totalPenaltiesYards'),
                'poss_min': poss_min, 'punts': punt_no, 'punt_yds': punt_yds,
                'punt_tb': tb, 'punt_in20': in20,
                'qb1': qb[0], 'qb_pass_yds': qb[1], 'qb_comp_att': qb[2],
                'rb1': rb[0], 'rb_rush_yds': rb[1], 'wr1': wr[0], 'wr_rec_yds': wr[1],
            })
    cols = list(rows_out[0].keys())
    with open(os.path.join(BASE, 'data', 'team_games.csv'), 'w', encoding='utf-8') as f:
        f.write(','.join(cols) + '\n')
        for r in rows_out:
            f.write(','.join(str(r[c]).replace(',', ';') if r[c] is not None else '' for c in cols) + '\n')
    # keep 3 raw samples, drop the rest of raw summaries to control repo size
    keep = {eid + '.json' for eid in sorted(events)[:3]}
    removed = sum(1 for fn in os.listdir(SUMDIR)
                  if fn.endswith('.json') and fn not in keep and not os.remove(os.path.join(SUMDIR, fn)))
    print('DONE new fetches:', n, 'team_game rows:', len(rows_out), 'raw kept:', len(keep),
          'removed:', removed, 'drive slices:', len(events))


if __name__ == '__main__':
    main()
