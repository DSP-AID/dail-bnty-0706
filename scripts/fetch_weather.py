"""Fetch NOAA/NWS game-day forecasts (wind!) for each slate venue at kickoff.

Reads data/venues.csv + data/slate_games.json; writes raw NWS JSON under
data/raw/nws/ and extracted data/weather.json. api.weather.gov needs only a
User-Agent header, no key.
"""
import csv
import hashlib
import json
import os
import time
import urllib.request
from datetime import datetime, timedelta, timezone

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NWS = os.path.join(BASE, 'data', 'raw', 'nws')
UA = {'User-Agent': 'dspaid-bnty0706-research/1.0 (bounty research; contact: dspaid on GitHub)'}


def fetch(url, tries=4):
    for i in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read()
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(2 * (i + 1))


def log(url, body):
    with open(os.path.join(BASE, 'data', 'manifest.jsonl'), 'a', encoding='utf-8') as f:
        f.write(json.dumps({'url': url, 'fetched_at_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                            'sha256': hashlib.sha256(body).hexdigest(), 'bytes': len(body)}) + '\n')


def main():
    os.makedirs(NWS, exist_ok=True)
    venues = {}
    with open(os.path.join(BASE, 'data', 'venues.csv'), encoding='utf-8') as f:
        for row in csv.DictReader(f):
            venues[row['stadium']] = (float(row['lat']), float(row['lon']))
    games = json.load(open(os.path.join(BASE, 'data', 'slate_games.json'), encoding='utf-8'))
    out = {}
    for g in games:
        vn = g['venue']['fullName']
        # ESPN venue name -> our venues.csv key mapping (name differences handled here)
        alias = {
            'DKR-Texas Memorial Stadium': 'Darrell K Royal-Texas Memorial Stadium',
            'Memorial Stadium (Norman, OK)': 'Memorial Stadium (Norman, OK)',
            'Memorial Stadium': 'Memorial Stadium (Columbia, MO)',
            'Bill Snyder Family Stadium': 'Bill Snyder Family Stadium',
        }
        key = alias.get(vn, vn)
        if key not in venues:
            key = next((k for k in venues if k.split('(')[0].strip() in vn or vn in k), None)
        lat, lon = venues[key]
        kickoff = datetime.fromisoformat(g['date_utc'].replace('Z', '+00:00'))
        pbody = None
        for dlat in (0.0, 0.02, -0.02, 0.05):  # NWS gridpoints can 404 at exact stadium coords
            try:
                purl = f'https://api.weather.gov/points/{round(lat + dlat, 4)},{round(lon, 4)}'
                pbody = fetch(purl, tries=1)
                break
            except urllib.error.HTTPError:
                continue
        if pbody is None:
            raise RuntimeError(f'no NWS gridpoint for {key}')
        log(purl, pbody)
        props = json.loads(pbody)['properties']
        furl = props['forecast']
        fbody = fetch(furl)
        log(furl, fbody)
        hurl = props['forecastHourly']
        hbody = fetch(hurl)
        log(hurl, hbody)
        with open(os.path.join(NWS, key.replace(' ', '_').replace(',', '') + '.json'), 'wb') as f:
            f.write(fbody)
        periods = json.loads(fbody)['properties']['periods']
        hperiods = json.loads(hbody)['properties']['periods']
        # covering 6h period and nearest hourly period to kickoff
        cov = None
        for p in periods:
            st = datetime.fromisoformat(p['startTime'])
            en = datetime.fromisoformat(p['endTime'])
            if st <= kickoff <= en:
                cov = p
                break
        near = min(hperiods, key=lambda p: abs(datetime.fromisoformat(p['startTime']) - kickoff))
        out[g['event_id']] = {
            'stadium': vn, 'kickoff_utc': g['date_utc'], 'lat': lat, 'lon': lon,
            'points_url': purl, 'forecast_url': furl, 'hourly_url': hurl,
            'covering_period': cov, 'hourly_at_kickoff': near,
        }
        print('weather ok', vn, flush=True)
    with open(os.path.join(BASE, 'data', 'weather.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=1)
    print('DONE weather for', len(out), 'venues')


if __name__ == '__main__':
    main()
