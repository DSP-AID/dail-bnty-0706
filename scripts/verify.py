"""Offline verification of the shipped dataset and analysis (no network, no API keys).

Re-derives the power ratings and every predicted score from data/results.csv, checks them
against data/analysis/*, checks that each game cites >=5 real public sources with pull dates
that exist in data/manifest.jsonl, and checks the retained raw payloads against their recorded
sha256 digests. Run: python scripts/verify.py
"""
import csv
import hashlib
import json
import os
import sys
from collections import defaultdict

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, 'data')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def load(*p):
    return json.load(open(os.path.join(DATA, *p), encoding='utf-8'))


def rated_games():
    by_ev = defaultdict(dict)
    for r in csv.DictReader(open(os.path.join(DATA, 'results.csv'), encoding='utf-8')):
        if r['state'] == 'True':
            by_ev[r['event_id']][r['homeaway']] = r
    games = []
    for ev, d in by_ev.items():
        if 'home' in d and 'away' in d:
            games.append({'h_id': d['home']['team_id'], 'hs': int(d['home']['score']),
                          'a_id': d['away']['team_id'], 'as': int(d['away']['score'])})
    return games


def ratings_from_results(games):
    """Same Massey-style iteration as build_data.py: mean home margin + 80 rating passes."""
    teams = {t for g in games for t in (g['h_id'], g['a_id'])}
    h_adv = round(sum(g['hs'] - g['as'] for g in games) / len(games), 3)
    rating = {t: 0.0 for t in teams}
    for _ in range(80):
        agg, cnt = defaultdict(float), defaultdict(int)
        for g in games:
            agg[g['h_id']] += (g['hs'] - g['as']) - h_adv + rating[g['a_id']]
            cnt[g['h_id']] += 1
            agg[g['a_id']] += (g['as'] - g['hs']) + h_adv + rating[g['h_id']]
            cnt[g['a_id']] += 1
        rating = {t: agg[t] / cnt[t] for t in teams}
    return rating, h_adv


def main():
    games = load('analysis', 'games.json')
    slate = load('slate_games.json')
    sl = slate if isinstance(slate, list) else slate['games']
    ids = {g['event_id']: (g['home_team']['id'], g['away_team']['id']) for g in sl}
    pulls, digests = {}, defaultdict(set)
    for line in open(os.path.join(DATA, 'manifest.jsonl'), encoding='utf-8'):
        m = json.loads(line)
        pulls[m['url']] = max(pulls.get(m['url'], ''), m['fetched_at_utc'])
        digests[m['url'].split('event=')[-1].split('&')[0]].add(m['sha256'])

    assert len(games) == 15, f'expected 15 games, got {len(games)}'
    assert sorted(games, key=lambda g: g['event_id']) and sorted(
        g['event_id'] for g in games) == sorted(ids), 'game ids != slate'

    # 1. ratings re-derived from raw results, compared to the shipped analysis layer
    rating, h_adv = ratings_from_results(rated_games())
    shipped = {r['team_id']: float(r['rating']) for r in
               csv.DictReader(open(os.path.join(DATA, 'analysis', 'ratings.csv'), encoding='utf-8'))}
    common = [t for t in rating if t in shipped]
    assert len(common) > 200, f'only {len(common)} teams overlap ratings.csv'
    worst = max(abs(rating[t] - shipped[t]) for t in common)
    assert worst < 0.05, f'rating drift up to {worst:.3f}'
    print(f'PASS ratings re-derived from results.csv ({len(common)} teams, max drift {worst:.4f}, home adv {h_adv})')

    # 2. every prediction is arithmetic on the shipped closing line + re-derived model margin
    for g in games:
        hid, aid = ids[g['event_id']]
        model = rating[hid] - rating[aid] + h_adv
        assert abs(model - g['ratings']['model_margin_home']) < 0.51, g['matchup']
        mkt, blend = g['prediction']['market_margin_signed_home'], g['prediction']['margin_blended_signed_home']
        ou = g['line']['over_under']
        assert abs(blend - (mkt + model) / 2) < 0.51, g['matchup']
        assert abs(g['prediction']['home_pts'] - (ou + blend) / 2) < 0.6, g['matchup']
        assert abs(g['prediction']['away_pts'] - (ou - blend) / 2) < 0.6, g['matchup']
        for key in ('wind', 'rest_days', 'travel_miles_campus_to_campus', 'home_record', 'fpi_win_pct'):
            assert g[key], (g['matchup'], key)
        assert len(g['named_players']) >= 4, (g['matchup'], len(g['named_players']))
    print('PASS 15/15 predictions re-derived from closing line + re-derived ratings; '
          'weather/rest/travel/ratings/player fields populated')

    # 3. sources: >=5 per game, all real URLs that appear in the manifest, each with a pull date
    import render_dossier as rd
    mp = pulls
    wiki = [u for u in mp if u.startswith('https://en.wikipedia.org/wiki/')]
    for g in games:
        srcs = rd.sources_for(g, mp, wiki)
        assert len(srcs) >= 5, (g['matchup'], len(srcs))
        for url, when, _why in srcs:
            assert when, (g['matchup'], url, 'no pull date')
            assert url in mp, (g['matchup'], url, 'not in manifest.jsonl')
    print('PASS every game cites >=5 public sources with pull dates, all present in manifest.jsonl')

    # 4. retained raw payloads match the sha256 recorded in the manifest
    checked = 0
    for fn in sorted(os.listdir(os.path.join(DATA, 'raw'))):
        if not fn.startswith('today_'):
            continue
        ev = fn[len('today_'):-len('.json')]
        blob = open(os.path.join(DATA, 'raw', fn), 'rb').read()
        assert hashlib.sha256(blob).hexdigest() in digests.get(ev, set()), f'{fn} sha256 not in manifest'
        checked += 1
    assert checked == 15, f'checked {checked} raw payloads'
    print(f'PASS {checked}/15 retained pre-game ESPN payloads match their recorded sha256')
    print('ALL CHECKS PASSED - reproducible offline from data/ alone')


if __name__ == '__main__':
    main()
