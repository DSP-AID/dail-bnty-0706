# Week 12 primetime CFB dossier - Saturday, November 21, 2026

DAiL bounty `bnty_0706`. Pre-game scouting dossier for **all 15 listed Top-25 games** on the
Week 12 college-football slate, with the full data pipeline that produced it.

Read [`DOSSIER.md`](DOSSIER.md) for the deliverable. Everything below runs offline on a clean
machine: no network, no API keys - the dataset it needs is in `data/`.

## Run it

```bash
python scripts/build_data.py       # data/ -> data/analysis/* (ratings, per-game analysis)
python scripts/render_dossier.py   # data/analysis/* -> DOSSIER.md
python scripts/verify.py           # offline checks: re-derives ratings + all 15 predictions,
                                   # checks citations and sha256 of retained raw payloads
```

Python 3.10+, standard library only. `scripts/fetch_*.py` are the collectors that built `data/`
(they do need network); re-running them today would pull live in-progress scores, so the shipped
`data/` snapshot is the frozen input of record - every fetch is logged in `data/manifest.jsonl`
with URL, `fetched_at_utc` and sha256.

## Layout

| Path | What it is |
|---|---|
| `DOSSIER.md` | The deliverable: slate table, method, then one section per game (rankings, venue/broadcast, opening + closing DraftKings spread/OU/moneyline with pull time, two power ratings, ESPN FPI, offense vs defense season splits, rest days, travel miles, kickoff weather, key-player availability, predicted score shown as arithmetic, and 7 cited public source URLs with pull dates). |
| `data/slate_games.json` | The 15 games: ESPN event ids, kickoff times, venue, TV, DraftKings open/close spread + OU + moneyline (pulled 2026-11-21T06:17Z, pre-game). |
| `data/results.csv` | Every completed 2026 FBS game tracked (scores, dates, venues) - the input the ratings are solved from. |
| `data/team_games.csv` | One row per (game, team): yards, plays, turnovers, 3rd/4th-down conversion, possession minutes, and the box-score QB/RB/WR names used for availability. |
| `data/team_season.json` -> `data/analysis/*` | Season aggregates plus derived metrics: SRS/Massey ratings (`analysis/ratings.csv`, `metrics.json`), opponent-adjusted PPA, drive/special-teams profiles, AP poll (`analysis/ap_poll.json`), and the per-game analysis layer `analysis/games.json` that the dossier renders. |
| `data/weather.json` | NWS `api.weather.gov` forecast at each kickoff site (conditions, wind, temperature) plus the public forecast URLs. |
| `data/venues.csv` | Stadium coordinates + Wikipedia page used for travel miles. |
| `data/manifest.jsonl` | 1041 fetch records: URL, pull time, sha256 - the provenance record behind every citation. |
| `data/raw/today_<event>.json` | The retained pre-game ESPN payload per slate game (byte-for-byte, hash-checked by `verify.py`). |
| `data/raw/wiki/`, `raw/scoreboards/`, `raw/nws/`, `raw/summaries/` | Retained raw pages/feeds behind the poll, rankings, schedules and weather. |

## Method (short version)

Full detail is in `DOSSIER.md` -> Method. Two ratings are reported per team: a least-squares
margin rating over all 752 tracked games (`scripts/compute_metrics.py`, league-wide home advantage
+4.72 pts) and the slate-fitted Massey iteration used for the margin (home advantage +10.503 pts,
shown alongside the league figure for sensitivity). The prediction blends the market and the model:
`blended = mean(market margin, model margin)`, then `(OU +/- blended)/2` for each team's points -
that arithmetic is printed for every game so any number can be recomputed by hand.

## Known limits (stated, not papered over)

- **No net punting.** ESPN per-game team stats carry no punting at all (`punts` = 0 in all 520
  `team_games.csv` rows) and the public punting endpoints return 404, so the special-teams numbers
  are *derived from drive data* instead: `data/raw/drive_slices/` holds the possession-level drive
  arrays (start field position, plays, yards, outcome) from each game's ESPN summary feed - a
  trimmed extract, so its bytes are not the full manifest payload and it is not hash-checked. From
  it come `net_punt_drive`, `punt_pg`, `drive_to_pg`, `scoring_drive_pct` and average drive start.
- **Skill-player yardage.** The ESPN team game log names one featured ball-carrier and receiver per
  week but exposes no position yardage, so RB/WR names are reported as "most-listed name in the
  tracked box scores (N games)", not as season yardage leaders.
- **Availability is inferred, not official.** No public injury report feed was available; each named
  player was checked against the ESPN game-summary payload, the ESPN news/injury feeds and the team's
  Wikipedia 2026 page. Absences found are shown as `FLAGGED` with the URL; anything else is stated as
  "no absence mention in checked sources", which is weaker than an official clearance.
- Some raw payloads referenced by `manifest.jsonl` were pruned to keep the repo small; only the
  files listed above ship, and `verify.py` hash-checks just those.
