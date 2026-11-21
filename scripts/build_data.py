"""Offline analysis layer: computes power ratings, season aggregates, rest/travel/wind,
player availability notes and predicted scores for the 15 slate games.

Reads only files under data/ (all snapshots already downloaded by fetch_*.py), so it
runs on a clean machine with no network access and no API keys.
Writes data/analysis/{ap_poll.json,ratings.csv,team_season.json,games.json}.
"""
import csv
import json
import math
import os
import re
from collections import Counter, defaultdict
from datetime import datetime, timedelta

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ADIR = os.path.join(BASE, 'data', 'analysis')
KICK_DATE = datetime(2026, 11, 21)


def load(name):
    return json.load(open(os.path.join(BASE, 'data', name), encoding='utf-8'))


def et_offset(dt_utc):
    # 2026 US DST ends Nov 1; games run Aug-Dec. EDT=-4 through Oct, EST=-5 from Nov.
    return -4 if dt_utc.month < 11 else -5


def to_et(iso):
    d = datetime.fromisoformat(iso.replace('Z', '+00:00'))
    return d + timedelta(hours=et_offset(d))


def haversine(a, b):
    lat1, lon1 = math.radians(a[0]), math.radians(a[1])
    lat2, lon2 = math.radians(b[0]), math.radians(b[1])
    p = 2 * math.asin(math.sqrt(math.sin((lat2 - lat1) / 2) ** 2 +
                                math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2))
    return round(p * 3958.8)


# keys are the venue spellings used by the ESPN game log; values are exact venues.csv rows
VENUE_ALIAS = {'Memorial Stadium': 'Memorial Stadium (Columbia; MO)',
               'Memorial Stadium (Norman; OK)': 'Memorial Stadium (Norman; OK)',
               'DKR-Texas Memorial Stadium': 'Darrell K Royal-Texas Memorial Stadium',
               'Memorial Stadium (Bloomington; IN)': 'Memorial Stadium (Bloomington; IN)'}


def fix_venue(v):
    return VENUE_ALIAS.get(v, v.replace(';', ','))


def main():
    os.makedirs(ADIR, exist_ok=True)
    rows = list(csv.DictReader(open(os.path.join(BASE, 'data', 'results.csv'), encoding='utf-8')))
    tgames = list(csv.DictReader(open(os.path.join(BASE, 'data', 'team_games.csv'), encoding='utf-8')))
    sl = load('slate_games.json')
    weather = load('weather.json')
    manifest = [json.loads(l) for l in open(os.path.join(BASE, 'data', 'manifest.jsonl'), encoding='utf-8')]
    pull = {}
    for m in manifest:
        pull[m['url']] = max(pull.get(m['url'], ''), m['fetched_at_utc'])
    venues = {}
    for r in csv.DictReader(open(os.path.join(BASE, 'data', 'venues.csv'), encoding='utf-8')):
        venues[r['stadium']] = ((float(r['lat']), float(r['lon'])), r['wiki_page'])

    # ---- games list (completed) with ET dates ----
    by_ev = defaultdict(dict)
    for r in rows:
        if r['state'] == 'True':
            by_ev[r['event_id']][r['homeaway']] = r
    games = []
    for ev, d in by_ev.items():
        if 'home' not in d or 'away' not in d:
            continue
        h, a = d['home'], d['away']
        et = to_et(h['date'])
        games.append({'event': ev, 'et_date': et.date().isoformat(),
                      'h_id': h['team_id'], 'h': h['team'], 'hs': int(h['score']),
                      'a_id': a['team_id'], 'a': a['team'], 'as': int(a['score']),
                      'venue': fix_venue(h['venue'])})
    games.sort(key=lambda g: g['et_date'])

    # ---- Massey-style iterative rating (schedule-adjusted point margin) ----
    team_name = {}
    for g in games:
        team_name[g['h_id']] = g['h']
        team_name[g['a_id']] = g['a']
    margins = [g['hs'] - g['as'] for g in games]
    h_adv = round(sum(margins) / len(margins), 3)
    rating = {t: 0.0 for t in team_name}
    for _ in range(80):
        agg, cnt = defaultdict(float), defaultdict(int)
        for g in games:
            mh = (g['hs'] - g['as']) - h_adv + rating[g['a_id']]
            ma = (g['as'] - g['hs']) + h_adv + rating[g['h_id']]
            agg[g['h_id']] += mh
            cnt[g['h_id']] += 1
            agg[g['a_id']] += ma
            cnt[g['a_id']] += 1
        rating = {t: (agg[t] / cnt[t]) for t in team_name}
    with open(os.path.join(ADIR, 'ratings.csv'), 'w', encoding='utf-8') as f:
        f.write('team_id,team,rating,games,w,l,avg_margin\n')
        recs = defaultdict(lambda: [0, 0])
        for g in games:
            recs[g['h_id']][1 if g['hs'] < g['as'] else 0] += 1
            recs[g['a_id']][1 if g['as'] < g['hs'] else 0] += 1
        for t in sorted(team_name, key=lambda t: -rating[t]):
            w_, l_ = recs[t]
            f.write(f'{t},{team_name[t].replace(",", ";")},{round(rating[t], 2)},{w_ + l_},{w_},{l_}\n')

    # ---- team season aggregates from per-game box scores ----
    ev_rows = defaultdict(dict)
    for r in tgames:
        ev_rows[r['event_id']][r['team_id']] = r
    slate_ids, slate_name = {}, {}
    for g in sl:
        slate_ids[g['home_team']['id']] = g['home_team']['displayName']
        slate_ids[g['away_team']['id']] = g['away_team']['displayName']

    def own_goal_yds(text, abbr):
        m = re.match(r'\s*([A-Z]{2,4})\s+(\d+)', text or '')
        if not m:
            return None
        n = int(m.group(2))
        return n if m.group(1) == abbr else 100 - n

    # ---- drive-level possession / net-punting profile from the shipped per-game drive slices ----
    drives = defaultdict(lambda: {'games': set(), 'starts': [], 'scores': 0, 'punts': 0, 'to': 0, 'nets': []})
    ddir = os.path.join(BASE, 'data', 'raw', 'drive_slices')
    for fn in sorted(os.listdir(ddir)):
        for s in json.load(open(os.path.join(ddir, fn), encoding='utf-8')):
            tid = str((s.get('team') or {}).get('id', ''))
            if tid not in slate_ids:
                continue
            ab = (s.get('team') or {}).get('abbreviation') or ''
            d0 = own_goal_yds((s.get('start') or {}).get('text'), ab)
            d1 = own_goal_yds((s.get('end') or {}).get('text'), ab)
            rec = drives[tid]
            rec['games'].add(fn)
            if d0 is not None:
                rec['starts'].append(d0)
            res = s.get('displayResult') or ''
            if s.get('isScore'):
                rec['scores'] += 1
            if res == 'Punt':
                rec['punts'] += 1
                # shortcut: net = scrimmage spot to return-end spot from the punting team's own goal;
                # touchbacks (end at/behind the opponent goal line) are excluded, upgrade if a play-level
                # punt feed is added.
                if d0 is not None and d1 is not None and d1 < 97:
                    rec['nets'].append(d1 - d0)
            if res in ('Interception', 'Fumble', 'Interception Touchdown'):
                rec['to'] += 1

    season = {}
    for tid in slate_ids:
        drv = drives[tid]
        trows = [r for ev, d in ev_rows.items() if tid in d for r in [d[tid]]]
        opps = [d[[k for k in d if k != tid][0]] for ev, d in ev_rows.items() if tid in d]

        def num(r, k):
            try:
                return float(r.get(k) or 0)
            except ValueError:
                return 0.0
        n = len(trows)
        pts = sum(num(r, 'points') for r in trows)
        pap = sum(num(o, 'points') for o in opps)
        plays = sum(num(r, 'plays_est') for r in trows)
        yards = sum(num(r, 'total_yards') for r in trows)
        yallowed = sum(num(o, 'total_yards') for o in opps)
        patt = sum(num(r, 'pass_att') for r in trows)
        pyds = sum(num(r, 'pass_yards_net') for r in trows)
        ratt = sum(num(r, 'rush_att') for r in trows)
        ryds = sum(num(r, 'rush_yards') for r in trows)
        c3 = sum(num(r, 'third_conv') for r in trows)
        a3 = sum(num(r, 'third_att') for r in trows)
        c4 = sum(num(r, 'fourth_conv') for r in trows)
        a4 = sum(num(r, 'fourth_att') for r in trows)
        tov = sum(num(r, 'turnovers') for r in trows)
        tot = sum(num(o, 'turnovers') for o in opps)
        poss = sum(num(r, 'poss_min') for r in trows)
        ppa_g, opp_ppa_g = [], []
        for ev, d in ev_rows.items():
            if tid not in d:
                continue
            me, op = d[tid], [d[k] for k in d if k != tid][0]
            mp, ap_ = num(me, 'plays_est'), num(op, 'plays_est')
            if mp > 0 and ap_ > 0:
                ppa_g.append(num(me, 'points') / mp)
                opp_ppa_g.append(num(op, 'points') / ap_)
        adj_ppa = (sum(ppa_g) - sum(opp_ppa_g)) / len(ppa_g) if ppa_g else None
        qb_cnt = Counter(r['qb1'] for r in trows if r['qb1'])
        rb_cnt = Counter(r['rb1'] for r in trows if r['rb1'])
        wr_cnt = Counter(r['wr1'] for r in trows if r['wr1'])
        qb1 = qb_cnt.most_common(1)[0][0] if qb_cnt else ''
        # ESPN team game logs name the featured ball-carrier/receiver each week but expose no position
        # yardage, so skill players are identified by how often they appear in that slot.
        rb1 = rb_cnt.most_common(1)[0][0] if rb_cnt else ''
        wr1 = wr_cnt.most_common(1)[0][0] if wr_cnt else ''
        season[tid] = {
            'team': slate_ids[tid], 'games': n, 'ppg': round(pts / n, 1), 'pap_g': round(pap / n, 1),
            'ypg': round(yards / n, 1), 'ya_g': round(yallowed / n, 1),
            'yards_per_play': round(yards / plays, 2) if plays else None,
            'yppa': round(pyds / patt, 1) if patt else None,
            'ypra': round(ryds / ratt, 2) if ratt else None,
            'third_pct': round(c3 / a3 * 100, 1) if a3 else None,
            'fourth_pct': round(c4 / a4 * 100, 1) if a4 else None,
            'to_give': int(tov), 'to_take': int(tot), 'to_margin': int(tot - tov),
            # drive-derived special-teams / field-position profile (see drive_slices note above)
            'slice_games': len(drv['games']),
            'net_punt_drive': round(sum(drv['nets']) / len(drv['nets']), 1) if drv['nets'] else None,
            'punt_pg': round(drv['punts'] / len(drv['games']), 1) if drv['games'] else None,
            'drive_to_pg': round(drv['to'] / len(drv['games']), 1) if drv['games'] else None,
            'scoring_drive_pct': round(100 * drv['scores'] / len(drv['starts']), 1) if drv['starts'] else None,
            'avg_start_own_goal': round(sum(drv['starts']) / len(drv['starts']), 1) if drv['starts'] else None,
            'poss_pg': round(poss / n, 1) if n else None,
            'adj_ppa': round(adj_ppa, 3) if adj_ppa is not None else None,
            'ppa': round(pts / plays, 3) if plays else None,
            'qb1': qb1, 'qb_games': qb_cnt.most_common(1)[0][1] if qb_cnt else 0,
            'rb1': rb1, 'rb_games': rb_cnt.most_common(1)[0][1] if rb_cnt else 0,
            'wr1': wr1, 'wr_games': wr_cnt.most_common(1)[0][1] if wr_cnt else 0,
        }

    # cross-check my PPG against ESPN's published per-game averages in the pregame summaries
    for g in sl:
        s = json.load(open(os.path.join(BASE, 'data', 'raw', f"today_{g['event_id']}.json"), encoding='utf-8'))
        for t in s.get('boxscore', {}).get('teams', []):
            tid = t['team']['id']
            if tid in season:
                pub = next((c['displayValue'] for c in t.get('statistics', [])
                            if c['name'] == 'totalPointsPerGame'), None)
                mine = season[tid]['ppg']
                assert pub is None or abs(float(pub) - mine) < 0.25, \
                    f"PPG mismatch {season[tid]['team']}: mine {mine} vs ESPN {pub}"

    json.dump(season, open(os.path.join(ADIR, 'team_season.json'), 'w', encoding='utf-8'), indent=1)

    # ---- rest / home-road / travel / venue per team ----
    last_game, hw, hl, rw, rl = {}, Counter(), Counter(), Counter(), Counter()
    for g in games:
        for tid in (g['h_id'], g['a_id']):
            last_game[tid] = max(last_game.get(tid, ''), g['et_date'])
        won_h = g['hs'] > g['as']
        hw[g['h_id']] += won_h
        hl[g['h_id']] += not won_h
        rw[g['a_id']] += (not won_h)
        rl[g['a_id']] += won_h
    home_venue = {}
    for r in rows:
        if r['state'] == 'True' and r['homeaway'] == 'home' and r['team_id'] in slate_ids:
            home_venue[r['team_id']] = Counter(home_venue.get(r['team_id'], {}))
            home_venue[r['team_id']][fix_venue(r['venue'])] += 1
    home_venue = {t: max(c, key=c.get) for t, c in home_venue.items()}

    # ---- AP poll Nov 16 from wiki snapshot ----
    html = open(os.path.join(BASE, 'data', 'raw', 'wiki',
                             'wiki_2026_NCAA_Division_I_FBS_football_rankings.html'),
                encoding='utf-8', errors='ignore').read()
    ap_sec = html.split('id="AP_poll"')[1].split('id="Coaches_Poll"')[0]
    hdr = None
    poll = []
    for rrow in re.findall(r'<tr[^>]*>(.*?)</tr>', ap_sec, re.S):
        cells = re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', rrow, re.S)
        txts = [re.sub('<[^>]+>', '', c).strip() for c in cells]
        if hdr is None:
            hit = [i for i, t in enumerate(txts) if 'Week 11' in t]
            if hit:
                hdr = hit[0]
            continue
        rank = txts[0].rstrip('.').strip()
        if not rank.isdigit():
            continue
        m = re.search(r'title="([^"]+)"', cells[hdr])
        team = m.group(1) if m else txts[hdr]
        team = re.sub(r'\s*\(\d+[–-]\d+\).*', '', team).strip()
        if team.startswith('2026 '):  # pages without redirect label
            team = team.replace(' football team', '')
        rec = re.findall(r'\((\d+[–-]\d+)\)', txts[hdr])
        poll.append({'rank': int(rank), 'team': team, 'record': rec[0] if rec else ''})
    assert len(poll) >= 25, f'AP poll parsed {len(poll)} rows'
    json.dump(poll[:25], open(os.path.join(ADIR, 'ap_poll.json'), 'w', encoding='utf-8'), indent=1)

    # ---- injury text mining from team season wiki pages + news feed ----
    TEAM_SLUG = {
        'UCLA Bruins': 'wiki_2026_UCLA_Bruins_football_team.html',
        'Michigan Wolverines': 'wiki_2026_Michigan_Wolverines_football_team.html',
        'Arkansas Razorbacks': 'wiki_2026_Arkansas_Razorbacks_football_team.html',
        'Texas Longhorns': 'wiki_2026_Texas_Longhorns_football_team.html',
        'Indiana Hoosiers': 'wiki_2026_Indiana_Hoosiers_football_team.html',
        'Washington Huskies': 'wiki_2026_Washington_Huskies_football_team.html',
        'LSU Tigers': 'wiki_2026_LSU_Tigers_football_team.html',
        'Tennessee Volunteers': 'wiki_2026_Tennessee_Volunteers_football_team.html',
        'Texas Tech Red Raiders': 'wiki_2026_Texas_Tech_Red_Raiders_football_team.html',
        'Baylor Bears': 'wiki_2026_Baylor_Bears_football_team.html',
        'Texas A&M Aggies': 'wiki_2026_Texas_A_26M_Aggies_football_team.html',
        'Oklahoma Sooners': 'wiki_2026_Oklahoma_Sooners_football_team.html',
        'Maryland Terrapins': 'wiki_2026_Maryland_Terrapins_football_team.html',
        'USC Trojans': 'wiki_2026_USC_Trojans_football_team.html',
        'Virginia Tech Hokies': 'wiki_2026_Virginia_Tech_Hokies_football_team.html',
        'Miami Hurricanes': 'wiki_2026_Miami_Hurricanes_football_team.html',
        'Arizona Wildcats': 'wiki_2026_Arizona_Wildcats_football_team.html',
        'Kansas State Wildcats': 'wiki_2026_Kansas_State_Wildcats_football_team.html',
        'Georgia Bulldogs': 'wiki_2026_Georgia_Bulldogs_football_team.html',
        'South Carolina Gamecocks': 'wiki_2026_South_Carolina_Gamecocks_football_team.html',
        'SMU Mustangs': 'wiki_2026_SMU_Mustangs_football_team.html',
        'Notre Dame Fighting Irish': 'wiki_2026_Notre_Dame_Fighting_Irish_football_team.html',
        'Kentucky Wildcats': 'wiki_2026_Kentucky_Wildcats_football_team.html',
        'Missouri Tigers': 'wiki_2026_Missouri_Tigers_football_team.html',
        'Pittsburgh Panthers': 'wiki_2026_Pittsburgh_Panthers_football_team.html',
        'Louisville Cardinals': 'wiki_2026_Louisville_Cardinals_football_team.html',
        'Utah Utes': 'wiki_2026_Utah_Utes_football_team.html',
        'TCU Horned Frogs': 'wiki_2026_TCU_Horned_Frogs_football_team.html',
        'San Diego State Aztecs': 'wiki_2026_San_Diego_State_Aztecs_football_team.html',
        'Boise State Broncos': 'wiki_2026_Boise_State_Broncos_football_team.html',
    }

    def wiki_injury_flags(team_display, player):
        path = os.path.join(BASE, 'data', 'raw', 'wiki', TEAM_SLUG[team_display])
        html = open(path, encoding='utf-8', errors='ignore').read()
        text = re.sub('<[^>]+>', ' ', html)
        out = []
        for sent in re.split(r'(?<=[.;])\s+', text):
            if player and player.lower().split()[-1] in sent.lower() and re.search(
                    r'injur|out for|sidelined|questionable|doubtful|suspend|will miss|out for the season',
                    sent, re.I):
                out.append(re.sub(r'\s+', ' ', sent.strip())[:280])
        return out[:3]

    injury_news = list(csv.DictReader(open(os.path.join(BASE, 'data', 'injury_news.csv'), encoding='utf-8'))) \
        if os.path.exists(os.path.join(BASE, 'data', 'injury_news.csv')) else []

    # ---- assemble games ----
    wdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    out = []
    for g in sorted(sl, key=lambda x: x['date_utc']):
        hid, aid = g['home_team']['id'], g['away_team']['id']
        et = to_et(g['date_utc'])
        s = json.load(open(os.path.join(BASE, 'data', 'raw', f"today_{g['event_id']}.json"), encoding='utf-8'))
        predictor = s.get('predictor') or {}
        fpi = {'home': predictor.get('homeTeam', {}).get('gameProjection'),
               'away': predictor.get('awayTeam', {}).get('gameProjection')}
        det = g['spread_details'] or ''
        fav_abbr, mline = det.rsplit(' ', 1)[0], float(det.rsplit(' ', 1)[1])
        fav_is_home = fav_abbr == g['home_team']['abbreviation']
        if not fav_is_home and fav_abbr != g['away_team']['abbreviation']:
            raise SystemExit(f"unknown favorite abbr {fav_abbr} in {det}")
        r_h, r_a = rating.get(hid, 0), rating.get(aid, 0)
        model_margin_home = r_h - r_a + h_adv
        market_signed = mline if fav_is_home else -mline
        blended = round((market_signed + model_margin_home) / 2, 1)
        T = float(g['over_under'])
        home_pts = round((T + blended) / 2 * 2) / 2
        away_pts = round((T - blended) / 2 * 2) / 2
        w = weather.get(g['event_id'], {})
        cov, hrly = w.get('covering_period') or {}, w.get('hourly_at_kickoff') or {}
        hs, as_ = season[hid], season[aid]
        home_v = home_venue.get(hid)
        away_v = home_venue.get(aid)
        travel_mi = haversine(venues[away_v][0], venues[home_v][0]) if away_v in venues and home_v in venues else None
        rest_h = (datetime.combine(KICK_DATE, datetime.min.time()) -
                  datetime.fromisoformat(last_game[hid])).days
        rest_a = (datetime.combine(KICK_DATE, datetime.min.time()) -
                  datetime.fromisoformat(last_game[aid])).days
        named = []
        for tid, side in ((hid, 'home'), (aid, 'away')):
            sea = season[tid]
            players = [(sea['qb1'], f"QB1 (most-started QB, {sea['qb_games']} of {sea['games']} tracked team box scores)")]
            for cand, games_, role in ((sea['rb1'], sea['rb_games'], 'backfield'),
                                       (sea['wr1'], sea['wr_games'], 'receiving')):
                if cand and all(cand != nm for nm, _ in players):
                    players.append((cand, f'most-listed {role} name in tracked ESPN team box scores '
                                          f'({games_} games); ESPN game logs expose no position yardage'))
            for p, role in players:
                flags = []
                for a in injury_news:
                    if p and p.split()[-1].lower() in (a.get('headline') or '').lower():
                        flags.append(a['url'])
                wiki_flags = wiki_injury_flags(sea['team'], p)
                flagged = flags + wiki_flags
                named.append({'team': sea['team'], 'side': side, 'name': p,
                              'role': role,
                              'status': ('FLAGGED: ' + flagged[0]) if flagged
                              else 'no absence mention in checked sources (ESPN game-summary news feed, ESPN '
                                   'injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; '
                                   'appears repeatedly in tracked ESPN team box scores this season - projected to play',
                              'flag_urls': (flags + wiki_flags)[:3]})

        def ap_rank(display):
            short = {'Miami (FL) Hurricanes': 'Miami (FL)', 'UCLA Bruins': 'UCLA',
                     'USC Trojans': 'USC', 'San Diego State Aztecs': 'San Diego State'}.get(display, display.split()[0])
            for p in poll:
                if p['team'] == short or p['team'].startswith(short + ' ') or short in (p['team'] + ' '):
                    return p
            return None
        out.append({
            'event_id': g['event_id'], 'matchup': f"{g['away_team']['displayName']} at {g['home_team']['displayName']}",
            'kickoff_et': et.strftime('%Y-%m-%d %H:%M ET') + f" ({wdays[et.weekday()]})",
            'venue': g['venue']['fullName'], 'city': g['venue']['address']['city'],
            'broadcast': ', '.join('/'.join(b) for b in g.get('broadcast', [])),
            'rankings': {'home': ap_rank(g['home_team']['displayName']), 'away': ap_rank(g['away_team']['displayName'])},
            'line': {'provider': g['odds_provider'], 'spread': det, 'margin': abs(mline),
                     'favorite': fav_abbr, 'over_under': T,
                     'ml_home_open': g['ml_home_open'], 'ml_home_close': g['ml_home_close'],
                     'ml_away_open': g['ml_away_open'], 'ml_away_close': g['ml_away_close'],
                     'pulled_at_utc': pull.get('https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261121', '')},
            'ratings': {'dsp_home': round(r_h, 2), 'dsp_away': round(r_a, 2), 'home_adv_league': h_adv,
                        'model_margin_home': round(model_margin_home, 1)},
            'fpi_win_pct': {'home': fpi['home'], 'away': fpi['away']},
            'offense_defense': {'home': hs, 'away': as_},
            'rest_days': {'home': rest_h, 'away': rest_a,
                          'last_game': {'home': last_game[hid], 'away': last_game[aid]}},
            'travel_miles_campus_to_campus': travel_mi,
            'home_record': {'home': f'{hw[hid]}-{hl[hid]}', 'away': f'{rw[aid]}-{rl[aid]}'},
            'wind': {'period': cov.get('shortForecast'), 'wind_speed': cov.get('windSpeed'),
                     'wind_dir': cov.get('windDirection'), 'temp': cov.get('temperature'),
                     'hourly_at_kickoff': (hrly.get('shortForecast', '') + ' | ' + str(hrly.get('windSpeed', '')) + ' ' + str(hrly.get('windDirection', ''))).strip(' |'),
                     'forecast_url': w.get('forecast_url'), 'hourly_url': w.get('hourly_url')},
            'prediction': {'margin_blended_signed_home': blended, 'market_margin_signed_home': market_signed,
                           'model_margin_signed_home': round(model_margin_home, 1),
                           'home_pts': home_pts, 'away_pts': away_pts,
                           'arithmetic': f'({T} + {blended})/2 = {(T + blended) / 2:.1f} (home); ({T} - {blended})/2 = {(T - blended) / 2:.1f} (away); blended = mean(market {market_signed:+.1f}, Massey model {model_margin_home:+.1f})'},
            'named_players': named,
        })
    json.dump(out, open(os.path.join(ADIR, 'games.json'), 'w', encoding='utf-8'), indent=1)
    print('DONE games:', len(out), 'teams rated:', len(rating), 'h_adv:', h_adv)


if __name__ == '__main__':
    main()
