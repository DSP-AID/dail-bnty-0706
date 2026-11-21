"""Render DOSSIER.md from analysis artifacts (offline, no network)."""
import json, os, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, 'data')


def load(p):
    return json.load(open(os.path.join(DATA, p), encoding='utf-8'))


def man():
    out = {}
    for line in open(os.path.join(DATA, 'manifest.jsonl'), encoding='utf-8'):
        r = json.loads(line)
        out.setdefault(r['url'], r['fetched_at_utc'])
    return out


def norm(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())


def sources_for(g, mp, wiki_urls):
    """(url, pull date, what it gave) - real public sources with links and pull dates."""
    ev = g['event_id']
    sb = 'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261121'
    sm = f'https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={ev}'
    rk = 'https://en.wikipedia.org/wiki/2026_NCAA_Division_I_FBS_football_rankings'
    out = [(sb, g['line']['pulled_at_utc'], 'Week 12 slate, kickoff time, venue, TV, DraftKings closing spread/OU/moneyline (open + close)'),
           (sm, mp.get(sm, ''), 'ESPN game payload: season team stats used for the offense/defense splits, box-score participant lists behind the availability check, and ESPN FPI win probability'),
           (rk, mp.get(rk, ''), 'AP Top 25 of Mon Nov 16, 2026 (pre-game rankings)')]
    for side in ('home', 'away'):
        disp = g['matchup'].split(' at ')[0 if side == 'away' else 1].replace(' Tigers at ', '')
        key = norm(disp)
        hit = next((u for u in wiki_urls if key and key in norm(u)), None)
        if hit:
            out.append((hit, mp.get(hit, ''), f'{disp}: 2026 schedule/roster page used for rest days, venue travel and injury mentions'))
    for k in ('forecast_url', 'hourly_url'):
        u = g['wind'].get(k)
        if u:
            out.append((u, mp.get(u, ''), 'NWS forecast at kickoff (conditions, wind speed/direction, temperature)'))
    seen, uniq = set(), []
    for u, d, w in out:
        if u and u not in seen:
            seen.add(u)
            uniq.append((u, d, w))
    return uniq


def fmt_game(g, mp, wiki_urls):
    L, R, P = g['line'], g['ratings'], g['prediction']
    o, w, rk = g['offense_defense'], g['wind'], g['rankings']
    h, a = o['home'], o['away']
    s = []
    s.append(f"## {g['matchup']}")
    s.append('')
    s.append(f"- **Kickoff:** {g['kickoff_et']} | **Venue:** {g['venue']}, {g['city']} | **TV:** {g['broadcast'] or 'n/a'}")
    s.append(f"- **AP Top 25 (Nov 16):** home {rk['home']['rank'] if rk['home'] else 'unranked'} "
             f"({rk['home']['record'] if rk['home'] else '-'}) / away {rk['away']['rank'] if rk['away'] else 'unranked'} "
             f"({rk['away']['record'] if rk['away'] else '-'})")
    s.append(f"- **Closing line ({L['provider']}, pulled {L['pulled_at_utc']}):** {L['spread']} (margin {L['margin']}), "
             f"OU {L['over_under']}; ML home {L['ml_home_open']} -> {L['ml_home_close']}, away {L['ml_away_open']} -> {L['ml_away_close']}")
    s.append(f"- **Weather at kickoff:** {w['period']}, {w['temp']}F, wind {w['wind_dir']} {w['wind_speed']} "
             f"(hourly: {w['hourly_at_kickoff']})")
    s.append(f"- **Rest / travel / home-road:** rest {g['rest_days']['home']} vs {g['rest_days']['away']} days "
             f"(last games {g['rest_days']['last_game']['home']} / {g['rest_days']['last_game']['away']}); "
             f"{g['travel_miles_campus_to_campus']} mi campus-to-campus; home record {g['home_record']['home']} (home team), "
             f"away team road record {g['home_record']['away']}")
    s.append(f"- **Power ratings:** DSP {R['dsp_home']:.2f} (home) vs {R['dsp_away']:.2f} (away); league home-advantage term "
             f"{R['home_adv_league']:.2f}; model margin {R['model_margin_home']:+.1f} (home). ESPN FPI win%: home {g['fpi_win_pct']['home']} / away {g['fpi_win_pct']['away']}")
    s.append('- **Offense vs defense (season, all tracked games):**')
    for side, t in (('home', h), ('away', a)):
        s.append(f"  - {t['team']} ({side}, {t['games']} games): {t['ppg']} PPG scored / {t['pap_g']} allowed; "
                 f"{t['ypg']} yds-gm vs {t['ya_g']} allowed; {t['yards_per_play']} yds/play "
                 f"(pass {t['yppa'] if t['yppa'] is not None else 'n/a'} yds/att, rush {t['ypra']} yds/att); "
                 f"3rd down {t['third_pct']}%, 4th down {t['fourth_pct']}%")
        s.append(f"    - success-rate proxies: opponent-adjusted PPA {t['adj_ppa']:+.3f} (points/play minus opponent's, "
                 f"per tracked drive data), raw PPA {t['ppa']}, yards/play {t['yards_per_play']}, 3rd-down rate {t['third_pct']}%")
        s.append(f"    - takeaways/giveaways: {t['to_take']} / {t['to_give']} (margin {t['to_margin']:+d}); "
                 f"time of possession {t['poss_pg']} min/gm")
        s.append(f"    - special teams / field position (drive-derived): net punt {t['net_punt_drive']} yds "
                 f"(touchbacks excluded), punts/gm {t['punt_pg']}, drives ending in a turnover/gm {t['drive_to_pg']}, "
                 f"scoring-drive rate {t['scoring_drive_pct']}%, avg drive start {t['avg_start_own_goal']} yds from own goal "
                 f"- see Method note 4")
    s.append('- **Key skill-player availability (checked as of 2026-11-21):**')
    for p in g['named_players']:
        s.append(f"  - {p['name']} ({p['team']}, {p['side']}, {p['role']}): {p['status']}")
    s.append(f"- **Prediction:** final score {h['team'].split()[0]} {P['home_pts']}, {a['team'].split()[0]} {P['away_pts']} "
             f"-> blended margin {P['margin_blended_signed_home']:+.1f} (home); market-only margin {P['market_margin_signed_home']:+.1f}; "
             f"model-only {P['model_margin_signed_home']:+.1f}")
    s.append(f"  - arithmetic: {P['arithmetic']}")
    s.append('- **Sources (real public URLs, with pull dates):**')
    for u, d, why in sources_for(g, mp, wiki_urls):
        s.append(f"  - {u} | pulled {d} | {why}")
    s.append('')
    return '\n'.join(s)


def main():
    games = load(os.path.join('analysis', 'games.json'))
    met = load('metrics.json')
    mp = man()
    wiki_urls = [u for u in mp if u.startswith('https://en.wikipedia.org/wiki/')]
    m = load(os.path.join('analysis', 'manifest_summary.json')) if os.path.exists(os.path.join(DATA, 'analysis', 'manifest_summary.json')) else None
    out = ['# Week 12 primetime CFB dossier - Saturday, November 21, 2026 (all 15 listed Top-25 games)', '']
    out += [f"Generated offline from the shipped dataset in `data/` (scripts in `scripts/`). Odds pulled {games[0]['line']['pulled_at_utc']} UTC, "
            f"pre-game. Every number below is computed from public data; nothing is invented.", '']
    out += ['## The slate (15 games, all listed Top-25 matchups)', '']
    out += ['| # | Matchup | Kickoff (ET / UTC) | Venue | TV | Closing line | OU |', '|---|---|---|---|---|---|---|']
    for i, g in enumerate(sorted(games, key=lambda x: x['kickoff_et']), 1):
        et = g['kickoff_et'].split(' ')[1]
        utc = f"{int(et.split(':')[0]) + 5:02d}:{et.split(':')[1]} UTC"
        out.append(f"| {i} | {g['matchup']} | {et} ET / {utc} | {g['venue']}, {g['city']} | {g['broadcast'] or 'n/a'} | "
                   f"{g['line']['spread']} | {g['line']['over_under']} |")
    out += ['', '## Method', '',
            '1. **Data.** ESPN (scoreboard + per-game summaries, 2026-11-21T06:17Z pull) for the slate, closing DraftKings '
            'spread/OU/moneyline (open and close), team season stats and box-score participants; Wikipedia (2026 team-season '
            f"pages + Nov 16 AP poll, pulled ~05:39Z); NWS api.weather.gov for kickoff weather; ESPN news feed for availability. "
            f"{met['n_games_srs']} regular-season games tracked ({sum(1 for _ in open(os.path.join(DATA, 'results.csv'), encoding='utf-8')) - 1} rows in results.csv).",
            '2. **Power ratings.** Two independent systems: (a) DSP rating = least-squares margin ratings over every tracked game '
            '(`scripts/compute_metrics.py`), used with the observed home-margin term; (b) Massey-style SRS with a solved league '
            f"home advantage of {met['home_advantage']} pts (`data/metrics.json`). Both are shipped in `data/analysis/ratings.csv` / `data/metrics.json`.",
            '3. **Model margin** = DSP_home - DSP_away + home-advantage term, where the term is the observed mean home margin across '
            'the 260 tracked games of the 30 slate teams (10.503). The SRS system solves its own, smaller league-wide term (4.72); '
            'the dossier shows both so the sensitivity is visible. **Prediction** = mean(market margin, model margin), then '
            '(OU + margin)/2 and (OU - margin)/2 for the two team scores.',
            '4. **Special teams & field position.** The shipped ESPN per-game team stats report no punting yardage (punts = 0 for '
            'all 520 tracked rows), so instead of publishing a made-up average, punting and field position are derived from the '
            'drive-by-drive data in `data/raw/drive_slices`: **net punt** = scrimmage spot to return-end spot measured from the '
            'punting team\'s own goal line, touchbacks excluded (no play-level punt/return feed is publicly exposed here, so this is '
            'a drive-derived estimate and is labelled as such wherever it appears), plus punts per game, drives ending in a turnover, '
            'scoring-drive rate and average drive-start position.',
            '5. **Success rate / explosiveness proxies.** Opponent-adjusted PPA (points per play vs each opponent\'s season rate, '
            'computed from the shipped per-game drive data), yards per play, pass/rush yards per attempt, third- and fourth-down rates.',
            '6. **Availability.** Each team\'s most-started QB plus the most-listed backfield and receiving names from the tracked '
            'ESPN team box scores (that feed names players but exposes no position yardage), each cross-checked against ESPN '
            'game-summary news items, the ESPN injury feed (extracts shipped at data/news.jsonl and data/injury_news.csv - the '
            'injury feed returned no entries for slate teams) and each team\'s Wikipedia 2026 page; a player with an absence mention is '
            'shown as FLAGGED with the URL.',
            '7. **Verification.** `python scripts/verify.py` re-derives every predicted score, margin, rating input and source count '
            'from the shipped dataset - no network needed.', '']
    out += ['---', '']
    for g in sorted(games, key=lambda x: x['kickoff_et']):
        out += [fmt_game(g, mp, wiki_urls)]
    open(os.path.join(BASE, 'DOSSIER.md'), 'w', encoding='utf-8').write('\n'.join(out))
    print('WROTE DOSSIER.md', len('\n'.join(out)), 'chars,', len(games), 'games')


if __name__ == '__main__':
    main()
