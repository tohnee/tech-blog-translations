#!/usr/bin/env python3
"""SemiAnalysis src/*.json → posts/*.md 英文归档转换器。

处理 Substack body_html 的特有结构：
- captioned-image-container / image-gallery-embed → Markdown 图片 + 斜体图注；
  图片 URL 从 substackcdn 签名链接中解出原始 S3 直链（稳定不签名）；
- digest-post-embed（站内文章卡片）→ 链接行；native-video-embed / iframe → 链接行；
- subscription-widget / button / svg 等界面元素 → 删除。
付费文（audience=only_paid）正文在付费墙处截断，文件头与正文均显式标注。
"""
import html as htmllib
import json
import re
import sys
import urllib.parse
from pathlib import Path

from bs4 import BeautifulSoup
from markdownify import MarkdownConverter

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "semianalysis-articles" / "src"
POSTS = ROOT / "semianalysis-articles" / "posts"
POSTS.mkdir(parents=True, exist_ok=True)


def clean_image_url(url: str | None) -> str:
    """substackcdn image/fetch/<签名参数>/<编码后的S3地址> → 原始 S3 直链。"""
    if not url:
        return ""
    if "/image/fetch/" in url:
        tail = url.split("/image/fetch/", 1)[1]
        # 形如  $s_!TOKEN!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2F...
        m = re.search(r"(https%3A%2F%2F|https://)", tail)
        if m:
            encoded = tail[m.start():]
            decoded = urllib.parse.unquote(encoded)
            return decoded.split()[0]
    return url


def replace_image_container(node) -> None:
    """captioned-image-container → <p>![alt](url)</p><p><em>caption</em></p>"""
    link = node.select_one("a.image-link")
    img = node.select_one("img")
    url = clean_image_url(link.get("href") if link else None) or (img.get("src") if img else "")
    alt = (img.get("alt") or "").strip() if img else ""
    cap_el = node.select_one(".image-caption")
    cap = cap_el.get_text(" ", strip=True) if cap_el else ""
    md = f"\n\n![{alt}]({url})\n\n"
    if cap:
        md += f"*{cap}*\n\n"
    node.replace_with(BeautifulSoup(md, "html.parser"))


def preprocess(soup: BeautifulSoup) -> None:
    # 1) 订阅挂件等界面元素
    for sel in [
        "div.subscription-widget",
        "div.subscription-widget-wrap",
        "div.paywall-title-section",
        "button",
        "svg",
        "style",
        "script",
    ]:
        for el in soup.select(sel):
            el.decompose()

    # 2) 图片容器
    for node in soup.select("div.captioned-image-container"):
        parent = node.find_parent("div.image-gallery-embed")
        if parent is not None:
            continue  # 画廊整体处理
        replace_image_container(node)
    for gallery in soup.select("div.image-gallery-embed"):
        parts = ["\n\n"]
        for img in gallery.select("img"):
            url = clean_image_url(img.get("src"))
            if url:
                parts.append(f"![{(img.get('alt') or '').strip()}]({url})\n\n")
        cap_el = gallery.select_one(".image-caption, .gallery-caption")
        if cap_el:
            parts.append(f"*{cap_el.get_text(' ', strip=True)}*\n\n")
        gallery.replace_with(BeautifulSoup("".join(parts), "html.parser"))

    # 3) 站内文章卡片 digest-post-embed → 链接
    for node in soup.select("div.digest-post-embed, .digest-post-below-title"):
        a = node.select_one("a[href]")
        t = node.select_one(".digest-post-title, h1, h2, h3")
        if a:
            title = t.get_text(" ", strip=True) if t else a.get_text(" ", strip=True)
            node.replace_with(BeautifulSoup(f'<p>📎 <a href="{a["href"]}">{htmllib.escape(title)}</a></p>', "html.parser"))
        else:
            node.decompose()
    # 容器残留清理（同名包装 div）
    for node in soup.select("div.digest-post-embed-wrap, div.digest-publication-wrap"):
        node.unwrap()

    # 4) 视频与 iframe
    for node in soup.select("div.native-video-embed"):
        video = node.select_one("video")
        src = (video.get("src") if video else "") or ""
        poster = video.get("poster") if video else ""
        if src:
            node.replace_with(BeautifulSoup(f'<p>🎬 <a href="{htmllib.escape(src)}">[视频]</a></p>', "html.parser"))
        elif poster:
            node.replace_with(BeautifulSoup(f'<p><img src="{htmllib.escape(poster)}" alt="video poster"/></p>', "html.parser"))
        else:
            node.decompose()
    for node in soup.select("iframe"):
        src = node.get("src") or ""
        if src:
            node.replace_with(BeautifulSoup(f'<p>🔗 <a href="{htmllib.escape(src)}">[嵌入内容]</a></p>', "html.parser"))
        else:
            node.decompose()

    # 5) 展开_soup 其余纯包装 div/span
    for el in soup.find_all(["div", "span"]):
        el.unwrap()


class MD(MarkdownConverter):
    def convert_figcaption(self, el, text):  # 图注已在容器处理时转写，兜底斜体
        return f"*{text.strip()}*\n\n" if text.strip() else ""


def html_to_md(body_html: str) -> str:
    soup = BeautifulSoup(body_html or "", "html.parser")
    preprocess(soup)
    md = MD(heading_style="ATX", bullets="-", strong="**", em="*").convert_soup(soup)
    md = md.replace("\u00a0", " ")
    # 还原 markdownify 对 URL/图注中 _ * [ ] 的过度转义
    md = md.replace("\\_", "_").replace("\\*", "*").replace("\\[", "[").replace("\\]", "]")
    md = re.sub(r"\n{3,}", "\n\n", md)
    md = re.sub(r"[ \t]+\n", "\n", md)
    return md.strip()


def main() -> None:
    index = {p["slug"]: p for p in json.load(open(SRC / "_index.json"))}
    files = [f for f in sorted(SRC.glob("*.json")) if f.name != "_index.json"]
    meta = []
    for f in files:
        d = json.load(open(f))
        slug = d["slug"]
        lst = index.get(slug, {})
        audience = d.get("audience") or lst.get("audience") or "everyone"
        date = (d.get("post_date") or lst.get("post_date") or "")[:10]
        title = d.get("title") or slug
        subtitle = d.get("subtitle") or ""
        url = d.get("canonical_url") or f"https://newsletter.semianalysis.com/p/{slug}"
        authors = []
        for b in lst.get("publishedBylines") or []:
            name = b.get("name")
            if name:
                authors.append(name)
        tags = [t.get("name") for t in (lst.get("postTags") or []) if t.get("name")]
        md = html_to_md(d.get("body_html") or "")
        paywalled = audience == "only_paid"
        fm = [
            "---",
            f'title: "{title.replace(chr(34), chr(39))}"',
            f'subtitle: "{subtitle.replace(chr(34), chr(39))}"' if subtitle else None,
            f"date: {date}",
            f"source: {url}",
            "crawled: 2026-09-15",
            f"authors: {json.dumps(authors, ensure_ascii=False)}",
            f"tags: {json.dumps(tags, ensure_ascii=False)}",
            f"audience: {audience}",
            f"paywalled: {str(paywalled).lower()}",
            "---",
        ]
        head = "\n".join(x for x in fm if x) + "\n\n"
        body_md = f"# {title}\n\n"
        if subtitle:
            body_md += f"**{subtitle}**\n\n"
        if paywalled and md:
            body_md += (
                "> ⚠️ 付费订阅文章：以下正文为公开可见的预览部分，在付费墙处截断，"
                "并非全文。/ Paid post: only the publicly visible preview portion "
                "is archived; the body is truncated at the paywall.\n\n"
            )
        if not md:
            body_md += (
                f"> 本文无公开正文（音频/播客或纯付费内容）。/ No public body "
                f"(podcast/audio-only or fully paywalled)."
                + (f"\n> 音频：{d.get('podcast_url')}" if d.get("podcast_url") else "")
                + "\n"
            )
        out = head + body_md + md + "\n"
        (POSTS / f"{slug}.md").write_text(out)
        meta.append(
            {
                "slug": slug,
                "title": title,
                "subtitle": subtitle,
                "date": date,
                "url": url,
                "authors": authors,
                "tags": tags,
                "audience": audience,
                "paywalled": paywalled,
                "chars": len(md),
            }
        )
    (ROOT / "semianalysis-articles" / "meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=1)
    )
    n_paid = sum(1 for m in meta if m["paywalled"])
    print(f"converted {len(meta)} posts ({n_paid} paywalled previews, {len(meta)-n_paid} full)")


if __name__ == "__main__":
    sys.exit(main())
