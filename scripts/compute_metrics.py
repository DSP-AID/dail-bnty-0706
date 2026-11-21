"""Compute power ratings (SRS with offense/defense split) and per-team method metrics
from the season's real game data (data/results.csv + data/team_games.csv).

Outputs: data/ratings.json, data/team_metrics.csv. Deterministic, stdlib+numpy only.
"""
import csv
import json
import math
import os
from collections import defaultdict
from datetime import date, datetime

import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KICKOFF = date(2026, 11, 21)


def f(x, d=0.0):
    try:
        return float(str(x).replace('-', '').strip() or d)
    except ValueError:
        return d


def haversine(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2-la1)/2)**2 + math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
    return 3958.8 * 2 * math.asin(math.sqrt(h))


def load_events():
    rows = list(csv.DictReader(open(os.path.join(BASE, 'data', 'results.csv'), encoding='utf-8')))
    ev = {}
    for r in rows:
        if r['state'] != 'True' or not r['score']:
            continue
        e = ev.setdefault(r['event_id'], {'date': r['date'][:10]})
        e[('home_id',) if r['homeaway'] == 'home' else ('away_id',)] = r['team_id']
        e[('home_team',) if r['homeaway'] == 'home' else ('away_team',)] = r['team']
        e[('hs',) if r['homeaway'] == 'home' else ('as',)] = int(r['score'])
        if r['homeaway'] == 'home':
            e['venue'] = r['venue']
    return [v for v in ev.values() if len(v) == 7], rows


def srs(events, teams):
    """margin_home = off_h - def_a - (off_a - def_h) + hfa; mean(off)=mean(def)."""
    idx = {t: i for i, t in enumerate(teams)}
    n = len(teams)
    A, b = [], []
    for e in events:
        h, a = idx[e['home_id']], idx[e['away_id']]
        row = [0.0] * (2*n + 1)
        row[h] -= 1; row[n+a] += 1; row[a] += 1; row[n+h] -= 1; row[2*n] = -1
        A.append(row); b.append(e['hs'] - e['as'])
    crow = [0.0] * (2*n + 1)
    for i in range(n):
        crow[i] = 1.0; crow[n+i] = -1.0
    for _ in range(50):
        A.append(crow[:]); b.append(0.0)
    x, *_ = np.linalg.lstsq(np.array(A), np.array(b), rcond=None)
    out = {}
    for t, i in idx.items():
        out[t] = {'off': round(float(x[i]), 2), 'def': round(float(x[n+i]), 2),
                  'srs': round(float(x[i]-x[n+i]), 2)}
    return out, round(float(x[2*n]), 2)


def main():
    events, rows = load_events()
    team_names = {r['team_id']: r['team'] for r in rows}
    teams = sorted(team_names)
    ratings, hfa = srs(events, teams)

    # season aggregates from box-score-derived team_games.csv
    tg = list(csv.DictReader(open(os.path.join(BASE, 'data', 'team_games.csv'), encoding='utf-8')))
    agg = defaultdict(lambda: defaultdict(float))
    per_event = defaultdict(dict)
    for r in tg:
        t, e = r['team_id'], r['event_id']
        a = agg[t]
        pts = f(r['points'])
        plays = f(r['plays_est']) or (f(r['pass_att']) + f(r['rush_att']))
        vals = {'gp': 1, 'pf': pts, 'pa': 0, 'plays': plays, 'yds': f(r['total_yards']),
                'pyds': f(r['pass_yards_net']), 'ryds': f(r['rush_yards']),
                'fd': f(r['first_downs']), 't3c': f(r['third_conv']), 't3a': f(r['third_att']),
                't4a': f(r['fourth_att']), 'to': f(r['turnovers']),
                'punts': f(r['punts']), 'punt_yds': f(r['punt_yds']), 'punt_tb': f(r['punt_tb']),
                'in20': f(r['punt_in20']), 'poss': f(r['poss_min'])}
        for k, v in vals.items():
            a[k] += v
        per_event[e][t] = {'pts': pts, 'plays': plays, 'to': f(r['turnovers'])}
    # points against + forced takeaways via same-event opponent rows
    for e, d in per_event.items():
        ids = list(d)
        if len(ids) != 2:
            continue
        x, y = ids
        agg[x]['pa'] += d[y]['pts']; agg[x]['plays_def'] += d[y]['plays']
        agg[x]['to_forced'] += d[y]['to']
        agg[y]['pa'] += d[x]['pts']; agg[y]['plays_def'] += d[x]['plays']
        agg[y]['to_forced'] += d[x]['to']

    # rest days + home venue per team
    last_game = {}
    home_venue = defaultdict(lambda: defaultdict(int))
    for e in events:
        d = datetime.strptime(e['date'], '%Y-%m-%d').date()
        for t in (e['home_id'], e['away_id']):
            if d > KICKOFF:
                continue
            last_game[t] = max(last_game.get(t, date(2026, 8, 1)), d)
        home_venue[e['home_id']][e['venue']] += 1

    venues = {}
    for r in csv.DictReader(open(os.path.join(BASE, 'data', 'venues.csv'), encoding='utf-8')):
        venues[r['stadium']] = (float(r['lat']), float(r['lon']))
    team_home = {t: max(v, key=v.get) for t, v in home_venue.items()}

    out_rows, out_json = [], {}
    for t in teams:
        a = agg[t]
        gp = max(a['gp'], 1)
        pp = a['plays'] or 1
        pd = a['plays_def'] or 1
        punts = a['punts'] or 1
        rest = (KICKOFF - last_game.get(t, KICKOFF)).days if t in last_game else None
        hv = team_home.get(t)
        m = ratings[t]
        out_json[team_names[t]] = {
            'espn_id': t, 'srs': m['srs'], 'off_eff_pts_per_game': m['off'],
            'def_eff_pts_per_game': m['def'],
            'gp': int(a['gp']), 'pf': round(a['pf'], 1), 'pa': round(a['pa'], 1),
            'points_per_play': round(a['pf']/pp, 3), 'opp_points_per_play': round(a['pa']/pd, 3),
            'net_pts_per_play': round(a['pf']/pp - a['pa']/pd, 3),
            'yards_per_play': round(a['yds']/pp, 2),
            'pass_ypp': round(a['pyds']/pp, 2),
            'rush_ypp': round(a['ryds']/pp, 2),
            'first_down_rate': round(a['fd']/pp, 3), 'third_down_pct': round(a['t3c']/max(a['t3a'], 1), 3),
            'fourth_att_per_game': round(a['t4a']/gp, 2),
            'to_gave_per_game': round(a['to']/gp, 2), 'to_forced_per_game': round(a['to_forced']/gp, 2),
            'to_margin_per_game': round((a['to_forced']-a['to'])/gp, 2),
            'net_punting': round((a['punt_yds'] - 10*a['punt_tb'])/punts, 2),
            'punt_in20_per_game': round(a['in20']/gp, 2),
            'poss_min_per_game': round(a['poss']/gp, 1),
            'rest_days': rest, 'home_venue': hv,
        }
        out_rows.append(team_names[t])

    with open(os.path.join(BASE, 'data', 'ratings.json'), 'w', encoding='utf-8') as fp:
        json.dump({'model': 'dual-effect SRS (margin = HFA + off_home - def_away - off_away + def_home), '
                   'solved by least squares on all 2026 D-I games in data/results.csv; '
                   'units = points/game above average', 'hfa_points': hfa,
                   'teams': out_json}, fp, indent=1)

    cols = list(next(iter(out_json.values())).keys()) + ['travel_miles']
    w = csv.writer(open(os.path.join(BASE, 'data', 'team_metrics.csv'), 'w', encoding='utf-8'))
    w.writerow(cols)
    for name in sorted(out_json):
        d = out_json[name]
        w.writerow([d.get(c, '') for c in cols[:-1]] + [''])
    print('teams:', len(out_json), 'hfa:', hfa)


if __name__ == '__main__':
    main()
