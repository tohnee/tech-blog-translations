#!/usr/bin/env python3
"""Meta AI 博客 Wayback 全量抓取（div._7g40 段落容器抽取，新模板 article/main 兜底）。"""
import subprocess, time, re, json
from pathlib import Path
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter

ROOT = Path(__file__).resolve().parent
EN = ROOT / 'meta-ai-articles' / 'posts'
EN.mkdir(parents=True, exist_ok=True)
pairs = [l.split() for l in open('/tmp/meta_final_pairs3.txt') if l.strip()]
print('to fetch:', len(pairs), flush=True)
meta_path = ROOT / 'meta-ai-articles' / 'meta.json'
meta = json.loads(meta_path.read_text()) if meta_path.exists() else []
# 只把磁盘上真实存在的文件视为已完成（meta.json 可能残留已清理条目）
done_slugs = {p.stem for p in EN.glob('*.md')}
meta = [m for m in meta if m['slug'] in done_slugs]
MONTHS = {m: i + 1 for i, m in enumerate(
    ['January', 'February', 'March', 'April', 'May', 'June',
     'July', 'August', 'September', 'October', 'November', 'December'])}


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
        # 兜底：h1 标题锚定纯文本抽取（兼容 fb 2021 Next 模板与 meta 2024 模板）
        for el in soup.select('script, style, noscript'):
            el.decompose()
        h1 = soup.find('h1')
        title0 = h1.get_text(strip=True) if h1 else (title or slug)
        text = re.sub(r'\s+', ' ', soup.get_text(' ', strip=True))
        if not date:
            md = re.search(r'(\d{1,2})/(\d{1,2})/(\d{4})', text[:2000])
            if md:
                date = f"{md.group(3)}-{int(md.group(1)):02d}-{int(md.group(2)):02d}"
        pos = text.rfind(title0) if title0 else -1
        if pos == -1 and title:
            pos = text.rfind(title)
        body = text[pos + len(title0):] if pos != -1 else text
        for marker in [' Related', 'Research Areas', 'Careers at Meta', 'About Meta AI', 'Subscribe']:
            p = body.rfind(marker)
            if p > len(body) * 0.5:
                body = body[:p]
                break
        body = body.strip()
        # 去掉开头的分享按钮行
        body = re.sub(r'^\s*(\d{4}[-/]\d{2}[-/]\d{2}|\d{1,2}/\d{1,2}/\d{4})?\s*(Share on Facebook\s*)?(Share on Twitter\s*)?', '', body).strip()
        if len(body) > 200:
            return (title or title0), date, body
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


for i, (url, ts) in enumerate(pairs, 1):
    slug = url.rstrip('/').rsplit('/', 1)[-1]
    if slug in done_slugs:
        continue
    snap = f'https://web.archive.org/web/{ts}id_/{url}'
    html = ''
    for attempt in range(3):
        r = subprocess.run(['curl', '-sSL', '--http1.1', '--max-time', '45', '--compressed',
                            '--socks5-hostname', '127.0.0.1:10808', snap],
                           capture_output=True, text=True)
        html = r.stdout
        if html and len(html) > 3000 and 'Wayback Machine has not archived' not in html:
            break
        time.sleep(10 * (attempt + 1))
    if not html:
        print(f'[{i}] FAILED {slug}', flush=True)
        continue
    title, date, md = extract(html)
    # 登录墙/空壳内容拒绝
    if md and 'Log in or sign up' in md[:600]:
        md = ''
        title = 'login-wall'
    if len(md) > 200 and len(re.sub(r'\s', '', md)) > 400:
        t = (title or slug).replace('"', "'")[:200]
        (EN / f'{slug}.md').write_text(
            f'---\ntitle: "{t}"\ndate: {date or "unknown"}\nsource: {url}\ncrawled: 2026-09-22\n---\n\n{md}\n')
        meta.append({'slug': slug, 'title': t, 'date': date, 'chars': len(md)})
        done_slugs.add(slug)
        if i % 25 == 0 or i <= 3:
            print(f'[{i}/{len(pairs)}] {slug} {date} chars={len(md)} | {t[:40]}', flush=True)
    else:
        print(f'[{i}] EMPTY {slug} (title={title[:40]})', flush=True)
    # 每 50 篇落盘一次 meta（可续传）
    if i % 50 == 0:
        meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=1))
    time.sleep(2.2)

meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=1))
print('DONE:', len(meta), flush=True)
