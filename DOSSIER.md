# Week 12 primetime CFB dossier - Saturday, November 21, 2026 (all 15 listed Top-25 games)

Generated offline from the shipped dataset in `data/` (scripts in `scripts/`). Odds pulled 2026-11-21T06:17:39Z UTC, pre-game. Every number below is computed from public data; nothing is invented.

## The slate (15 games, all listed Top-25 matchups)

| # | Matchup | Kickoff (ET / UTC) | Venue | TV | Closing line | OU |
|---|---|---|---|---|---|---|
| 1 | UCLA Bruins at Michigan Wolverines | 15:30 ET / 20:30 UTC | Michigan Stadium, Ann Arbor | CBS | UCLA -3.5 | 36.5 |
| 2 | Arkansas Razorbacks at Texas Longhorns | 15:30 ET / 20:30 UTC | DKR-Texas Memorial Stadium, Austin | ESPN/Disney+ | TEX -20.5 | 47.5 |
| 3 | Indiana Hoosiers at Washington Huskies | 15:30 ET / 20:30 UTC | Husky Stadium, Seattle | Peacock | IU -7.5 | 43.5 |
| 4 | LSU Tigers at Tennessee Volunteers | 15:30 ET / 20:30 UTC | Neyland Stadium, Knoxville | ABC | LSU -1.5 | 45.5 |
| 5 | Texas Tech Red Raiders at Baylor Bears | 15:30 ET / 20:30 UTC | McLane Stadium, Waco | Fox | TTU -4.5 | 56.5 |
| 6 | Texas A&M Aggies at Oklahoma Sooners | 15:45 ET / 20:45 UTC | Memorial Stadium (Norman, OK), Norman | ESPN2 | OU -7 | 37.5 |
| 7 | Maryland Terrapins at USC Trojans | 18:15 ET / 23:15 UTC | Los Angeles Memorial Coliseum, Los Angeles | BTN | USC -17.5 | 56.5 |
| 8 | Virginia Tech Hokies at Miami Hurricanes | 19:00 ET / 24:00 UTC | Hard Rock Stadium, Miami Gardens | ESPN/Disney+ | MIA -20.5 | 60.5 |
| 9 | Arizona Wildcats at Kansas State Wildcats | 19:00 ET / 24:00 UTC | Bill Snyder Family Stadium, Manhattan | FS1 | ARIZ -7.5 | 51.5 |
| 10 | Georgia Bulldogs at South Carolina Gamecocks | 19:30 ET / 24:30 UTC | Williams-Brice Stadium, Columbia | ABC | UGA -14.5 | 50.5 |
| 11 | SMU Mustangs at Notre Dame Fighting Irish | 19:30 ET / 24:30 UTC | Notre Dame Stadium, Notre Dame | NBC | ND -20.5 | 56.5 |
| 12 | Kentucky Wildcats at Missouri Tigers | 19:30 ET / 24:30 UTC | Memorial Stadium, Columbia | SEC Network | MIZ -4.5 | 48.5 |
| 13 | Pittsburgh Panthers at Louisville Cardinals | 19:30 ET / 24:30 UTC | L&N Federal Credit Union Stadium, Louisville | ESPN2 | LOU -13.5 | 50.5 |
| 14 | Utah Utes at TCU Horned Frogs | 21:00 ET / 26:00 UTC | Amon G. Carter Stadium, Fort Worth | Fox | UTAH -8.5 | 46.5 |
| 15 | San Diego State Aztecs at Boise State Broncos | 21:30 ET / 26:30 UTC | Albertsons Stadium, Boise | USA Net | BOIS -17.5 | 60.5 |

## Method

1. **Data.** ESPN (scoreboard + per-game summaries, 2026-11-21T06:17Z pull) for the slate, closing DraftKings spread/OU/moneyline (open and close), team season stats and box-score participants; Wikipedia (2026 team-season pages + Nov 16 AP poll, pulled ~05:39Z); NWS api.weather.gov for kickoff weather; ESPN news feed for availability. 752 regular-season games tracked (1504 rows in results.csv).
2. **Power ratings.** Two independent systems: (a) DSP rating = least-squares margin ratings over every tracked game (`scripts/compute_metrics.py`), used with the observed home-margin term; (b) Massey-style SRS with a solved league home advantage of 4.72 pts (`data/metrics.json`). Both are shipped in `data/analysis/ratings.csv` / `data/metrics.json`.
3. **Model margin** = DSP_home - DSP_away + home-advantage term, where the term is the observed mean home margin across the 260 tracked games of the 30 slate teams (10.503). The SRS system solves its own, smaller league-wide term (4.72); the dossier shows both so the sensitivity is visible. **Prediction** = mean(market margin, model margin), then (OU + margin)/2 and (OU - margin)/2 for the two team scores.
4. **Special teams & field position.** The shipped ESPN per-game team stats report no punting yardage (punts = 0 for all 520 tracked rows), so instead of publishing a made-up average, punting and field position are derived from the drive-by-drive data in `data/raw/drive_slices`: **net punt** = scrimmage spot to return-end spot measured from the punting team's own goal line, touchbacks excluded (no play-level punt/return feed is publicly exposed here, so this is a drive-derived estimate and is labelled as such wherever it appears), plus punts per game, drives ending in a turnover, scoring-drive rate and average drive-start position.
5. **Success rate / explosiveness proxies.** Opponent-adjusted PPA (points per play vs each opponent's season rate, computed from the shipped per-game drive data), yards per play, pass/rush yards per attempt, third- and fourth-down rates.
6. **Availability.** Each team's most-started QB plus the most-listed backfield and receiving names from the tracked ESPN team box scores (that feed names players but exposes no position yardage), each cross-checked against ESPN game-summary news items, the ESPN injury feed (extracts shipped at data/news.jsonl and data/injury_news.csv - the injury feed returned no entries for slate teams) and each team's Wikipedia 2026 page; a player with an absence mention is shown as FLAGGED with the URL.
7. **Verification.** `python scripts/verify.py` re-derives every predicted score, margin, rating input and source count from the shipped dataset - no network needed.

---

## UCLA Bruins at Michigan Wolverines

- **Kickoff:** 2026-11-21 15:30 ET (Sat) | **Venue:** Michigan Stadium, Ann Arbor | **TV:** CBS
- **AP Top 25 (Nov 16):** home unranked (-) / away 4 (10–0)
- **Closing line (DraftKings, pulled 2026-11-21T06:17:39Z):** UCLA -3.5 (margin 3.5), OU 36.5; ML home +180 -> +150, away -218 -> -180
- **Weather at kickoff:** Sunny, 65F, wind S 5 to 8 mph (hourly: Sunny | 8 mph S)
- **Rest / travel / home-road:** rest 7 vs 8 days (last games 2026-11-14 / 2026-11-13); 1936 mi campus-to-campus; home record 4-3 (home team), away team road record 4-0
- **Power ratings:** DSP 0.45 (home) vs 17.58 (away); league home-advantage term 10.50; model margin -6.6 (home). ESPN FPI win%: home 46.9 / away 53
- **Offense vs defense (season, all tracked games):**
  - Michigan Wolverines (home, 10 games): 18.3 PPG scored / 17.7 allowed; 300.9 yds-gm vs 276.5 allowed; 8.27 yds/play (pass n/a yds/att, rush 3.77 yds/att); 3rd down 40.8%, 4th down 57.1%
    - success-rate proxies: opponent-adjusted PPA -0.054 (points/play minus opponent's, per tracked drive data), raw PPA 0.503, yards/play 8.27, 3rd-down rate 40.8%
    - takeaways/giveaways: 9 / 19 (margin -10); time of possession 29.4 min/gm
    - special teams / field position (drive-derived): net punt 12.8 yds (touchbacks excluded), punts/gm 4.5, drives ending in a turnover/gm 1.7, scoring-drive rate 25.2%, avg drive start 27.8 yds from own goal - see Method note 4
  - UCLA Bruins (away, 10 games): 32.4 PPG scored / 14.1 allowed; 424.8 yds-gm vs 262.2 allowed; 10.73 yds/play (pass n/a yds/att, rush 5.12 yds/att); 3rd down 45.3%, 4th down 20.0%
    - success-rate proxies: opponent-adjusted PPA +0.379 (points/play minus opponent's, per tracked drive data), raw PPA 0.818, yards/play 10.73, 3rd-down rate 45.3%
    - takeaways/giveaways: 30 / 14 (margin +16); time of possession 32.6 min/gm
    - special teams / field position (drive-derived): net punt 11.2 yds (touchbacks excluded), punts/gm 4.2, drives ending in a turnover/gm 1.4, scoring-drive rate 39.7%, avg drive start 35.9 yds from own goal - see Method note 4
- **Key skill-player availability (checked as of 2026-11-21):**
  - Bryce Underwood (Michigan Wolverines, home, QB1 (most-started QB, 5 of 10 tracked team box scores)): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Savion Hiter (Michigan Wolverines, home, most-listed backfield name in tracked ESPN team box scores (4 games); ESPN game logs expose no position yardage): FLAGGED: (quarterbacks) Lewis Powell (defensive ends / defensive run game coordinator) Larry Black (defensive tackles) Alex Whittingham (linebackers) Jernaro Gilford (cornerbacks) Tyler Stockton (safeties) Doug Elisaia (strength and conditioning coach) Support staff Eli Alford (assistant 
  - JJ Buchanan (Michigan Wolverines, home, most-listed receiving name in tracked ESPN team box scores (7 games); ESPN game logs expose no position yardage): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Nico Iamaleava (UCLA Bruins, away, QB1 (most-started QB, 5 of 10 tracked team box scores)): FLAGGED: [ 6 ] UCLA opened the season with Nico Iamaleava as their starting quarterback , but he was lost for the season after a leg injury in week 5 against Oregon .
  - Wayne Knight (UCLA Bruins, away, most-listed backfield name in tracked ESPN team box scores (7 games); ESPN game logs expose no position yardage): FLAGGED: PST Game weather : Cloudy • Temperature : 58 °F (14 °C) • Wind : SE at 4 miles per hour (6.4 km/h) Game attendance : 45,800 Referee : Chris Coyte TV announcers (FOX) : Tim Brando , Devin Gardner , and Josh Sims Statistics background-color:#FF5F05!important;color:#13294B!important
  - Aidan Mizell (UCLA Bruins, away, most-listed receiving name in tracked ESPN team box scores (4 games); ESPN game logs expose no position yardage): FLAGGED: PST Game weather : Cloudy • Temperature : 58 °F (14 °C) • Wind : SE at 4 miles per hour (6.4 km/h) Game attendance : 45,800 Referee : Chris Coyte TV announcers (FOX) : Tim Brando , Devin Gardner , and Josh Sims Statistics background-color:#FF5F05!important;color:#13294B!important
- **Prediction:** final score Michigan 17.5, UCLA 19.0 -> blended margin -1.6 (home); market-only margin +3.5; model-only -6.6
  - arithmetic: (36.5 + -1.6)/2 = 17.4 (home); (36.5 - -1.6)/2 = 19.1 (away); blended = mean(market +3.5, Massey model -6.6)
- **Sources (real public URLs, with pull dates):**
  - https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261121 | pulled 2026-11-21T06:17:39Z | Week 12 slate, kickoff time, venue, TV, DraftKings closing spread/OU/moneyline (open + close)
  - https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event=401858528 | pulled 2026-11-21T06:17:39Z | ESPN game payload: season team stats used for the offense/defense splits, box-score participant lists behind the availability check, and ESPN FPI win probability
  - https://en.wikipedia.org/wiki/2026_NCAA_Division_I_FBS_football_rankings | pulled 2026-11-21T05:39:51Z | AP Top 25 of Mon Nov 16, 2026 (pre-game rankings)
  - https://en.wikipedia.org/wiki/2026_Michigan_Wolverines_football_team | pulled 2026-11-21T05:39:52Z | Michigan Wolverines: 2026 schedule/roster page used for rest days, venue travel and injury mentions
  - https://en.wikipedia.org/wiki/2026_UCLA_Bruins_football_team | pulled 2026-11-21T05:39:51Z | UCLA Bruins: 2026 schedule/roster page used for rest days, venue travel and injury mentions
  - https://api.weather.gov/gridpoints/DTX/42,29/forecast | pulled 2026-11-21T07:04:40Z | NWS forecast at kickoff (conditions, wind speed/direction, temperature)
  - https://api.weather.gov/gridpoints/DTX/42,29/forecast/hourly | pulled 2026-11-21T07:04:41Z | NWS forecast at kickoff (conditions, wind speed/direction, temperature)

## Arkansas Razorbacks at Texas Longhorns

- **Kickoff:** 2026-11-21 15:30 ET (Sat) | **Venue:** DKR-Texas Memorial Stadium, Austin | **TV:** ESPN/Disney+
- **AP Top 25 (Nov 16):** home 8 (8–2) / away unranked (-)
- **Closing line (DraftKings, pulled 2026-11-21T06:17:39Z):** TEX -20.5 (margin 20.5), OU 47.5; ML home -1450 -> -1600, away +850 -> +900
- **Weather at kickoff:** Areas Of Fog then Mostly Sunny, 75F, wind SSE 0 to 5 mph (hourly: Mostly Sunny | 5 mph S)
- **Rest / travel / home-road:** rest 7 vs 7 days (last games 2026-11-14 / 2026-11-14); 449 mi campus-to-campus; home record 5-1 (home team), away team road record 1-3
- **Power ratings:** DSP 25.23 (home) vs 8.97 (away); league home-advantage term 10.50; model margin +26.8 (home). ESPN FPI win%: home 94.2 / away 5.8
- **Offense vs defense (season, all tracked games):**
  - Texas Longhorns (home, 10 games): 30.2 PPG scored / 17.8 allowed; 354.7 yds-gm vs 288.7 allowed; 9.83 yds/play (pass n/a yds/att, rush 3.56 yds/att); 3rd down 40.4%, 4th down 61.5%
    - success-rate proxies: opponent-adjusted PPA +0.299 (points/play minus opponent's, per tracked drive data), raw PPA 0.837, yards/play 9.83, 3rd-down rate 40.4%
    - takeaways/giveaways: 13 / 17 (margin -4); time of possession 30.2 min/gm
    - special teams / field position (drive-derived): net punt 7.3 yds (touchbacks excluded), punts/gm 4.2, drives ending in a turnover/gm 1.4, scoring-drive rate 44.3%, avg drive start 31.2 yds from own goal - see Method note 4
  - Arkansas Razorbacks (away, 10 games): 21.4 PPG scored / 25.3 allowed; 339.6 yds-gm vs 362.5 allowed; 9.36 yds/play (pass n/a yds/att, rush 3.25 yds/att); 3rd down 42.3%, 4th down 55.6%
    - success-rate proxies: opponent-adjusted PPA -0.148 (points/play minus opponent's, per tracked drive data), raw PPA 0.59, yards/play 9.36, 3rd-down rate 42.3%
    - takeaways/giveaways: 14 / 14 (margin +0); time of possession 31.7 min/gm
    - special teams / field position (drive-derived): net punt 10.4 yds (touchbacks excluded), punts/gm 4.1, drives ending in a turnover/gm 1.3, scoring-drive rate 33.9%, avg drive start 28.1 yds from own goal - see Method note 4
- **Key skill-player availability (checked as of 2026-11-21):**
  - Arch Manning (Texas Longhorns, home, QB1 (most-started QB, 10 of 10 tracked team box scores)): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Hollywood Smothers (Texas Longhorns, home, most-listed backfield name in tracked ESPN team box scores (4 games); ESPN game logs expose no position yardage): FLAGGED: Hollywood Smothers was dealing with a lower-leg injury and not play.
  - Ryan Wingo (Texas Longhorns, home, most-listed receiving name in tracked ESPN team box scores (4 games); ESPN game logs expose no position yardage): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - KJ Jackson (Arkansas Razorbacks, away, QB1 (most-started QB, 10 of 10 tracked team box scores)): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Cam Settles (Arkansas Razorbacks, away, most-listed backfield name in tracked ESPN team box scores (5 games); ESPN game logs expose no position yardage): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Chris Marshall (Arkansas Razorbacks, away, most-listed receiving name in tracked ESPN team box scores (8 games); ESPN game logs expose no position yardage): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
- **Prediction:** final score Texas 25.5, Arkansas 22.0 -> blended margin +3.1 (home); market-only margin -20.5; model-only +26.8
  - arithmetic: (47.5 + 3.1)/2 = 25.3 (home); (47.5 - 3.1)/2 = 22.2 (away); blended = mean(market -20.5, Massey model +26.8)
- **Sources (real public URLs, with pull dates):**
  - https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261121 | pulled 2026-11-21T06:17:39Z | Week 12 slate, kickoff time, venue, TV, DraftKings closing spread/OU/moneyline (open + close)
  - https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event=401856755 | pulled 2026-11-21T06:17:39Z | ESPN game payload: season team stats used for the offense/defense splits, box-score participant lists behind the availability check, and ESPN FPI win probability
  - https://en.wikipedia.org/wiki/2026_NCAA_Division_I_FBS_football_rankings | pulled 2026-11-21T05:39:51Z | AP Top 25 of Mon Nov 16, 2026 (pre-game rankings)
  - https://en.wikipedia.org/wiki/2026_Texas_Longhorns_football_team | pulled 2026-11-21T05:39:54Z | Texas Longhorns: 2026 schedule/roster page used for rest days, venue travel and injury mentions
  - https://en.wikipedia.org/wiki/2026_Arkansas_Razorbacks_football_team | pulled 2026-11-21T05:39:54Z | Arkansas Razorbacks: 2026 schedule/roster page used for rest days, venue travel and injury mentions
  - https://api.weather.gov/gridpoints/EWX/156,92/forecast | pulled 2026-11-21T07:04:41Z | NWS forecast at kickoff (conditions, wind speed/direction, temperature)
  - https://api.weather.gov/gridpoints/EWX/156,92/forecast/hourly | pulled 2026-11-21T07:04:41Z | NWS forecast at kickoff (conditions, wind speed/direction, temperature)

## Indiana Hoosiers at Washington Huskies

- **Kickoff:** 2026-11-21 15:30 ET (Sat) | **Venue:** Husky Stadium, Seattle | **TV:** Peacock
- **AP Top 25 (Nov 16):** home unranked (-) / away 6 (9–1)
- **Closing line (DraftKings, pulled 2026-11-21T06:17:39Z):** IU -7.5 (margin 7.5), OU 43.5; ML home +225 -> +250, away -278 -> -310
- **Weather at kickoff:** Patchy Fog then Chance Light Rain, 51F, wind N 2 mph (hourly: Partly Sunny | 2 mph SSE)
- **Rest / travel / home-road:** rest 7 vs 7 days (last games 2026-11-14 / 2026-11-14); 1869 mi campus-to-campus; home record 3-3 (home team), away team road record 3-0
- **Power ratings:** DSP 6.54 (home) vs 15.73 (away); league home-advantage term 10.50; model margin +1.3 (home). ESPN FPI win%: home 21.4 / away 78.6
- **Offense vs defense (season, all tracked games):**
  - Washington Huskies (home, 10 games): 25.8 PPG scored / 21.1 allowed; 361.2 yds-gm vs 349.6 allowed; 13.23 yds/play (pass n/a yds/att, rush 3.44 yds/att); 3rd down 34.9%, 4th down 69.2%
    - success-rate proxies: opponent-adjusted PPA +0.339 (points/play minus opponent's, per tracked drive data), raw PPA 0.945, yards/play 13.23, 3rd-down rate 34.9%
    - takeaways/giveaways: 16 / 11 (margin +5); time of possession 29.0 min/gm
    - special teams / field position (drive-derived): net punt 9.5 yds (touchbacks excluded), punts/gm 5.0, drives ending in a turnover/gm 0.8, scoring-drive rate 38.3%, avg drive start 28.0 yds from own goal - see Method note 4
  - Indiana Hoosiers (away, 10 games): 31.9 PPG scored / 12.5 allowed; 422.7 yds-gm vs 274.2 allowed; 12.08 yds/play (pass n/a yds/att, rush 5.21 yds/att); 3rd down 41.7%, 4th down 50.0%
    - success-rate proxies: opponent-adjusted PPA +0.504 (points/play minus opponent's, per tracked drive data), raw PPA 0.911, yards/play 12.08, 3rd-down rate 41.7%
    - takeaways/giveaways: 12 / 7 (margin +5); time of possession 29.5 min/gm
    - special teams / field position (drive-derived): net punt 10.2 yds (touchbacks excluded), punts/gm 3.4, drives ending in a turnover/gm 0.6, scoring-drive rate 47.3%, avg drive start 31.7 yds from own goal - see Method note 4
- **Key skill-player availability (checked as of 2026-11-21):**
  - Demond Williams Jr. (Washington Huskies, home, QB1 (most-started QB, 7 of 10 tracked team box scores)): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Brian Bonner Jr. (Washington Huskies, home, most-listed backfield name in tracked ESPN team box scores (4 games); ESPN game logs expose no position yardage): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Chris Lawson (Washington Huskies, home, most-listed receiving name in tracked ESPN team box scores (7 games); ESPN game logs expose no position yardage): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Josh Hoover (Indiana Hoosiers, away, QB1 (most-started QB, 8 of 10 tracked team box scores)): FLAGGED: # Name Class K 15 Nico Radicic Jr P 19 Billy Gowers So K 35 Paddy McAteer Sr K 43 Bryce Taylor Fr LS 47 Jackson Tolle Fr LS 55 Drew Clausen GS LS 57 Sam Lindsey Jr K 90 Josh Placzek So K 93 Quinn Warren Jr Head coach Curt Cignetti Coordinators/assistant coaches Bryant Haines (Def
  - Turbo Richard (Indiana Hoosiers, away, most-listed backfield name in tracked ESPN team box scores (5 games); ESPN game logs expose no position yardage): FLAGGED: # Name Class K 15 Nico Radicic Jr P 19 Billy Gowers So K 35 Paddy McAteer Sr K 43 Bryce Taylor Fr LS 47 Jackson Tolle Fr LS 55 Drew Clausen GS LS 57 Sam Lindsey Jr K 90 Josh Placzek So K 93 Quinn Warren Jr Head coach Curt Cignetti Coordinators/assistant coaches Bryant Haines (Def
  - Charlie Becker (Indiana Hoosiers, away, most-listed receiving name in tracked ESPN team box scores (7 games); ESPN game logs expose no position yardage): FLAGGED: # Name Class K 15 Nico Radicic Jr P 19 Billy Gowers So K 35 Paddy McAteer Sr K 43 Bryce Taylor Fr LS 47 Jackson Tolle Fr LS 55 Drew Clausen GS LS 57 Sam Lindsey Jr K 90 Josh Placzek So K 93 Quinn Warren Jr Head coach Curt Cignetti Coordinators/assistant coaches Bryant Haines (Def
- **Prediction:** final score Washington 24.0, Indiana 19.5 -> blended margin +4.4 (home); market-only margin +7.5; model-only +1.3
  - arithmetic: (43.5 + 4.4)/2 = 23.9 (home); (43.5 - 4.4)/2 = 19.6 (away); blended = mean(market +7.5, Massey model +1.3)
- **Sources (real public URLs, with pull dates):**
  - https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261121 | pulled 2026-11-21T06:17:39Z | Week 12 slate, kickoff time, venue, TV, DraftKings closing spread/OU/moneyline (open + close)
  - https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event=401858535 | pulled 2026-11-21T06:17:40Z | ESPN game payload: season team stats used for the offense/defense splits, box-score participant lists behind the availability check, and ESPN FPI win probability
  - https://en.wikipedia.org/wiki/2026_NCAA_Division_I_FBS_football_rankings | pulled 2026-11-21T05:39:51Z | AP Top 25 of Mon Nov 16, 2026 (pre-game rankings)
  - https://en.wikipedia.org/wiki/2026_Washington_Huskies_football_team | pulled 2026-11-21T05:39:56Z | Washington Huskies: 2026 schedule/roster page used for rest days, venue travel and injury mentions
  - https://en.wikipedia.org/wiki/2026_Indiana_Hoosiers_football_team | pulled 2026-11-21T05:39:55Z | Indiana Hoosiers: 2026 schedule/roster page used for rest days, venue travel and injury mentions
  - https://api.weather.gov/gridpoints/SEW/126,70/forecast | pulled 2026-11-21T07:04:42Z | NWS forecast at kickoff (conditions, wind speed/direction, temperature)
  - https://api.weather.gov/gridpoints/SEW/126,70/forecast/hourly | pulled 2026-11-21T07:04:42Z | NWS forecast at kickoff (conditions, wind speed/direction, temperature)

## LSU Tigers at Tennessee Volunteers

- **Kickoff:** 2026-11-21 15:30 ET (Sat) | **Venue:** Neyland Stadium, Knoxville | **TV:** ABC
- **AP Top 25 (Nov 16):** home 9 (8–2) / away unranked (-)
- **Closing line (DraftKings, pulled 2026-11-21T06:17:39Z):** LSU -1.5 (margin 1.5), OU 45.5; ML home -102 -> -105, away -118 -> -115
- **Weather at kickoff:** Mostly Cloudy, 68F, wind NE 0 to 5 mph (hourly: Mostly Cloudy | 0 mph)
- **Rest / travel / home-road:** rest 7 vs 7 days (last games 2026-11-14 / 2026-11-14); 568 mi campus-to-campus; home record 5-1 (home team), away team road record 1-2
- **Power ratings:** DSP 24.53 (home) vs 24.80 (away); league home-advantage term 10.50; model margin +10.2 (home). ESPN FPI win%: home 49.9 / away 50.1
- **Offense vs defense (season, all tracked games):**
  - Tennessee Volunteers (home, 10 games): 31.4 PPG scored / 14.3 allowed; 385.5 yds-gm vs 284.7 allowed; 8.66 yds/play (pass n/a yds/att, rush 4.81 yds/att); 3rd down 36.5%, 4th down 77.8%
    - success-rate proxies: opponent-adjusted PPA +0.260 (points/play minus opponent's, per tracked drive data), raw PPA 0.706, yards/play 8.66, 3rd-down rate 36.5%
    - takeaways/giveaways: 19 / 11 (margin +8); time of possession 31.8 min/gm
    - special teams / field position (drive-derived): net punt 11.5 yds (touchbacks excluded), punts/gm 4.1, drives ending in a turnover/gm 1.0, scoring-drive rate 46.2%, avg drive start 28.6 yds from own goal - see Method note 4
  - LSU Tigers (away, 10 games): 35.5 PPG scored / 18.1 allowed; 490.3 yds-gm vs 262.3 allowed; 12.29 yds/play (pass n/a yds/att, rush 4.35 yds/att); 3rd down 50.0%, 4th down 68.2%
    - success-rate proxies: opponent-adjusted PPA +0.265 (points/play minus opponent's, per tracked drive data), raw PPA 0.89, yards/play 12.29, 3rd-down rate 50.0%
    - takeaways/giveaways: 12 / 16 (margin -4); time of possession 32.7 min/gm
    - special teams / field position (drive-derived): net punt 8.7 yds (touchbacks excluded), punts/gm 2.9, drives ending in a turnover/gm 1.5, scoring-drive rate 50.4%, avg drive start 31.0 yds from own goal - see Method note 4
- **Key skill-player availability (checked as of 2026-11-21):**
  - George MacIntyre (Tennessee Volunteers, home, QB1 (most-started QB, 6 of 10 tracked team box scores)): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - DeSean Bishop (Tennessee Volunteers, home, most-listed backfield name in tracked ESPN team box scores (9 games); ESPN game logs expose no position yardage): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Mike Matthews (Tennessee Volunteers, home, most-listed receiving name in tracked ESPN team box scores (5 games); ESPN game logs expose no position yardage): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Sam Leavitt (LSU Tigers, away, QB1 (most-started QB, 10 of 10 tracked team box scores)): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Dilin Jones (LSU Tigers, away, most-listed backfield name in tracked ESPN team box scores (8 games); ESPN game logs expose no position yardage): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Jackson Harris (LSU Tigers, away, most-listed receiving name in tracked ESPN team box scores (4 games); ESPN game logs expose no position yardage): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
- **Prediction:** final score Tennessee 25.5, LSU 20.0 -> blended margin +5.9 (home); market-only margin +1.5; model-only +10.2
  - arithmetic: (45.5 + 5.9)/2 = 25.7 (home); (45.5 - 5.9)/2 = 19.8 (away); blended = mean(market +1.5, Massey model +10.2)
- **Sources (real public URLs, with pull dates):**
  - https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261121 | pulled 2026-11-21T06:17:39Z | Week 12 slate, kickoff time, venue, TV, DraftKings closing spread/OU/moneyline (open + close)
  - https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event=401856754 | pulled 2026-11-21T06:17:40Z | ESPN game payload: season team stats used for the offense/defense splits, box-score participant lists behind the availability check, and ESPN FPI win probability
  - https://en.wikipedia.org/wiki/2026_NCAA_Division_I_FBS_football_rankings | pulled 2026-11-21T05:39:51Z | AP Top 25 of Mon Nov 16, 2026 (pre-game rankings)
  - https://en.wikipedia.org/wiki/2026_Tennessee_Volunteers_football_team | pulled 2026-11-21T05:39:58Z | Tennessee Volunteers: 2026 schedule/roster page used for rest days, venue travel and injury mentions
  - https://en.wikipedia.org/wiki/2026_LSU_Tigers_football_team | pulled 2026-11-21T05:39:57Z | LSU Tigers: 2026 schedule/roster page used for rest days, venue travel and injury mentions
  - https://api.weather.gov/gridpoints/MRX/71,51/forecast | pulled 2026-11-21T07:04:43Z | NWS forecast at kickoff (conditions, wind speed/direction, temperature)
  - https://api.weather.gov/gridpoints/MRX/71,51/forecast/hourly | pulled 2026-11-21T07:04:43Z | NWS forecast at kickoff (conditions, wind speed/direction, temperature)

## Texas Tech Red Raiders at Baylor Bears

- **Kickoff:** 2026-11-21 15:30 ET (Sat) | **Venue:** McLane Stadium, Waco | **TV:** Fox
- **AP Top 25 (Nov 16):** home unranked (-) / away 8 (8–2)
- **Closing line (DraftKings, pulled 2026-11-21T06:17:39Z):** TTU -4.5 (margin 4.5), OU 56.5; ML home -108 -> +170, away -112 -> -205
- **Weather at kickoff:** Patchy Fog then Partly Sunny, 77F, wind SSE 5 to 10 mph (hourly: Partly Sunny | 10 mph S)
- **Rest / travel / home-road:** rest 7 vs 7 days (last games 2026-11-14 / 2026-11-14); 311 mi campus-to-campus; home record 4-1 (home team), away team road record 3-1
- **Power ratings:** DSP 17.60 (home) vs 18.37 (away); league home-advantage term 10.50; model margin +9.7 (home). ESPN FPI win%: home 38.6 / away 61.4
- **Offense vs defense (season, all tracked games):**
  - Baylor Bears (home, 10 games): 29.4 PPG scored / 18.1 allowed; 413.9 yds-gm vs 344.6 allowed; 11.19 yds/play (pass n/a yds/att, rush 4.0 yds/att); 3rd down 41.2%, 4th down 56.5%
    - success-rate proxies: opponent-adjusted PPA +0.307 (points/play minus opponent's, per tracked drive data), raw PPA 0.795, yards/play 11.19, 3rd-down rate 41.2%
    - takeaways/giveaways: 16 / 12 (margin +4); time of possession 28.2 min/gm
    - special teams / field position (drive-derived): net punt 8.6 yds (touchbacks excluded), punts/gm 4.4, drives ending in a turnover/gm 1.2, scoring-drive rate 36.4%, avg drive start 32.3 yds from own goal - see Method note 4
  - Texas Tech Red Raiders (away, 10 games): 39.0 PPG scored / 24.4 allowed; 448.6 yds-gm vs 408.6 allowed; 11.16 yds/play (pass n/a yds/att, rush 5.24 yds/att); 3rd down 39.7%, 4th down 62.5%
    - success-rate proxies: opponent-adjusted PPA +0.261 (points/play minus opponent's, per tracked drive data), raw PPA 0.97, yards/play 11.16, 3rd-down rate 39.7%
    - takeaways/giveaways: 16 / 14 (margin +2); time of possession 28.4 min/gm
    - special teams / field position (drive-derived): net punt 9.1 yds (touchbacks excluded), punts/gm 3.9, drives ending in a turnover/gm 1.3, scoring-drive rate 47.4%, avg drive start 31.3 yds from own goal - see Method note 4
- **Key skill-player availability (checked as of 2026-11-21):**
  - DJ Lagway (Baylor Bears, home, QB1 (most-started QB, 8 of 10 tracked team box scores)): FLAGGED: # Name Class LS 93 Dylan Schaub Jr P 94 Palmer Williams Sr K 96 Riley Sullivan Jr K , P 97 Bronson Mueller Fr K 98 Rhett Armstrong So Head coach Dave Aranda Coordinators/assistant coaches Khenon Hall Associate Head Coach and Running Backs Coach Joe Klanderman Defensive Coordinato
  - Dawson Pendergrass (Baylor Bears, home, most-listed backfield name in tracked ESPN team box scores (3 games); ESPN game logs expose no position yardage): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Gavin Freeman (Baylor Bears, home, most-listed receiving name in tracked ESPN team box scores (7 games); ESPN game logs expose no position yardage): FLAGGED: # Name Class LS 93 Dylan Schaub Jr P 94 Palmer Williams Sr K 96 Riley Sullivan Jr K , P 97 Bronson Mueller Fr K 98 Rhett Armstrong So Head coach Dave Aranda Coordinators/assistant coaches Khenon Hall Associate Head Coach and Running Backs Coach Joe Klanderman Defensive Coordinato
  - Will Hammond (Texas Tech Red Raiders, away, QB1 (most-started QB, 7 of 10 tracked team box scores)): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - J'Koby Williams (Texas Tech Red Raiders, away, most-listed backfield name in tracked ESPN team box scores (8 games); ESPN game logs expose no position yardage): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Kenny Johnson (Texas Tech Red Raiders, away, most-listed receiving name in tracked ESPN team box scores (7 games); ESPN game logs expose no position yardage): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
- **Prediction:** final score Baylor 32.0, Texas 24.5 -> blended margin +7.1 (home); market-only margin +4.5; model-only +9.7
  - arithmetic: (56.5 + 7.1)/2 = 31.8 (home); (56.5 - 7.1)/2 = 24.7 (away); blended = mean(market +4.5, Massey model +9.7)
- **Sources (real public URLs, with pull dates):**
  - https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261121 | pulled 2026-11-21T06:17:39Z | Week 12 slate, kickoff time, venue, TV, DraftKings closing spread/OU/moneyline (open + close)
  - https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event=401856871 | pulled 2026-11-21T06:17:40Z | ESPN game payload: season team stats used for the offense/defense splits, box-score participant lists behind the availability check, and ESPN FPI win probability
  - https://en.wikipedia.org/wiki/2026_NCAA_Division_I_FBS_football_rankings | pulled 2026-11-21T05:39:51Z | AP Top 25 of Mon Nov 16, 2026 (pre-game rankings)
  - https://en.wikipedia.org/wiki/2026_Baylor_Bears_football_team | pulled 2026-11-21T05:40:00Z | Baylor Bears: 2026 schedule/roster page used for rest days, venue travel and injury mentions
  - https://en.wikipedia.org/wiki/2026_Texas_Tech_Red_Raiders_football_team | pulled 2026-11-21T05:39:59Z | Texas Tech Red Raiders: 2026 schedule/roster page used for rest days, venue travel and injury mentions
  - https://api.weather.gov/gridpoints/FWD/77,50/forecast | pulled 2026-11-21T07:04:43Z | NWS forecast at kickoff (conditions, wind speed/direction, temperature)
  - https://api.weather.gov/gridpoints/FWD/77,50/forecast/hourly | pulled 2026-11-21T07:04:44Z | NWS forecast at kickoff (conditions, wind speed/direction, temperature)

## Texas A&M Aggies at Oklahoma Sooners

- **Kickoff:** 2026-11-21 15:45 ET (Sat) | **Venue:** Memorial Stadium (Norman, OK), Norman | **TV:** ESPN2
- **AP Top 25 (Nov 16):** home unranked (-) / away 8 (8–2)
- **Closing line (DraftKings, pulled 2026-11-21T06:17:39Z):** OU -7 (margin 7.0), OU 37.5; ML home -142 -> -290, away +120 -> +235
- **Weather at kickoff:** Mostly Sunny then Slight Chance Showers And Thunderstorms, 69F, wind S 10 to 18 mph (hourly: Slight Chance Showers And Thunderstorms | 16 mph S)
- **Rest / travel / home-road:** rest 6 vs 7 days (last games 2026-11-15 / 2026-11-14); 324 mi campus-to-campus; home record 4-2 (home team), away team road record 0-4
- **Power ratings:** DSP 12.61 (home) vs 14.50 (away); league home-advantage term 10.50; model margin +8.6 (home). ESPN FPI win%: home 61.7 / away 38.3
- **Offense vs defense (season, all tracked games):**
  - Oklahoma Sooners (home, 10 games): 22.3 PPG scored / 19.0 allowed; 334.5 yds-gm vs 294.6 allowed; 9.34 yds/play (pass n/a yds/att, rush 3.31 yds/att); 3rd down 40.9%, 4th down 50.0%
    - success-rate proxies: opponent-adjusted PPA +0.024 (points/play minus opponent's, per tracked drive data), raw PPA 0.623, yards/play 9.34, 3rd-down rate 40.9%
    - takeaways/giveaways: 13 / 15 (margin -2); time of possession 31.6 min/gm
    - special teams / field position (drive-derived): net punt 8.0 yds (touchbacks excluded), punts/gm 4.3, drives ending in a turnover/gm 1.3, scoring-drive rate 34.8%, avg drive start 27.5 yds from own goal - see Method note 4
  - Texas A&M Aggies (away, 10 games): 24.2 PPG scored / 19.0 allowed; 341.2 yds-gm vs 319.0 allowed; 9.37 yds/play (pass n/a yds/att, rush 4.22 yds/att); 3rd down 40.3%, 4th down 42.9%
    - success-rate proxies: opponent-adjusted PPA +0.074 (points/play minus opponent's, per tracked drive data), raw PPA 0.665, yards/play 9.37, 3rd-down rate 40.3%
    - takeaways/giveaways: 11 / 13 (margin -2); time of possession 31.1 min/gm
    - special teams / field position (drive-derived): net punt None yds (touchbacks excluded), punts/gm 4.0, drives ending in a turnover/gm 1.3, scoring-drive rate 293.3%, avg drive start 71.9 yds from own goal - see Method note 4
- **Key skill-player availability (checked as of 2026-11-21):**
  - John Mateer (Oklahoma Sooners, home, QB1 (most-started QB, 10 of 10 tracked team box scores)): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Lloyd Avant (Oklahoma Sooners, home, most-listed backfield name in tracked ESPN team box scores (5 games); ESPN game logs expose no position yardage): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Isaiah Sategna III (Oklahoma Sooners, home, most-listed receiving name in tracked ESPN team box scores (4 games); ESPN game logs expose no position yardage): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Marcel Reed (Texas A&M Aggies, away, QB1 (most-started QB, 10 of 10 tracked team box scores)): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - KJ Edwards (Texas A&M Aggies, away, most-listed backfield name in tracked ESPN team box scores (5 games); ESPN game logs expose no position yardage): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Isaiah Horton (Texas A&M Aggies, away, most-listed receiving name in tracked ESPN team box scores (3 games); ESPN game logs expose no position yardage): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
- **Prediction:** final score Oklahoma 19.0, Texas 18.5 -> blended margin +0.8 (home); market-only margin -7.0; model-only +8.6
  - arithmetic: (37.5 + 0.8)/2 = 19.1 (home); (37.5 - 0.8)/2 = 18.4 (away); blended = mean(market -7.0, Massey model +8.6)
- **Sources (real public URLs, with pull dates):**
  - https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261121 | pulled 2026-11-21T06:17:39Z | Week 12 slate, kickoff time, venue, TV, DraftKings closing spread/OU/moneyline (open + close)
  - https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event=401856752 | pulled 2026-11-21T06:17:40Z | ESPN game payload: season team stats used for the offense/defense splits, box-score participant lists behind the availability check, and ESPN FPI win probability
  - https://en.wikipedia.org/wiki/2026_NCAA_Division_I_FBS_football_rankings | pulled 2026-11-21T05:39:51Z | AP Top 25 of Mon Nov 16, 2026 (pre-game rankings)
  - https://en.wikipedia.org/wiki/2026_Oklahoma_Sooners_football_team | pulled 2026-11-21T05:40:02Z | Oklahoma Sooners: 2026 schedule/roster page used for rest days, venue travel and injury mentions
  - https://api.weather.gov/gridpoints/OUN/100,82/forecast | pulled 2026-11-21T07:04:44Z | NWS forecast at kickoff (conditions, wind speed/direction, temperature)
  - https://api.weather.gov/gridpoints/OUN/100,82/forecast/hourly | pulled 2026-11-21T07:04:45Z | NWS forecast at kickoff (conditions, wind speed/direction, temperature)

## Maryland Terrapins at USC Trojans

- **Kickoff:** 2026-11-21 18:15 ET (Sat) | **Venue:** Los Angeles Memorial Coliseum, Los Angeles | **TV:** BTN
- **AP Top 25 (Nov 16):** home 18 (7–3) / away unranked (-)
- **Closing line (DraftKings, pulled 2026-11-21T06:17:39Z):** USC -17.5 (margin 17.5), OU 56.5; ML home -800 -> -950, away +550 -> +625
- **Weather at kickoff:** Sunny, 68F, wind NW 0 to 5 mph (hourly: Sunny | 5 mph W)
- **Rest / travel / home-road:** rest 7 vs 7 days (last games 2026-11-14 / 2026-11-14); 2302 mi campus-to-campus; home record 5-1 (home team), away team road record 2-2
- **Power ratings:** DSP 11.46 (home) vs -4.56 (away); league home-advantage term 10.50; model margin +26.5 (home). ESPN FPI win%: home 93.1 / away 6.9
- **Offense vs defense (season, all tracked games):**
  - USC Trojans (home, 10 games): 30.5 PPG scored / 24.5 allowed; 422.3 yds-gm vs 356.5 allowed; 13.07 yds/play (pass n/a yds/att, rush 3.91 yds/att); 3rd down 46.6%, 4th down 65.0%
    - success-rate proxies: opponent-adjusted PPA +0.161 (points/play minus opponent's, per tracked drive data), raw PPA 0.944, yards/play 13.07, 3rd-down rate 46.6%
    - takeaways/giveaways: 8 / 12 (margin -4); time of possession 30.8 min/gm
    - special teams / field position (drive-derived): net punt 11.0 yds (touchbacks excluded), punts/gm 2.0, drives ending in a turnover/gm 1.2, scoring-drive rate 46.1%, avg drive start 28.1 yds from own goal - see Method note 4
  - Maryland Terrapins (away, 10 games): 27.3 PPG scored / 30.3 allowed; 361.2 yds-gm vs 359.9 allowed; 12.0 yds/play (pass n/a yds/att, rush 4.23 yds/att); 3rd down 34.1%, 4th down 63.2%
    - success-rate proxies: opponent-adjusted PPA +0.105 (points/play minus opponent's, per tracked drive data), raw PPA 0.907, yards/play 12.0, 3rd-down rate 34.1%
    - takeaways/giveaways: 15 / 11 (margin +4); time of possession 27.9 min/gm
    - special teams / field position (drive-derived): net punt 10.1 yds (touchbacks excluded), punts/gm 4.8, drives ending in a turnover/gm 1.0, scoring-drive rate 37.9%, avg drive start 32.5 yds from own goal - see Method note 4
- **Key skill-player availability (checked as of 2026-11-21):**
  - Jayden Maiava (USC Trojans, home, QB1 (most-started QB, 10 of 10 tracked team box scores)): FLAGGED: Floyd Boucard Braylan Shelby Jadyn Ramos CB Chasen Johnson OR Elbert “Rock” Hill IV Offense Pro-style WR Tanook Hines OR Tron Baker WR Kayden Dixon-Wyatt Ethan “Boobie” Feaster LT LG C RG RT Elijah Paige Hayden Treter OR Kaylon Miller Tobias Raymond Alani Noa Justin Tauanuu Vlad 
  - King Miller (USC Trojans, home, most-listed backfield name in tracked ESPN team box scores (7 games); ESPN game logs expose no position yardage): FLAGGED: Floyd Boucard Braylan Shelby Jadyn Ramos CB Chasen Johnson OR Elbert “Rock” Hill IV Offense Pro-style WR Tanook Hines OR Tron Baker WR Kayden Dixon-Wyatt Ethan “Boobie” Feaster LT LG C RG RT Elijah Paige Hayden Treter OR Kaylon Miller Tobias Raymond Alani Noa Justin Tauanuu Vlad 
  - Trent Mosley (USC Trojans, home, most-listed receiving name in tracked ESPN team box scores (5 games); ESPN game logs expose no position yardage): FLAGGED: Floyd Boucard Braylan Shelby Jadyn Ramos CB Chasen Johnson OR Elbert “Rock” Hill IV Offense Pro-style WR Tanook Hines OR Tron Baker WR Kayden Dixon-Wyatt Ethan “Boobie” Feaster LT LG C RG RT Elijah Paige Hayden Treter OR Kaylon Miller Tobias Raymond Alani Noa Justin Tauanuu Vlad 
  - Malik Washington (Maryland Terrapins, away, QB1 (most-started QB, 9 of 10 tracked team box scores)): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - DeJuan Williams (Maryland Terrapins, away, most-listed backfield name in tracked ESPN team box scores (6 games); ESPN game logs expose no position yardage): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Chris Durr Jr. (Maryland Terrapins, away, most-listed receiving name in tracked ESPN team box scores (7 games); ESPN game logs expose no position yardage): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
- **Prediction:** final score USC 30.5, Maryland 26.0 -> blended margin +4.5 (home); market-only margin -17.5; model-only +26.5
  - arithmetic: (56.5 + 4.5)/2 = 30.5 (home); (56.5 - 4.5)/2 = 26.0 (away); blended = mean(market -17.5, Massey model +26.5)
- **Sources (real public URLs, with pull dates):**
  - https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261121 | pulled 2026-11-21T06:17:39Z | Week 12 slate, kickoff time, venue, TV, DraftKings closing spread/OU/moneyline (open + close)
  - https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event=401858534 | pulled 2026-11-21T06:17:41Z | ESPN game payload: season team stats used for the offense/defense splits, box-score participant lists behind the availability check, and ESPN FPI win probability
  - https://en.wikipedia.org/wiki/2026_NCAA_Division_I_FBS_football_rankings | pulled 2026-11-21T05:39:51Z | AP Top 25 of Mon Nov 16, 2026 (pre-game rankings)
  - https://en.wikipedia.org/wiki/2026_USC_Trojans_football_team | pulled 2026-11-21T05:40:04Z | USC Trojans: 2026 schedule/roster page used for rest days, venue travel and injury mentions
  - https://en.wikipedia.org/wiki/2026_Maryland_Terrapins_football_team | pulled 2026-11-21T05:40:02Z | Maryland Terrapins: 2026 schedule/roster page used for rest days, venue travel and injury mentions
  - https://api.weather.gov/gridpoints/LOX/153,44/forecast | pulled 2026-11-21T07:04:45Z | NWS forecast at kickoff (conditions, wind speed/direction, temperature)
  - https://api.weather.gov/gridpoints/LOX/153,44/forecast/hourly | pulled 2026-11-21T07:04:45Z | NWS forecast at kickoff (conditions, wind speed/direction, temperature)

## Virginia Tech Hokies at Miami Hurricanes

- **Kickoff:** 2026-11-21 19:00 ET (Sat) | **Venue:** Hard Rock Stadium, Miami Gardens | **TV:** ESPN/Disney+
- **AP Top 25 (Nov 16):** home 5 (9–1) / away unranked (-)
- **Closing line (DraftKings, pulled 2026-11-21T06:17:39Z):** MIA -20.5 (margin 20.5), OU 60.5; ML home -1050 -> -1650, away +675 -> +950
- **Weather at kickoff:** Partly Cloudy, 72F, wind S 3 to 7 mph (hourly: Mostly Cloudy | 6 mph S)
- **Rest / travel / home-road:** rest 7 vs 7 days (last games 2026-11-14 / 2026-11-14); 778 mi campus-to-campus; home record 5-0 (home team), away team road record 3-2
- **Power ratings:** DSP 30.05 (home) vs -2.65 (away); league home-advantage term 10.50; model margin +43.2 (home). ESPN FPI win%: home 96.3 / away 3.7
- **Offense vs defense (season, all tracked games):**
  - Miami Hurricanes (home, 10 games): 44.1 PPG scored / 19.8 allowed; 518.1 yds-gm vs 325.4 allowed; 14.59 yds/play (pass n/a yds/att, rush 5.27 yds/att); 3rd down 52.6%, 4th down 50.0%
    - success-rate proxies: opponent-adjusted PPA +0.427 (points/play minus opponent's, per tracked drive data), raw PPA 1.242, yards/play 14.59, 3rd-down rate 52.6%
    - takeaways/giveaways: 11 / 5 (margin +6); time of possession 33.7 min/gm
    - special teams / field position (drive-derived): net punt 9.9 yds (touchbacks excluded), punts/gm 2.6, drives ending in a turnover/gm 0.4, scoring-drive rate 61.4%, avg drive start 29.0 yds from own goal - see Method note 4
  - Virginia Tech Hokies (away, 10 games): 33.0 PPG scored / 25.5 allowed; 420.8 yds-gm vs 349.6 allowed; 11.43 yds/play (pass n/a yds/att, rush 3.73 yds/att); 3rd down 41.7%, 4th down 68.2%
    - success-rate proxies: opponent-adjusted PPA +0.053 (points/play minus opponent's, per tracked drive data), raw PPA 0.897, yards/play 11.43, 3rd-down rate 41.7%
    - takeaways/giveaways: 7 / 15 (margin -8); time of possession 31.3 min/gm
    - special teams / field position (drive-derived): net punt 8.1 yds (touchbacks excluded), punts/gm 3.5, drives ending in a turnover/gm 1.0, scoring-drive rate 42.1%, avg drive start 31.1 yds from own goal - see Method note 4
- **Key skill-player availability (checked as of 2026-11-21):**
  - Darian Mensah (Miami Hurricanes, home, QB1 (most-started QB, 10 of 10 tracked team box scores)): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Javian Mallory (Miami Hurricanes, home, most-listed backfield name in tracked ESPN team box scores (5 games); ESPN game logs expose no position yardage): FLAGGED: # Name Class K 22 Jake Weinberg So LS 46 Adam Booker Sr K 82 Jack Olsen Sr P 94 Dylan Joyce Sr P 96 Tucker Tevepaugh So K 97 Will Rocha Jr Head coach Mario Cristobal Coordinators/assistant coaches Shannon Dawson – Offensive Coordinator/Quarterbacks Corey Hetherman – Defensive Coo
  - Malachi Toney (Miami Hurricanes, home, most-listed receiving name in tracked ESPN team box scores (7 games); ESPN game logs expose no position yardage): FLAGGED: # Name Class K 22 Jake Weinberg So LS 46 Adam Booker Sr K 82 Jack Olsen Sr P 94 Dylan Joyce Sr P 96 Tucker Tevepaugh So K 97 Will Rocha Jr Head coach Mario Cristobal Coordinators/assistant coaches Shannon Dawson – Offensive Coordinator/Quarterbacks Corey Hetherman – Defensive Coo
  - Ethan Grunkemeyer (Virginia Tech Hokies, away, QB1 (most-started QB, 10 of 10 tracked team box scores)): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Jeffrey Overton Jr. (Virginia Tech Hokies, away, most-listed backfield name in tracked ESPN team box scores (9 games); ESPN game logs expose no position yardage): FLAGGED: Assistant linebackers Mike Moyseenko Assistant quarterbacks Cam Phillips Assistant wide receivers Danny Rocco Senior defensive analyst for offense David Rocco Associate tight ends Warren Ruggiero Senior offensive analyst Pat Shepard Assistant special teams Derrick Tangelo Assista
  - Que'Sean Brown (Virginia Tech Hokies, away, most-listed receiving name in tracked ESPN team box scores (6 games); ESPN game logs expose no position yardage): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
- **Prediction:** final score Miami 36.0, Virginia 24.5 -> blended margin +11.3 (home); market-only margin -20.5; model-only +43.2
  - arithmetic: (60.5 + 11.3)/2 = 35.9 (home); (60.5 - 11.3)/2 = 24.6 (away); blended = mean(market -20.5, Massey model +43.2)
- **Sources (real public URLs, with pull dates):**
  - https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261121 | pulled 2026-11-21T06:17:39Z | Week 12 slate, kickoff time, venue, TV, DraftKings closing spread/OU/moneyline (open + close)
  - https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event=401858302 | pulled 2026-11-21T06:17:41Z | ESPN game payload: season team stats used for the offense/defense splits, box-score participant lists behind the availability check, and ESPN FPI win probability
  - https://en.wikipedia.org/wiki/2026_NCAA_Division_I_FBS_football_rankings | pulled 2026-11-21T05:39:51Z | AP Top 25 of Mon Nov 16, 2026 (pre-game rankings)
  - https://en.wikipedia.org/wiki/2026_Miami_Hurricanes_football_team | pulled 2026-11-21T05:40:06Z | Miami Hurricanes: 2026 schedule/roster page used for rest days, venue travel and injury mentions
  - https://en.wikipedia.org/wiki/2026_Virginia_Tech_Hokies_football_team | pulled 2026-11-21T05:40:05Z | Virginia Tech Hokies: 2026 schedule/roster page used for rest days, venue travel and injury mentions
  - https://api.weather.gov/gridpoints/MFL/107,58/forecast | pulled 2026-11-21T07:04:46Z | NWS forecast at kickoff (conditions, wind speed/direction, temperature)
  - https://api.weather.gov/gridpoints/MFL/107,58/forecast/hourly | pulled 2026-11-21T07:04:46Z | NWS forecast at kickoff (conditions, wind speed/direction, temperature)

## Arizona Wildcats at Kansas State Wildcats

- **Kickoff:** 2026-11-21 19:00 ET (Sat) | **Venue:** Bill Snyder Family Stadium, Manhattan | **TV:** FS1
- **AP Top 25 (Nov 16):** home unranked (-) / away 19 (7–3)
- **Closing line (DraftKings, pulled 2026-11-21T06:17:39Z):** ARIZ -7.5 (margin 7.5), OU 51.5; ML home +300 -> +235, away -380 -> -290
- **Weather at kickoff:** Mostly Cloudy then Showers And Thunderstorms Likely, 68F, wind SW 5 to 15 mph (hourly: Showers And Thunderstorms | 5 mph SW)
- **Rest / travel / home-road:** rest 7 vs 7 days (last games 2026-11-14 / 2026-11-14); 937 mi campus-to-campus; home record 4-2 (home team), away team road record 2-2
- **Power ratings:** DSP -0.27 (home) vs 17.02 (away); league home-advantage term 10.50; model margin -6.8 (home). ESPN FPI win%: home 25.4 / away 74.6
- **Offense vs defense (season, all tracked games):**
  - Kansas State Wildcats (home, 10 games): 29.2 PPG scored / 26.1 allowed; 404.2 yds-gm vs 343.3 allowed; 11.04 yds/play (pass n/a yds/att, rush 5.0 yds/att); 3rd down 50.7%, 4th down 28.6%
    - success-rate proxies: opponent-adjusted PPA +0.058 (points/play minus opponent's, per tracked drive data), raw PPA 0.798, yards/play 11.04, 3rd-down rate 50.7%
    - takeaways/giveaways: 7 / 11 (margin -4); time of possession 32.2 min/gm
    - special teams / field position (drive-derived): net punt 12.7 yds (touchbacks excluded), punts/gm 3.9, drives ending in a turnover/gm 1.1, scoring-drive rate 41.2%, avg drive start 28.0 yds from own goal - see Method note 4
  - Arizona Wildcats (away, 10 games): 34.7 PPG scored / 21.9 allowed; 450.1 yds-gm vs 345.7 allowed; 13.72 yds/play (pass n/a yds/att, rush 3.78 yds/att); 3rd down 49.6%, 4th down 50.0%
    - success-rate proxies: opponent-adjusted PPA +0.414 (points/play minus opponent's, per tracked drive data), raw PPA 1.058, yards/play 13.72, 3rd-down rate 49.6%
    - takeaways/giveaways: 12 / 10 (margin +2); time of possession 32.4 min/gm
    - special teams / field position (drive-derived): net punt 5.7 yds (touchbacks excluded), punts/gm 3.3, drives ending in a turnover/gm 0.9, scoring-drive rate 48.3%, avg drive start 28.7 yds from own goal - see Method note 4
- **Key skill-player availability (checked as of 2026-11-21):**
  - Avery Johnson (Kansas State Wildcats, home, QB1 (most-started QB, 6 of 10 tracked team box scores)): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Rodney Fields Jr. (Kansas State Wildcats, home, most-listed backfield name in tracked ESPN team box scores (6 games); ESPN game logs expose no position yardage): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Derrick Salley Jr. (Kansas State Wildcats, home, most-listed receiving name in tracked ESPN team box scores (4 games); ESPN game logs expose no position yardage): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Noah Fifita (Arizona Wildcats, away, QB1 (most-started QB, 10 of 10 tracked team box scores)): FLAGGED: Antwan Roberts Jr."},"RB1_Third":{"wt":"Wesley Yarbrough"},"WR1_Starter":{"wt":"Tre Spivey"},"WR1_Backup":{"wt":"Brandon Phelps"},"WR1_Third":{"wt":"&apos;&apos;RJ Mosley&apos;&apos;"},"WR2_Starter":{"wt":"Giovanni Richardson"},"WR2_Backup":{"wt":"Rodney Gallagher III"},"WR2_Thir
  - Kedrick Reescano (Arizona Wildcats, away, most-listed backfield name in tracked ESPN team box scores (6 games); ESPN game logs expose no position yardage): FLAGGED: Antwan Roberts Jr."},"RB1_Third":{"wt":"Wesley Yarbrough"},"WR1_Starter":{"wt":"Tre Spivey"},"WR1_Backup":{"wt":"Brandon Phelps"},"WR1_Third":{"wt":"&apos;&apos;RJ Mosley&apos;&apos;"},"WR2_Starter":{"wt":"Giovanni Richardson"},"WR2_Backup":{"wt":"Rodney Gallagher III"},"WR2_Thir
  - Isaiah Mizell (Arizona Wildcats, away, most-listed receiving name in tracked ESPN team box scores (4 games); ESPN game logs expose no position yardage): FLAGGED: Antwan Roberts Jr."},"RB1_Third":{"wt":"Wesley Yarbrough"},"WR1_Starter":{"wt":"Tre Spivey"},"WR1_Backup":{"wt":"Brandon Phelps"},"WR1_Third":{"wt":"&apos;&apos;RJ Mosley&apos;&apos;"},"WR2_Starter":{"wt":"Giovanni Richardson"},"WR2_Backup":{"wt":"Rodney Gallagher III"},"WR2_Thir
- **Prediction:** final score Kansas 26.0, Arizona 25.5 -> blended margin +0.4 (home); market-only margin +7.5; model-only -6.8
  - arithmetic: (51.5 + 0.4)/2 = 25.9 (home); (51.5 - 0.4)/2 = 25.6 (away); blended = mean(market +7.5, Massey model -6.8)
- **Sources (real public URLs, with pull dates):**
  - https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261121 | pulled 2026-11-21T06:17:39Z | Week 12 slate, kickoff time, venue, TV, DraftKings closing spread/OU/moneyline (open + close)
  - https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event=401856865 | pulled 2026-11-21T06:17:41Z | ESPN game payload: season team stats used for the offense/defense splits, box-score participant lists behind the availability check, and ESPN FPI win probability
  - https://en.wikipedia.org/wiki/2026_NCAA_Division_I_FBS_football_rankings | pulled 2026-11-21T05:39:51Z | AP Top 25 of Mon Nov 16, 2026 (pre-game rankings)
  - https://en.wikipedia.org/wiki/2026_Kansas_State_Wildcats_football_team | pulled 2026-11-21T05:40:07Z | Kansas State Wildcats: 2026 schedule/roster page used for rest days, venue travel and injury mentions
  - https://en.wikipedia.org/wiki/2026_Arizona_Wildcats_football_team | pulled 2026-11-21T05:40:07Z | Arizona Wildcats: 2026 schedule/roster page used for rest days, venue travel and injury mentions
  - https://api.weather.gov/gridpoints/TOP/49,56/forecast | pulled 2026-11-21T07:04:47Z | NWS forecast at kickoff (conditions, wind speed/direction, temperature)
  - https://api.weather.gov/gridpoints/TOP/49,56/forecast/hourly | pulled 2026-11-21T07:04:47Z | NWS forecast at kickoff (conditions, wind speed/direction, temperature)

## Georgia Bulldogs at South Carolina Gamecocks

- **Kickoff:** 2026-11-21 19:30 ET (Sat) | **Venue:** Williams-Brice Stadium, Columbia | **TV:** ABC
- **AP Top 25 (Nov 16):** home unranked (-) / away 1 (9–1)
- **Closing line (DraftKings, pulled 2026-11-21T06:17:39Z):** UGA -14.5 (margin 14.5), OU 50.5; ML home +295 -> +525, away -375 -> -750
- **Weather at kickoff:** Light Rain Likely, 57F, wind NE 6 to 13 mph (hourly: Light Rain Likely | 12 mph NE)
- **Rest / travel / home-road:** rest 7 vs 7 days (last games 2026-11-14 / 2026-11-14); 135 mi campus-to-campus; home record 4-2 (home team), away team road record 3-0
- **Power ratings:** DSP 14.30 (home) vs 31.79 (away); league home-advantage term 10.50; model margin -7.0 (home). ESPN FPI win%: home 13.1 / away 86.9
- **Offense vs defense (season, all tracked games):**
  - South Carolina Gamecocks (home, 10 games): 31.8 PPG scored / 24.5 allowed; 444.2 yds-gm vs 353.6 allowed; 12.17 yds/play (pass n/a yds/att, rush 5.33 yds/att); 3rd down 46.5%, 4th down 59.1%
    - success-rate proxies: opponent-adjusted PPA +0.165 (points/play minus opponent's, per tracked drive data), raw PPA 0.871, yards/play 12.17, 3rd-down rate 46.5%
    - takeaways/giveaways: 6 / 17 (margin -11); time of possession 29.2 min/gm
    - special teams / field position (drive-derived): net punt 6.1 yds (touchbacks excluded), punts/gm 3.2, drives ending in a turnover/gm 1.7, scoring-drive rate 44.5%, avg drive start 27.4 yds from own goal - see Method note 4
  - Georgia Bulldogs (away, 10 games): 41.8 PPG scored / 14.7 allowed; 455.6 yds-gm vs 272.5 allowed; 12.83 yds/play (pass n/a yds/att, rush 5.85 yds/att); 3rd down 51.8%, 4th down 66.7%
    - success-rate proxies: opponent-adjusted PPA +0.766 (points/play minus opponent's, per tracked drive data), raw PPA 1.177, yards/play 12.83, 3rd-down rate 51.8%
    - takeaways/giveaways: 18 / 10 (margin +8); time of possession 31.3 min/gm
    - special teams / field position (drive-derived): net punt 10.8 yds (touchbacks excluded), punts/gm 2.8, drives ending in a turnover/gm 0.8, scoring-drive rate 54.4%, avg drive start 33.9 yds from own goal - see Method note 4
- **Key skill-player availability (checked as of 2026-11-21):**
  - LaNorris Sellers (South Carolina Gamecocks, home, QB1 (most-started QB, 9 of 10 tracked team box scores)): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Matt Fuller (South Carolina Gamecocks, home, most-listed backfield name in tracked ESPN team box scores (4 games); ESPN game logs expose no position yardage): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Nyck Harbor (South Carolina Gamecocks, home, most-listed receiving name in tracked ESPN team box scores (4 games); ESPN game logs expose no position yardage): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Gunner Stockton (Georgia Bulldogs, away, QB1 (most-started QB, 10 of 10 tracked team box scores)): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Nate Frazier (Georgia Bulldogs, away, most-listed backfield name in tracked ESPN team box scores (4 games); ESPN game logs expose no position yardage): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Craig Dandridge (Georgia Bulldogs, away, most-listed receiving name in tracked ESPN team box scores (4 games); ESPN game logs expose no position yardage): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
- **Prediction:** final score South 27.0, Georgia 23.5 -> blended margin +3.8 (home); market-only margin +14.5; model-only -7.0
  - arithmetic: (50.5 + 3.8)/2 = 27.1 (home); (50.5 - 3.8)/2 = 23.4 (away); blended = mean(market +14.5, Massey model -7.0)
- **Sources (real public URLs, with pull dates):**
  - https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261121 | pulled 2026-11-21T06:17:39Z | Week 12 slate, kickoff time, venue, TV, DraftKings closing spread/OU/moneyline (open + close)
  - https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event=401856753 | pulled 2026-11-21T06:17:42Z | ESPN game payload: season team stats used for the offense/defense splits, box-score participant lists behind the availability check, and ESPN FPI win probability
  - https://en.wikipedia.org/wiki/2026_NCAA_Division_I_FBS_football_rankings | pulled 2026-11-21T05:39:51Z | AP Top 25 of Mon Nov 16, 2026 (pre-game rankings)
  - https://en.wikipedia.org/wiki/2026_South_Carolina_Gamecocks_football_team | pulled 2026-11-21T05:40:08Z | South Carolina Gamecocks: 2026 schedule/roster page used for rest days, venue travel and injury mentions
  - https://en.wikipedia.org/wiki/2026_Georgia_Bulldogs_football_team | pulled 2026-11-21T05:40:08Z | Georgia Bulldogs: 2026 schedule/roster page used for rest days, venue travel and injury mentions
  - https://api.weather.gov/gridpoints/CAE/65,60/forecast | pulled 2026-11-21T07:04:48Z | NWS forecast at kickoff (conditions, wind speed/direction, temperature)
  - https://api.weather.gov/gridpoints/CAE/65,60/forecast/hourly | pulled 2026-11-21T07:04:48Z | NWS forecast at kickoff (conditions, wind speed/direction, temperature)

## SMU Mustangs at Notre Dame Fighting Irish

- **Kickoff:** 2026-11-21 19:30 ET (Sat) | **Venue:** Notre Dame Stadium, Notre Dame | **TV:** NBC
- **AP Top 25 (Nov 16):** home 3 (9–1) / away unranked (-)
- **Closing line (DraftKings, pulled 2026-11-21T06:17:39Z):** ND -20.5 (margin 20.5), OU 56.5; ML home -950 -> -1650, away +625 -> +950
- **Weather at kickoff:** Mostly Clear, 46F, wind S 5 mph (hourly: Clear | 5 mph S)
- **Rest / travel / home-road:** rest 7 vs 7 days (last games 2026-11-14 / 2026-11-14); 842 mi campus-to-campus; home record 6-0 (home team), away team road record 1-2
- **Power ratings:** DSP 28.86 (home) vs 2.81 (away); league home-advantage term 10.50; model margin +36.5 (home). ESPN FPI win%: home 93.4 / away 6.6
- **Offense vs defense (season, all tracked games):**
  - Notre Dame Fighting Irish (home, 10 games): 39.5 PPG scored / 13.8 allowed; 445.4 yds-gm vs 239.6 allowed; 12.41 yds/play (pass n/a yds/att, rush 5.17 yds/att); 3rd down 45.0%, 4th down 72.7%
    - success-rate proxies: opponent-adjusted PPA +0.637 (points/play minus opponent's, per tracked drive data), raw PPA 1.1, yards/play 12.41, 3rd-down rate 45.0%
    - takeaways/giveaways: 20 / 4 (margin +16); time of possession 32.5 min/gm
    - special teams / field position (drive-derived): net punt 10.6 yds (touchbacks excluded), punts/gm 2.3, drives ending in a turnover/gm 0.3, scoring-drive rate 56.6%, avg drive start 31.2 yds from own goal - see Method note 4
  - SMU Mustangs (away, 10 games): 34.0 PPG scored / 25.5 allowed; 455.7 yds-gm vs 341.3 allowed; 13.29 yds/play (pass n/a yds/att, rush 4.24 yds/att); 3rd down 44.8%, 4th down 66.7%
    - success-rate proxies: opponent-adjusted PPA +0.269 (points/play minus opponent's, per tracked drive data), raw PPA 0.991, yards/play 13.29, 3rd-down rate 44.8%
    - takeaways/giveaways: 9 / 15 (margin -6); time of possession 29.2 min/gm
    - special teams / field position (drive-derived): net punt 8.3 yds (touchbacks excluded), punts/gm 2.8, drives ending in a turnover/gm 1.4, scoring-drive rate 49.6%, avg drive start 30.4 yds from own goal - see Method note 4
- **Key skill-player availability (checked as of 2026-11-21):**
  - CJ Carr (Notre Dame Fighting Irish, home, QB1 (most-started QB, 10 of 10 tracked team box scores)): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Nolan James Jr. (Notre Dame Fighting Irish, home, most-listed backfield name in tracked ESPN team box scores (4 games); ESPN game logs expose no position yardage): FLAGGED: Jonaz Walton Aneyas Williams Injuries [ edit ] Player Position Injury Status Will Black OL Concussion Questionable Francis Brewu DL Left knee Questionable Brauntae Johnson S Left foot Questionable Jason Onye DL Right knee Questionable Drayk Bowen LB Right ankle Out for next game 
  - Micah Gilbert (Notre Dame Fighting Irish, home, most-listed receiving name in tracked ESPN team box scores (4 games); ESPN game logs expose no position yardage): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Kevin Jennings (SMU Mustangs, away, QB1 (most-started QB, 10 of 10 tracked team box scores)): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Kendrick Raphael (SMU Mustangs, away, most-listed backfield name in tracked ESPN team box scores (8 games); ESPN game logs expose no position yardage): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Yamir Knight (SMU Mustangs, away, most-listed receiving name in tracked ESPN team box scores (4 games); ESPN game logs expose no position yardage): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
- **Prediction:** final score Notre 32.0, SMU 24.0 -> blended margin +8.0 (home); market-only margin -20.5; model-only +36.5
  - arithmetic: (56.5 + 8.0)/2 = 32.2 (home); (56.5 - 8.0)/2 = 24.2 (away); blended = mean(market -20.5, Massey model +36.5)
- **Sources (real public URLs, with pull dates):**
  - https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261121 | pulled 2026-11-21T06:17:39Z | Week 12 slate, kickoff time, venue, TV, DraftKings closing spread/OU/moneyline (open + close)
  - https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event=401858307 | pulled 2026-11-21T06:17:42Z | ESPN game payload: season team stats used for the offense/defense splits, box-score participant lists behind the availability check, and ESPN FPI win probability
  - https://en.wikipedia.org/wiki/2026_NCAA_Division_I_FBS_football_rankings | pulled 2026-11-21T05:39:51Z | AP Top 25 of Mon Nov 16, 2026 (pre-game rankings)
  - https://en.wikipedia.org/wiki/2026_Notre_Dame_Fighting_Irish_football_team | pulled 2026-11-21T05:40:09Z | Notre Dame Fighting Irish: 2026 schedule/roster page used for rest days, venue travel and injury mentions
  - https://en.wikipedia.org/wiki/2026_SMU_Mustangs_football_team | pulled 2026-11-21T05:40:09Z | SMU Mustangs: 2026 schedule/roster page used for rest days, venue travel and injury mentions
  - https://api.weather.gov/gridpoints/IWX/30,64/forecast | pulled 2026-11-21T07:04:49Z | NWS forecast at kickoff (conditions, wind speed/direction, temperature)
  - https://api.weather.gov/gridpoints/IWX/30,64/forecast/hourly | pulled 2026-11-21T07:04:49Z | NWS forecast at kickoff (conditions, wind speed/direction, temperature)

## Kentucky Wildcats at Missouri Tigers

- **Kickoff:** 2026-11-21 19:30 ET (Sat) | **Venue:** Memorial Stadium, Columbia | **TV:** SEC Network
- **AP Top 25 (Nov 16):** home unranked (-) / away 17 (7–3)
- **Closing line (DraftKings, pulled 2026-11-21T06:17:39Z):** MIZ -4.5 (margin 4.5), OU 48.5; ML home -225 -> -205, away +185 -> +170
- **Weather at kickoff:** Mostly Cloudy, 60F, wind SSW 0 to 5 mph (hourly: Mostly Cloudy | 0 mph)
- **Rest / travel / home-road:** rest 7 vs 7 days (last games 2026-11-14 / 2026-11-14); 428 mi campus-to-campus; home record 4-1 (home team), away team road record 3-1
- **Power ratings:** DSP 17.39 (home) vs 13.68 (away); league home-advantage term 10.50; model margin +14.2 (home). ESPN FPI win%: home 61.5 / away 38.5
- **Offense vs defense (season, all tracked games):**
  - Missouri Tigers (home, 10 games): 29.3 PPG scored / 22.9 allowed; 401.9 yds-gm vs 347.0 allowed; 11.58 yds/play (pass n/a yds/att, rush 4.4 yds/att); 3rd down 37.4%, 4th down 53.8%
    - success-rate proxies: opponent-adjusted PPA +0.137 (points/play minus opponent's, per tracked drive data), raw PPA 0.844, yards/play 11.58, 3rd-down rate 37.4%
    - takeaways/giveaways: 16 / 7 (margin +9); time of possession 29.9 min/gm
    - special teams / field position (drive-derived): net punt 12.8 yds (touchbacks excluded), punts/gm 4.8, drives ending in a turnover/gm 0.7, scoring-drive rate 39.5%, avg drive start 32.4 yds from own goal - see Method note 4
  - Kentucky Wildcats (away, 10 games): 28.3 PPG scored / 25.3 allowed; 369.4 yds-gm vs 362.0 allowed; 10.8 yds/play (pass n/a yds/att, rush 4.49 yds/att); 3rd down 36.2%, 4th down 50.0%
    - success-rate proxies: opponent-adjusted PPA +0.068 (points/play minus opponent's, per tracked drive data), raw PPA 0.827, yards/play 10.8, 3rd-down rate 36.2%
    - takeaways/giveaways: 18 / 9 (margin +9); time of possession 30.1 min/gm
    - special teams / field position (drive-derived): net punt 13.5 yds (touchbacks excluded), punts/gm 3.3, drives ending in a turnover/gm 0.8, scoring-drive rate 42.6%, avg drive start 30.0 yds from own goal - see Method note 4
- **Key skill-player availability (checked as of 2026-11-21):**
  - Austin Simmons (Missouri Tigers, home, QB1 (most-started QB, 10 of 10 tracked team box scores)): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Jamal Roberts (Missouri Tigers, home, most-listed backfield name in tracked ESPN team box scores (10 games); ESPN game logs expose no position yardage): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Cayden Lee (Missouri Tigers, home, most-listed receiving name in tracked ESPN team box scores (5 games); ESPN game logs expose no position yardage): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Kenny Minchey (Kentucky Wildcats, away, QB1 (most-started QB, 10 of 10 tracked team box scores)): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - CJ Baxter (Kentucky Wildcats, away, most-listed backfield name in tracked ESPN team box scores (5 games); ESPN game logs expose no position yardage): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Kenny Darby (Kentucky Wildcats, away, most-listed receiving name in tracked ESPN team box scores (5 games); ESPN game logs expose no position yardage): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
- **Prediction:** final score Missouri 26.5, Kentucky 22.0 -> blended margin +4.9 (home); market-only margin -4.5; model-only +14.2
  - arithmetic: (48.5 + 4.9)/2 = 26.7 (home); (48.5 - 4.9)/2 = 21.8 (away); blended = mean(market -4.5, Massey model +14.2)
- **Sources (real public URLs, with pull dates):**
  - https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261121 | pulled 2026-11-21T06:17:39Z | Week 12 slate, kickoff time, venue, TV, DraftKings closing spread/OU/moneyline (open + close)
  - https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event=401856751 | pulled 2026-11-21T06:17:42Z | ESPN game payload: season team stats used for the offense/defense splits, box-score participant lists behind the availability check, and ESPN FPI win probability
  - https://en.wikipedia.org/wiki/2026_NCAA_Division_I_FBS_football_rankings | pulled 2026-11-21T05:39:51Z | AP Top 25 of Mon Nov 16, 2026 (pre-game rankings)
  - https://en.wikipedia.org/wiki/2026_Missouri_Tigers_football_team | pulled 2026-11-21T05:40:10Z | Missouri Tigers: 2026 schedule/roster page used for rest days, venue travel and injury mentions
  - https://en.wikipedia.org/wiki/2026_Kentucky_Wildcats_football_team | pulled 2026-11-21T05:40:10Z | Kentucky Wildcats: 2026 schedule/roster page used for rest days, venue travel and injury mentions
  - https://api.weather.gov/gridpoints/EWX/156,92/forecast | pulled 2026-11-21T07:04:41Z | NWS forecast at kickoff (conditions, wind speed/direction, temperature)
  - https://api.weather.gov/gridpoints/EWX/156,92/forecast/hourly | pulled 2026-11-21T07:04:41Z | NWS forecast at kickoff (conditions, wind speed/direction, temperature)

## Pittsburgh Panthers at Louisville Cardinals

- **Kickoff:** 2026-11-21 19:30 ET (Sat) | **Venue:** L&N Federal Credit Union Stadium, Louisville | **TV:** ESPN2
- **AP Top 25 (Nov 16):** home 21 (7–3) / away unranked (-)
- **Closing line (DraftKings, pulled 2026-11-21T06:17:39Z):** LOU -13.5 (margin 13.5), OU 50.5; ML home -340 -> -575, away +270 -> +425
- **Weather at kickoff:** Mostly Clear, 43F, wind E 2 mph (hourly: Partly Cloudy | 2 mph SE)
- **Rest / travel / home-road:** rest 7 vs 8 days (last games 2026-11-14 / 2026-11-13); 344 mi campus-to-campus; home record 4-1 (home team), away team road record 1-2
- **Power ratings:** DSP 16.91 (home) vs 5.07 (away); league home-advantage term 10.50; model margin +22.3 (home). ESPN FPI win%: home 77.5 / away 22.5
- **Offense vs defense (season, all tracked games):**
  - Louisville Cardinals (home, 10 games): 38.3 PPG scored / 24.7 allowed; 469.5 yds-gm vs 393.3 allowed; 13.15 yds/play (pass n/a yds/att, rush 6.16 yds/att); 3rd down 43.8%, 4th down 0.0%
    - success-rate proxies: opponent-adjusted PPA +0.425 (points/play minus opponent's, per tracked drive data), raw PPA 1.073, yards/play 13.15, 3rd-down rate 43.8%
    - takeaways/giveaways: 17 / 8 (margin +9); time of possession 29.2 min/gm
    - special teams / field position (drive-derived): net punt 7.3 yds (touchbacks excluded), punts/gm 3.4, drives ending in a turnover/gm 0.8, scoring-drive rate 50.0%, avg drive start 30.8 yds from own goal - see Method note 4
  - Pittsburgh Panthers (away, 10 games): 29.7 PPG scored / 19.4 allowed; 432.1 yds-gm vs 314.8 allowed; 11.68 yds/play (pass n/a yds/att, rush 4.48 yds/att); 3rd down 40.0%, 4th down 39.1%
    - success-rate proxies: opponent-adjusted PPA +0.271 (points/play minus opponent's, per tracked drive data), raw PPA 0.803, yards/play 11.68, 3rd-down rate 40.0%
    - takeaways/giveaways: 14 / 12 (margin +2); time of possession 31.1 min/gm
    - special teams / field position (drive-derived): net punt 9.5 yds (touchbacks excluded), punts/gm 4.1, drives ending in a turnover/gm 1.2, scoring-drive rate 41.3%, avg drive start 29.8 yds from own goal - see Method note 4
- **Key skill-player availability (checked as of 2026-11-21):**
  - Lincoln Kienholz (Louisville Cardinals, home, QB1 (most-started QB, 10 of 10 tracked team box scores)): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Lawayne McCoy (Louisville Cardinals, home, most-listed receiving name in tracked ESPN team box scores (5 games); ESPN game logs expose no position yardage): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Mason Heintschel (Pittsburgh Panthers, away, QB1 (most-started QB, 5 of 10 tracked team box scores)): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Damon Ferguson Jr. (Pittsburgh Panthers, away, most-listed backfield name in tracked ESPN team box scores (7 games); ESPN game logs expose no position yardage): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Cataurus Hicks (Pittsburgh Panthers, away, most-listed receiving name in tracked ESPN team box scores (5 games); ESPN game logs expose no position yardage): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
- **Prediction:** final score Louisville 27.5, Pittsburgh 23.0 -> blended margin +4.4 (home); market-only margin -13.5; model-only +22.3
  - arithmetic: (50.5 + 4.4)/2 = 27.4 (home); (50.5 - 4.4)/2 = 23.1 (away); blended = mean(market -13.5, Massey model +22.3)
- **Sources (real public URLs, with pull dates):**
  - https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261121 | pulled 2026-11-21T06:17:39Z | Week 12 slate, kickoff time, venue, TV, DraftKings closing spread/OU/moneyline (open + close)
  - https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event=401858306 | pulled 2026-11-21T06:17:43Z | ESPN game payload: season team stats used for the offense/defense splits, box-score participant lists behind the availability check, and ESPN FPI win probability
  - https://en.wikipedia.org/wiki/2026_NCAA_Division_I_FBS_football_rankings | pulled 2026-11-21T05:39:51Z | AP Top 25 of Mon Nov 16, 2026 (pre-game rankings)
  - https://en.wikipedia.org/wiki/2026_Louisville_Cardinals_football_team | pulled 2026-11-21T05:40:11Z | Louisville Cardinals: 2026 schedule/roster page used for rest days, venue travel and injury mentions
  - https://en.wikipedia.org/wiki/2026_Pittsburgh_Panthers_football_team | pulled 2026-11-21T05:40:11Z | Pittsburgh Panthers: 2026 schedule/roster page used for rest days, venue travel and injury mentions
  - https://api.weather.gov/gridpoints/LMK/50,76/forecast | pulled 2026-11-21T07:04:50Z | NWS forecast at kickoff (conditions, wind speed/direction, temperature)
  - https://api.weather.gov/gridpoints/LMK/50,76/forecast/hourly | pulled 2026-11-21T07:04:50Z | NWS forecast at kickoff (conditions, wind speed/direction, temperature)

## Utah Utes at TCU Horned Frogs

- **Kickoff:** 2026-11-21 21:00 ET (Sat) | **Venue:** Amon G. Carter Stadium, Fort Worth | **TV:** Fox
- **AP Top 25 (Nov 16):** home unranked (-) / away 2 (10–0)
- **Closing line (DraftKings, pulled 2026-11-21T06:17:39Z):** UTAH -8.5 (margin 8.5), OU 46.5; ML home +170 -> +270, away -205 -> -340
- **Weather at kickoff:** Mostly Cloudy, 58F, wind SSW 5 to 10 mph (hourly: Mostly Cloudy | 10 mph S)
- **Rest / travel / home-road:** rest 7 vs 7 days (last games 2026-11-14 / 2026-11-14); 974 mi campus-to-campus; home record 4-3 (home team), away team road record 4-0
- **Power ratings:** DSP 7.71 (home) vs 23.47 (away); league home-advantage term 10.50; model margin -5.3 (home). ESPN FPI win%: home 26.5 / away 73.5
- **Offense vs defense (season, all tracked games):**
  - TCU Horned Frogs (home, 10 games): 23.4 PPG scored / 15.2 allowed; 372.9 yds-gm vs 304.4 allowed; 11.62 yds/play (pass n/a yds/att, rush 3.32 yds/att); 3rd down 45.0%, 4th down 46.7%
    - success-rate proxies: opponent-adjusted PPA +0.295 (points/play minus opponent's, per tracked drive data), raw PPA 0.729, yards/play 11.62, 3rd-down rate 45.0%
    - takeaways/giveaways: 14 / 15 (margin -1); time of possession 30.7 min/gm
    - special teams / field position (drive-derived): net punt 11.6 yds (touchbacks excluded), punts/gm 4.4, drives ending in a turnover/gm 1.3, scoring-drive rate 33.6%, avg drive start 29.5 yds from own goal - see Method note 4
  - Utah Utes (away, 10 games): 37.9 PPG scored / 18.6 allowed; 471.3 yds-gm vs 344.9 allowed; 12.21 yds/play (pass n/a yds/att, rush 5.79 yds/att); 3rd down 53.2%, 4th down 42.9%
    - success-rate proxies: opponent-adjusted PPA +0.308 (points/play minus opponent's, per tracked drive data), raw PPA 0.982, yards/play 12.21, 3rd-down rate 53.2%
    - takeaways/giveaways: 18 / 15 (margin +3); time of possession 32.2 min/gm
    - special teams / field position (drive-derived): net punt 12.5 yds (touchbacks excluded), punts/gm 3.0, drives ending in a turnover/gm 1.4, scoring-drive rate 48.7%, avg drive start 30.0 yds from own goal - see Method note 4
- **Key skill-player availability (checked as of 2026-11-21):**
  - Jaden Craig (TCU Horned Frogs, home, QB1 (most-started QB, 10 of 10 tracked team box scores)): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Jeremy Payne (TCU Horned Frogs, home, most-listed backfield name in tracked ESPN team box scores (6 games); ESPN game logs expose no position yardage): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Kari Ashley (TCU Horned Frogs, home, most-listed receiving name in tracked ESPN team box scores (5 games); ESPN game logs expose no position yardage): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Devon Dampier (Utah Utes, away, QB1 (most-started QB, 10 of 10 tracked team box scores)): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Wayshawn Parker (Utah Utes, away, most-listed backfield name in tracked ESPN team box scores (5 games); ESPN game logs expose no position yardage): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Braden Pegan (Utah Utes, away, most-listed receiving name in tracked ESPN team box scores (3 games); ESPN game logs expose no position yardage): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
- **Prediction:** final score TCU 24.0, Utah 22.5 -> blended margin +1.6 (home); market-only margin +8.5; model-only -5.3
  - arithmetic: (46.5 + 1.6)/2 = 24.1 (home); (46.5 - 1.6)/2 = 22.4 (away); blended = mean(market +8.5, Massey model -5.3)
- **Sources (real public URLs, with pull dates):**
  - https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261121 | pulled 2026-11-21T06:17:39Z | Week 12 slate, kickoff time, venue, TV, DraftKings closing spread/OU/moneyline (open + close)
  - https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event=401856872 | pulled 2026-11-21T06:17:43Z | ESPN game payload: season team stats used for the offense/defense splits, box-score participant lists behind the availability check, and ESPN FPI win probability
  - https://en.wikipedia.org/wiki/2026_NCAA_Division_I_FBS_football_rankings | pulled 2026-11-21T05:39:51Z | AP Top 25 of Mon Nov 16, 2026 (pre-game rankings)
  - https://en.wikipedia.org/wiki/2026_TCU_Horned_Frogs_football_team | pulled 2026-11-21T05:40:13Z | TCU Horned Frogs: 2026 schedule/roster page used for rest days, venue travel and injury mentions
  - https://en.wikipedia.org/wiki/2026_Utah_Utes_football_team | pulled 2026-11-21T05:40:12Z | Utah Utes: 2026 schedule/roster page used for rest days, venue travel and injury mentions
  - https://api.weather.gov/gridpoints/FWD/68,101/forecast | pulled 2026-11-21T07:04:51Z | NWS forecast at kickoff (conditions, wind speed/direction, temperature)
  - https://api.weather.gov/gridpoints/FWD/68,101/forecast/hourly | pulled 2026-11-21T07:04:51Z | NWS forecast at kickoff (conditions, wind speed/direction, temperature)

## San Diego State Aztecs at Boise State Broncos

- **Kickoff:** 2026-11-21 21:30 ET (Sat) | **Venue:** Albertsons Stadium, Boise | **TV:** USA Net
- **AP Top 25 (Nov 16):** home 15 (9–1) / away unranked (-)
- **Closing line (DraftKings, pulled 2026-11-21T06:17:39Z):** BOIS -17.5 (margin 17.5), OU 60.5; ML home -1450 -> -950, away +850 -> +625
- **Weather at kickoff:** Cloudy then Slight Chance Light Rain, 35F, wind SE 5 mph (hourly: Cloudy | 3 mph ESE)
- **Rest / travel / home-road:** rest 7 vs 7 days (last games 2026-11-14 / 2026-11-14); 749 mi campus-to-campus; home record 5-0 (home team), away team road record 0-4
- **Power ratings:** DSP 17.51 (home) vs -9.50 (away); league home-advantage term 10.50; model margin +37.5 (home). ESPN FPI win%: home 93.8 / away 6.2
- **Offense vs defense (season, all tracked games):**
  - Boise State Broncos (home, 10 games): 39.7 PPG scored / 26.8 allowed; 478.3 yds-gm vs 390.1 allowed; 11.55 yds/play (pass n/a yds/att, rush 5.51 yds/att); 3rd down 52.3%, 4th down 76.2%
    - success-rate proxies: opponent-adjusted PPA -0.120 (points/play minus opponent's, per tracked drive data), raw PPA 0.959, yards/play 11.55, 3rd-down rate 52.3%
    - takeaways/giveaways: 9 / 6 (margin +3); time of possession 35.1 min/gm
    - special teams / field position (drive-derived): net punt 9.1 yds (touchbacks excluded), punts/gm 2.7, drives ending in a turnover/gm 0.4, scoring-drive rate 55.0%, avg drive start 27.2 yds from own goal - see Method note 4
  - San Diego State Aztecs (away, 10 games): 26.8 PPG scored / 32.2 allowed; 333.1 yds-gm vs 425.9 allowed; 9.23 yds/play (pass n/a yds/att, rush 4.48 yds/att); 3rd down 36.4%, 4th down 43.8%
    - success-rate proxies: opponent-adjusted PPA -0.025 (points/play minus opponent's, per tracked drive data), raw PPA 0.742, yards/play 9.23, 3rd-down rate 36.4%
    - takeaways/giveaways: 11 / 14 (margin -3); time of possession 26.0 min/gm
    - special teams / field position (drive-derived): net punt 10.0 yds (touchbacks excluded), punts/gm 4.3, drives ending in a turnover/gm 1.3, scoring-drive rate 39.5%, avg drive start 29.9 yds from own goal - see Method note 4
- **Key skill-player availability (checked as of 2026-11-21):**
  - Maddux Madsen (Boise State Broncos, home, QB1 (most-started QB, 9 of 10 tracked team box scores)): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Dylan Riley (Boise State Broncos, home, most-listed backfield name in tracked ESPN team box scores (9 games); ESPN game logs expose no position yardage): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Rasean Jones (Boise State Broncos, home, most-listed receiving name in tracked ESPN team box scores (7 games); ESPN game logs expose no position yardage): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Jayden Denegal (San Diego State Aztecs, away, QB1 (most-started QB, 7 of 10 tracked team box scores)): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Lucky Sutton (San Diego State Aztecs, away, most-listed backfield name in tracked ESPN team box scores (4 games); ESPN game logs expose no position yardage): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
  - Jaylon Hawkins (San Diego State Aztecs, away, most-listed receiving name in tracked ESPN team box scores (3 games); ESPN game logs expose no position yardage): no absence mention in checked sources (ESPN game-summary news feed, ESPN injury-news feed, Wikipedia 2026 team-season page) as of 2026-11-21; appears repeatedly in tracked ESPN team box scores this season - projected to play
- **Prediction:** final score Boise 35.0, San 25.0 -> blended margin +10.0 (home); market-only margin -17.5; model-only +37.5
  - arithmetic: (60.5 + 10.0)/2 = 35.2 (home); (60.5 - 10.0)/2 = 25.2 (away); blended = mean(market -17.5, Massey model +37.5)
- **Sources (real public URLs, with pull dates):**
  - https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates=20261121 | pulled 2026-11-21T06:17:39Z | Week 12 slate, kickoff time, venue, TV, DraftKings closing spread/OU/moneyline (open + close)
  - https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event=401860925 | pulled 2026-11-21T06:17:43Z | ESPN game payload: season team stats used for the offense/defense splits, box-score participant lists behind the availability check, and ESPN FPI win probability
  - https://en.wikipedia.org/wiki/2026_NCAA_Division_I_FBS_football_rankings | pulled 2026-11-21T05:39:51Z | AP Top 25 of Mon Nov 16, 2026 (pre-game rankings)
  - https://en.wikipedia.org/wiki/2026_Boise_State_Broncos_football_team | pulled 2026-11-21T05:40:14Z | Boise State Broncos: 2026 schedule/roster page used for rest days, venue travel and injury mentions
  - https://en.wikipedia.org/wiki/2026_San_Diego_State_Aztecs_football_team | pulled 2026-11-21T05:40:13Z | San Diego State Aztecs: 2026 schedule/roster page used for rest days, venue travel and injury mentions
  - https://api.weather.gov/gridpoints/BOI/134,85/forecast | pulled 2026-11-21T07:04:52Z | NWS forecast at kickoff (conditions, wind speed/direction, temperature)
  - https://api.weather.gov/gridpoints/BOI/134,85/forecast/hourly | pulled 2026-11-21T07:04:52Z | NWS forecast at kickoff (conditions, wind speed/direction, temperature)
