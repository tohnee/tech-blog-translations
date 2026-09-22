#!/usr/bin/env python3
"""Meta AI 抓取回收：对首轮 EMPTY/FAILED 的 URL 改用较早 timestamp（facebook 时代老模板）重抓。"""
import subprocess, time, re, json
from pathlib import Path
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter

ROOT = Path(__file__).resolve().parent
EN = ROOT / 'meta-ai-articles' / 'posts'
log = open('/tmp/meta_crawl3.log').read()
empty_slugs = set(re.findall(r'EMPTY ([\w.-]+) ', log))
failed_slugs = set(re.findall(r'FAILED ([\w.-]+)', log))
todo_slugs = (empty_slugs | failed_slugs) - {p.stem for p in EN.glob('*.md')}
print('to retry:', len(todo_slugs), flush=True)

MONTHS = {m: i + 1 for i, m in enumerate(
    ['January', 'February', 'March', 'April', 'May', 'June',
     'July', 'August', 'September', 'October', 'November', 'December'])}


def cdx_timestamps(url):
    q = f"https://web.archive.org/cdx/search/cdx?url={url.rstrip('/')}&output=text&fl=timestamp,statuscode&filter=statuscode:200&limit=100"
    r = subprocess.run(['curl', '-sS', '--max-time', '40', '--socks5-hostname', '127.0.0.1:10808', q],
                       capture_output=True, text=True)
    ts_list = [l.split()[0] for l in r.stdout.splitlines() if l.strip()]
    return sorted(ts_list)


def extract(html):
    soup = BeautifulSoup(html, 'html.parser')
    title = ''
    og = re.search(r'<meta property="og:title" content="([^"]+)"', html)
    if og:
        title = og.group(1)
    date = ''
    m = re.search(r'"datePublished"\s*:\s*"?(\d{4}-\d{2}-\d{2})', html)
    if m:
        date = m.group(1)
    if not date:
        mp = re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),\s+(\d{4})', html)
        if mp:
            date = f"{mp.group(3)}-{MONTHS[mp.group(1)]:02d}-{int(mp.group(2)):02d}"
    sections = soup.select('div._7g40')
    parts = []
    if sections:
        for sec in sections:
            for el in sec.select('script, style'):
                el.decompose()
            parts.append(str(sec))
    else:
        art = soup.find('article') or soup.find('main')
        if art:
            for el in art.select('script, style, nav, footer, aside'):
                el.decompose()
            parts.append(str(art))
    if not parts:
        text = re.sub(r'<script[^>]*>.*?</script>|<style[^>]*>.*?</style>', ' ', html, flags=re.S)
        text = re.sub(r'<[^>]+>', ' ', text)
        t = re.sub(r'\s+', ' ', text).strip()
        s = t.find('Share on Twitter')
        e = t.rfind(' Related')
        if s != -1 and e > s:
            body = t[s + 16:e].strip()
            if len(body) > 200:
                if not date:
                    md = re.search(r'(\d{1,2})/(\d{1,2})/(\d{4})', t[:s])
                    if md:
                        date = f"{md.group(3)}-{int(md.group(1)):02d}-{int(md.group(2)):02d}"
                return title, date, body
        return title, date, ''
    md = ''
    for p in parts:
        md += MarkdownConverter(heading_style='ATX', bullets='-').convert_soup(
            BeautifulSoup(p, 'html.parser')) + '\n\n'
    md = md.replace('\u00a0', ' ').replace('\\_', '_').replace('\\*', '*').replace('\\[', '[').replace('\\]', ']')
    md = re.sub(r'\n{3,}', '\n\n', md).strip()
    md = re.sub(r'^\s*(Share|Tweet|Share on Facebook.*)\s*$', '', md, flags=re.M)
    md = re.sub(r'!\[\]\(https://scontent[^)]*\)', '', md)
    return title, date, md.strip()


pairs = {l.split()[0].rstrip('/').rsplit('/', 1)[-1]: l.split()[0]
         for l in open('/tmp/meta_pairs.txt') if l.strip()}
meta_path = ROOT / 'meta-ai-articles' / 'meta.json'
meta = json.loads(meta_path.read_text()) if meta_path.exists() else []
meta_idx = {m['slug'] for m in meta}

for i, slug in enumerate(sorted(todo_slugs), 1):
    url = pairs.get(slug)
    if not url:
        continue
    ts_list = cdx_timestamps(url)
    # 优先 2019-2023 老快照（facebook 模板 _7g40），否则全部尝试
    old = [t for t in ts_list if '2019' <= t[:4] <= '2023'] or ts_list
    got = False
    for ts in old[:3]:
        snap = f'https://web.archive.org/web/{ts}id_/{url}'
        r = subprocess.run(['curl', '-sSL', '--http1.1', '--max-time', '45', '--compressed',
                            '--socks5-hostname', '127.0.0.1:10808', snap],
                           capture_output=True, text=True)
        html = r.stdout
        if not html or len(html) < 3000 or 'Wayback Machine has not archived' in html:
            time.sleep(6)
            continue
        title, date, md = extract(html)
        if len(md) > 200:
            t = (title or slug).replace('"', "'")[:200]
            (EN / f'{slug}.md').write_text(
                f'---\ntitle: "{t}"\ndate: {date or "unknown"}\nsource: {url}\ncrawled: 2026-09-22\n---\n\n{md}\n')
            if slug not in meta_idx:
                meta.append({'slug': slug, 'title': t, 'date': date, 'chars': len(md)})
                meta_idx.add(slug)
            print(f'[{i}/{len(todo_slugs)}] {slug} via {ts[:8]} {date} chars={len(md)}', flush=True)
            got = True
            break
        time.sleep(3)
    if not got:
        print(f'[{i}] STILL-EMPTY {slug}', flush=True)
    if i % 25 == 0:
        meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=1))
    time.sleep(2)

meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=1))
print('RETRY DONE. total meta:', len(meta), flush=True)
