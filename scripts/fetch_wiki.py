"""Fetch Wikipedia snapshots used by the dossier (rankings, season, team seasons, stadiums).

Writes raw HTML under data/raw/wiki/ and data/venues.csv (stadium coords parsed from
the stadium article infoboxes) + appends to data/manifest.jsonl. No keys required.
"""
import hashlib
import os
import re
import time
import urllib.request

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WDIR = os.path.join(BASE, 'data', 'raw', 'wiki')
UA = {'User-Agent': 'dspaid-bnty0706-research/1.0 (bounty research; contact: dspaid on GitHub)'}

PAGES = [
    '2026_NCAA_Division_I_FBS_football_season',
    '2026_NCAA_Division_I_FBS_football_rankings',
]
TEAMS = [
    'UCLA_Bruins', 'Michigan_Wolverines', 'Arkansas_Razorbacks', 'Texas_Longhorns',
    'Indiana_Hoosiers', 'Washington_Huskies', 'LSU_Tigers', 'Tennessee_Volunteers',
    'Texas_Tech_Red_Raiders', 'Baylor_Bears', 'Texas_A%26M_Aggies', 'Oklahoma_Sooners',
    'Maryland_Terrapins', 'USC_Trojans', 'Virginia_Tech_Hokies', 'Miami_Hurricanes',
    'Arizona_Wildcats', 'Kansas_State_Wildcats', 'Georgia_Bulldogs', 'South_Carolina_Gamecocks',
    'SMU_Mustangs', 'Notre_Dame_Fighting_Irish', 'Kentucky_Wildcats', 'Missouri_Tigers',
    'Pittsburgh_Panthers', 'Louisville_Cardinals', 'Utah_Utes', 'TCU_Horned_Frogs',
    'San_Diego_State_Aztecs', 'Boise_State_Broncos',
]
STADIUMS = {
    'Michigan Stadium': ['Michigan_Stadium'],
    'Darrell K Royal-Texas Memorial Stadium': ['Darrell_K_Royal%E2%80%93Texas_Memorial_Stadium'],
    'Husky Stadium': ['Husky_Stadium', 'Husky_Stadium_(Seattle)'],
    'Neyland Stadium': ['Neyland_Stadium'],
    'McLane Stadium': ['McLane_Stadium'],
    'Memorial Stadium (Norman, OK)': ['Gaylord_Family_Oklahoma_Memorial_Stadium',
                                      'Gaylord_Family_%E2%80%93_Oklahoma_Memorial_Stadium',
                                      'Memorial_Stadium_(Norman,_Oklahoma)'],
    'Los Angeles Memorial Coliseum': ['Los_Angeles_Memorial_Coliseum'],
    'Hard Rock Stadium': ['Hard_Rock_Stadium'],
    'Bill Snyder Family Stadium': ['Bill_Snyder_Family_Football_Stadium', 'Bill_Snyder_Family_Stadium'],
    'Williams-Brice Stadium': ['Williams%E2%80%93Brice_Stadium', 'Williams-Brice_Stadium'],
    'Notre Dame Stadium': ['Notre_Dame_Stadium'],
    'Memorial Stadium (Columbia, MO)': ['Memorial_Stadium_(University_of_Missouri)',
                                        'Memorial_Stadium_(Columbia,_Missouri)'],
    'L&N Federal Credit Union Stadium': ['L%26N_Federal_Credit_Union_Stadium', 'Cardinal_Stadium_(Louisville)'],
    'Amon G. Carter Stadium': ['Amon_G._Carter_Stadium'],
    'Albertsons Stadium': ['Albertsons_Stadium'],
}
# away-campus venues keyed by the actual ESPN home-venue name seen in results.csv,
# each with same-campus fallback wiki slugs (for travel distance between campuses)
STADIUMS2 = {
    'Rose Bowl': ['Rose_Bowl_(stadium)'],
    'Donald W. Reynolds Razorback Stadium': ['Donald_W._Reynolds_Razorback_Stadium'],
    'Memorial Stadium (Bloomington; IN)': ['Memorial_Stadium_(Indiana_University)'],
    'Tiger Stadium (LA)': ['Tiger_Stadium_(LSU)'],
    'Galaxy Stadium': ['Jones_AT%26T_Stadium', 'Galaxy_Stadium'],
    'Kyle Field': ['Kyle_Field'],
    'SECU Stadium': ['SECU_Stadium'],
    'Lane Stadium': ['Lane_Stadium'],
    'Casino Del Sol Stadium': ['Arizona_Stadium', 'Casino_Del_Sol_Stadium'],
    'Sanford Stadium': ['Sanford_Stadium'],
    'Gerald J. Ford Stadium': ['Gerald_J._Ford_Stadium'],
    'Kroger Field': ['Kroger_Field', 'Commonwealth_Stadium'],
    'Acrisure Stadium': ['Heinz_Field', 'Acrisure_Stadium'],
    'Rice-Eccles Stadium': ['Rice%E2%80%93Eccles_Stadium'],
    'Snapdragon Stadium': ['Snapdragon_Stadium'],
    'Gaylord Family Oklahoma Memorial Stadium': ['Gaylord_Family_Oklahoma_Memorial_Stadium',
                                                 'Memorial_Stadium_(Norman,_Oklahoma)'],
}


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


import json  # noqa: E402


def dms_to_dec(txt):
    m = re.match(r'(\d+)[°º]\s*(\d+)′\s*([\d.]+)″\s*([NS])', txt)
    if not m:
        return None
    val = int(m.group(1)) + int(m.group(2)) / 60 + float(m.group(3)) / 3600
    return -val if m.group(4) in 'SW' else val


def parse_coords(html):
    m = re.search(r'"wgCoordinates":\{"lat":([-\d.]+),"lon":([-\d.]+)\}', html)
    if m:
        return round(float(m.group(1)), 4), round(float(m.group(2)), 4)
    m = re.search(r'class="geo-dec"[^>]*>([\d.]+)°N\s+([\d.]+)°W', html)
    if m:
        return round(float(m.group(1)), 4), -round(float(m.group(2)), 4)
    m = re.search(r'class="geo[^"]*"[^>]*>([\d.\-]+);([\d.\-]+)<', html)
    if m:
        return float(m.group(1)), float(m.group(2))
    return None


def main():
    os.makedirs(WDIR, exist_ok=True)
    urls = []
    for p in PAGES + [f'2026_{t}_football_team' for t in TEAMS]:
        urls.append(('wiki_' + re.sub(r'[^A-Za-z0-9_-]', '_', p), f'https://en.wikipedia.org/wiki/{p}'))
    resolved = {}
    for name, cands in list(STADIUMS.items()) + list(STADIUMS2.items()):
        for c in cands:
            url = f'https://en.wikipedia.org/wiki/{c}'
            slug = 'wiki_' + re.sub(r'[^A-Za-z0-9_-]', '_', c)
            path = os.path.join(WDIR, slug + '.html')
            if os.path.exists(path):
                resolved[name] = (c, slug, path)
                break
            try:
                body = fetch(url, tries=2)
            except Exception:
                continue
            log(url, body)
            with open(path, 'wb') as f:
                f.write(body)
            print('got stadium page', name, len(body), flush=True)
            resolved[name] = (c, slug, path)
            break
        if name not in resolved:
            raise SystemExit('no wiki page for stadium ' + name)
    for slug, url in urls:
        path = os.path.join(WDIR, slug + '.html')
        if os.path.exists(path):
            continue
        body = fetch(url)
        log(url, body)
        with open(path, 'wb') as f:
            f.write(body)
        print('got', slug, len(body), flush=True)
    rows = ['stadium,wiki_page,lat,lon']
    for name in list(STADIUMS) + list(STADIUMS2):
        page, slug, path = resolved[name]
        html = open(path, encoding='utf-8', errors='ignore').read()
        cc = parse_coords(html)
        if not cc:
            raise SystemExit('coords parse failed for ' + name)
        rows.append(f'{name.replace(",", ";")},{page.replace("%26", "&")},{cc[0]},{cc[1]}')
    with open(os.path.join(BASE, 'data', 'venues.csv'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(rows) + '\n')
    print('venues written:', len(rows) - 1)


if __name__ == '__main__':
    main()
