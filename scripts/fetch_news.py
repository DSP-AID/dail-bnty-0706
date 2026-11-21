"""Pull ESPN college-football news feeds and extract player-availability mentions.

Writes data/news.jsonl (all articles with headline/url/date) and
data/injury_news.csv (articles mentioning a slate team + availability keywords).
No keys required.
"""
import json
import os
import re
import time
import urllib.request

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = {'User-Agent': 'dspaid-bnty0706-research/1.0 (bounty research; contact: dspaid on GitHub)'}
FEEDS = [
    'https://site.api.espn.com/apis/site/v2/sports/football/college-football/news?lang=en&region=us&count=100',
    'https://site.api.espn.com/apis/site/v2/league/ncaaf/news?lang=en&region=us&count=100',
]
TEAMS = ['UCLA', 'Michigan', 'Arkansas', 'Texas', 'Indiana', 'Washington', 'LSU', 'Tennessee',
         'Texas Tech', 'Baylor', 'Texas A&M', 'Oklahoma', 'Maryland', 'USC', 'Virginia Tech',
         'Miami', 'Arizona', 'Kansas State', 'Georgia', 'South Carolina', 'SMU', 'Notre Dame',
         'Kentucky', 'Missouri', 'Pitt', 'Louisville', 'Utah', 'TCU', 'San Diego State', 'Boise State']
INJ_WORDS = r'injur|out for|sidelined|questionable|doubtful|day-to-day|availability|status|scratch|withdraw|redshirt|return from'


def fetch(url, tries=4):
    for i in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read()
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(2 * (i + 1))


def main():
    seen = set()
    arts = []
    for u in FEEDS:
        try:
            body = fetch(u)
        except Exception as e:
            print('feed fail', u, e, flush=True)
            continue
        with open(os.path.join(BASE, 'data', 'manifest.jsonl'), 'a', encoding='utf-8') as f:
            f.write(json.dumps({'url': u, 'fetched_at_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                                'sha256': hashlib.sha256(body).hexdigest(), 'bytes': len(body)}) + '\n')
        d = json.loads(body)

        def walk(o):
            if isinstance(o, dict):
                if o.get('headline') and (o.get('links') or o.get('web')):
                    lnk = o.get('links')
                    href = None
                    if isinstance(lnk, list) and lnk:
                        href = lnk[0].get('href')
                    elif isinstance(lnk, dict):
                        href = (lnk.get('web') or {}).get('href') or lnk.get('href')
                    key = (o['headline'], href)
                    if key not in seen:
                        seen.add(key)
                        arts.append({'headline': o['headline'], 'url': href,
                                     'date': str(o.get('publishedDate', ''))[:10]})
                for v in o.values():
                    walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
        walk(d)
    # also fold in the news blocks from the 15 game summaries (already downloaded)
    for fn in os.listdir(os.path.join(BASE, 'data', 'raw')):
        if fn.startswith('today_') and fn.endswith('.json'):
            s = json.load(open(os.path.join(BASE, 'data', 'raw', fn), encoding='utf-8'))
            walk(s.get('news', {}))
    with open(os.path.join(BASE, 'data', 'news.jsonl'), 'w', encoding='utf-8') as f:
        for a in arts:
            f.write(json.dumps(a) + '\n')
    inj_rows = ['team,headline,url,date']
    for a in arts:
        h = a['headline'] or ''
        if not re.search(INJ_WORDS, h, re.I):
            continue
        for t in TEAMS:
            if re.search(r'\b' + re.escape(t) + r'\b', h):
                inj_rows.append(f'{t},"{h.replace(chr(34), chr(39))}","{a["url"]}",{a["date"]}')
                break
    with open(os.path.join(BASE, 'data', 'injury_news.csv'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(inj_rows) + '\n')
    print('DONE articles:', len(arts), 'injury mentions:', len(inj_rows) - 1)


import hashlib  # noqa: E402

if __name__ == '__main__':
    main()
