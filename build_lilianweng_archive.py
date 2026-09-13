#!/usr/bin/env python3
"""Build the lilianweng-articles archive.

Sources:
  - 37 old posts (<= 2022-02-20): real markdown recovered from lil-log git
    history (lilianweng-md-real/_posts/), Liquid tags resolved against the
    live deployed site structure (lilianweng.github.io/posts/<slug>/).
  - 15 new posts (>= 2022-04-15) + FAQ page: converted from deployed HTML
    (lilianweng-src/posts/<slug>/index.html), math preserved as raw LaTeX.
"""
import json
import re
import html as H
from pathlib import Path

from bs4 import BeautifulSoup
from markdownify import MarkdownConverter

ROOT = Path(__file__).parent
SITE = ROOT / "lilianweng-src"           # deployed HTML repo
MD_REAL = ROOT / "lilianweng-md-real"    # real md from git history
OUT = ROOT / "lilianweng-articles"
BASE = "https://lilianweng.github.io"
CRAWLED = "2026-09-08"

MD_TO_SLUG = {
    "2017-06-21-an-overview-of-deep-learning.md": "2017-06-21-overview",
    "2017-07-08-predict-stock-prices-using-RNN-part-1.md": "2017-07-08-stock-rnn-part-1",
    "2017-07-22-predict-stock-prices-using-RNN-part-2.md": "2017-07-22-stock-rnn-part-2",
    "2017-08-01-how-to-explain-the-prediction-of-a-machine-learning-model.md": "2017-08-01-interpretation",
    "2017-08-20-from-GAN-to-WGAN.md": "2017-08-20-gan",
    "2017-09-28-anatomize-deep-learning-with-information-theory.md": "2017-09-28-information-bottleneck",
    "2017-10-15-learning-word-embedding.md": "2017-10-15-word-embedding",
    "2017-10-29-object-recognition-for-dummies-part-1.md": "2017-10-29-object-recognition-part-1",
    "2017-12-15-object-recognition-for-dummies-part-2.md": "2017-12-15-object-recognition-part-2",
    "2017-12-31-object-recognition-for-dummies-part-3.md": "2017-12-31-object-recognition-part-3",
    "2018-01-23-the-multi-armed-bandit-problem-and-its-solutions.md": "2018-01-23-multi-armed-bandit",
    "2018-02-19-a-long-peek-into-reinforcement-learning.md": "2018-02-19-rl-overview",
    "2018-04-08-policy-gradient-algorithms.md": "2018-04-08-policy-gradient",
    "2018-05-05-implementing-deep-reinforcement-learning-models.md": "2018-05-05-drl-implementation",
    "2018-06-24-attention-attention.md": "2018-06-24-attention",
    "2018-08-12-from-autoencoder-to-beta-vae.md": "2018-08-12-vae",
    "2018-10-13-flow-based-deep-generative-models.md": "2018-10-13-flow-models",
    "2018-11-30-meta-learning.md": "2018-11-30-meta-learning",
    "2018-12-27-object-detection-part-4.md": "2018-12-27-object-recognition-part-4",
    "2019-01-31-generalized-language-models.md": "2019-01-31-lm",
    "2019-03-14-are-deep-neural-networks-dramatically-overfitted.md": "2019-03-14-overfit",
    "2019-05-05-domain-randomization.md": "2019-05-05-domain-randomization",
    "2019-06-23-meta-reinforcement-learning.md": "2019-06-23-meta-rl",
    "2019-09-05-evolution-strategies.md": "2019-09-05-evolution-strategies",
    "2019-11-10-self-supervised-learning.md": "2019-11-10-self-supervised",
    "2020-01-29-curriculum-for-reinforcement-learning.md": "2020-01-29-curriculum-rl",
    "2020-04-07-the-transformer-family.md": "2020-04-07-the-transformer-family",
    "2020-06-07-exploration-strategies-in-deep-reinforcement-learning.md": "2020-06-07-exploration-drl",
    "2020-08-06-neural-architecture-search.md": "2020-08-06-nas",
    "2020-10-29-open-domain-question-answering.md": "2020-10-29-odqa",
    "2021-01-02-controllable-neural-text-generation.md": "2021-01-02-controllable-text-generation",
    "2021-03-21-reducing-toxicity-in-language-models.md": "2021-03-21-lm-toxicity",
    "2021-05-31-contrastive-representation-learning.md": "2021-05-31-contrastive",
    "2021-07-11-diffusion-models.md": "2021-07-11-diffusion-models",
    "2021-09-25-train-large-neural-networks.md": "2021-09-25-train-large",
    "2021-12-05-semi-supervised-learning.md": "2021-12-05-semi-supervised",
    "2022-02-20-active-learning.md": "2022-02-20-active-learning",
}
DATE_TO_SLUG = {fn[:10]: slug for fn, slug in MD_TO_SLUG.items()}
NEW_POSTS = [
    "2022-04-15-data-gen", "2022-06-09-vlm", "2022-09-08-ntk",
    "2023-01-10-inference-optimization", "2023-01-27-the-transformer-family-v2",
    "2023-03-15-prompt-engineering", "2023-06-23-agent", "2023-10-25-adv-attack-llm",
    "2024-02-05-human-data-quality", "2024-04-12-diffusion-video",
    "2024-07-07-hallucination", "2024-11-28-reward-hacking", "2025-05-01-thinking",
    "2026-06-24-scaling-laws", "2026-07-04-harness",
]

IMG_INDEX = {}
for _d in sorted((SITE / "posts").iterdir()):
    if _d.is_dir():
        for _f in _d.iterdir():
            if _f.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}:
                IMG_INDEX.setdefault(_f.name, []).append(_d.name)


def img_url(src, slug):
    """Resolve an image reference (absolute, relative or bare) to live-site URL."""
    if src.startswith(("http://", "https://", "data:")):
        return src
    basename = src.split("/")[-1].split("?")[0]
    dirs = IMG_INDEX.get(basename, [])
    if slug in dirs:
        return f"{BASE}/posts/{slug}/{basename}"
    if dirs:
        return f"{BASE}/posts/{dirs[0]}/{basename}"
    return f"{BASE}/assets/images/{basename}"


report = []


def write_post(slug, title, date, tags, body, src):
    lines = ["---", f'title: "{title}"']
    if date:
        lines.append(f"date: {date}")
    if tags:
        lines.append(f"tags: [{tags}]")
    lines.append(f"source: {BASE}/posts/{slug}/" if src == "post" else f"source: {BASE}/faq/")
    lines.append(f"crawled: {CRAWLED}")
    lines.append("---")
    body = body.strip() + "\n"
    (OUT / "posts").mkdir(parents=True, exist_ok=True)
    path = OUT / "posts" / f"{slug}.md"
    path.write_text("\n".join(lines) + "\n\n" + body, encoding="utf-8")
    report.append({"slug": slug, "title": title, "date": date,
                   "words": len(body.split()), "file": f"posts/{slug}.md"})


# ------------------------------------------------------------ old posts
def build_old_posts():
    fence_open = "```LANG```"  # marker replaced after regex
    for fn, slug in sorted(MD_TO_SLUG.items()):
        text = (MD_REAL / "_posts" / fn).read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
        fm_raw, body = m.group(1), m.group(2)
        title, date, tags = "", "", ""
        for line in fm_raw.splitlines():
            if line.startswith("title:"):
                title = line[6:].strip().strip('"')
            elif line.startswith("date:"):
                date = line[5:].strip()[:10]
            elif line.startswith("tags:"):
                tags = line[5:].strip()

        def repl_post_url(match):
            d = match.group(1)[:10]
            sl = DATE_TO_SLUG.get(d, match.group(1))
            return f"{BASE}/posts/{sl}/"

        body = re.sub(r"\{%\s*post_url\s+([^\s%]+)\s*%\}", repl_post_url, body)
        body = re.sub(
            r"\{\{\s*'/assets/images/([^']+)'\s*\|\s*relative_url\s*\}\}",
            lambda mo: img_url(mo.group(1), slug), body)
        # /assets/data/x.jpg refs: files migrated into post dirs as .png
        body = re.sub(
            r"\{\{\s*'/assets/data/([^']+?)\.jpg'\s*\|\s*relative_url\s*\}\}",
            lambda mo: img_url(mo.group(1) + ".png", slug), body)
        # combined baseurl+post_url first (avoid double prefix), then leftovers
        body = re.sub(r"\{\{\s*site\.baseurl\s*\}\}\s*(https?://[^)\s]+)", r"\1", body)
        body = re.sub(r"\{\{\s*site\.baseurl\s*\}\}", BASE, body)

        def repl_hl(match):
            lang = match.group(1)
            return "\n```" + lang + "\n" if lang else "\n```\n"

        body = re.sub(r"\{%\s*highlight\s+(\w+)(?:\s+linenos)?\s*%\}", repl_hl, body)
        body = body.replace("{% endhighlight %}", "```")
        body = body.replace("<!--more-->\n", "").replace("<!--more-->", "")
        # kramdown markers: strip attribute lists, drop auto-TOC blocks
        body = re.sub(r"^\* TOC\n^\{:toc\}\n?", "", body, flags=re.M)
        body = re.sub(r"\{:[^}\n]*\}", "", body)
        # images referenced as plain /assets/... or relative paths
        body = re.sub(
            r"(\]\()(?!https?://|/posts/|#|mailto)(/?assets/images/[^)\s]+)\)",
            lambda mo: f"]({img_url(mo.group(2), slug)})", body)
        write_post(slug, title, date, tags, body, "post")


# ------------------------------------------------------------ new posts
MATH_PH = []       # (placeholder, content)
CODE_PH = []       # (placeholder, fenced-markdown block)


def fence_pre(pre_html):
    """Turn a stashed <pre> block into a fenced markdown code block."""
    inner = re.search(r"<pre[^>]*>(.*)</pre>", pre_html, re.S)
    inner = inner.group(1) if inner else pre_html
    lang = ""
    m = re.search(r'<code[^>]*class="language-([^"]+)"', inner)
    if m:
        lang = m.group(1)
    text = re.sub(r"</?code[^>]*>", "", inner)
    text = H.unescape(text)
    return f"```{lang}\n{text.strip()}\n```"


def stash(html_str, pattern, bucket, transform=None):
    def _stash(match):
        content = match.group(0)
        if transform:
            content = transform(content)
        key = f"XXPH{len(bucket)}PHXX"
        bucket.append((key, content))
        return key
    return re.sub(pattern, _stash, html_str, flags=re.S)


def convert_new(slug, content_div_html):
    html_str = content_div_html
    # protect <pre> blocks first (may contain $)
    html_str = re.sub(
        r"<pre[^>]*>.*?</pre>",
        lambda mo: (CODE_PH.append((f"XXCODE{len(CODE_PH)}XX", fence_pre(mo.group(0)))),
                    f"XXCODE{len(CODE_PH)-1}XX")[1],
        html_str, flags=re.S)
    # protect display math $$...$$ and inline $...$; entities unescaped inside
    html_str = stash(html_str, r"\$\$.+?\$\$", MATH_PH, H.unescape)
    html_str = stash(html_str, r"\$[^$\n]{1,400}?\$", MATH_PH, H.unescape)

    soup = BeautifulSoup(html_str, "html.parser")
    # drop heading anchor links ("#") injected by the site generator
    for a in soup.find_all("a", class_="anchor"):
        a.decompose()

    # images: rewrite src to absolute
    for img in soup.find_all("img"):
        img["src"] = img_url(img.get("src", ""), slug)
        if not img.get("alt"):
            img["alt"] = ""
    # figure -> <p><img></p> + italic caption paragraph (keep the image!)
    for fig in soup.find_all("figure"):
        cap = fig.find("figcaption")
        cap_text = cap.get_text(" ", strip=True) if cap else ""
        if cap:
            cap.extract()
        img_html = "".join(str(c) for c in fig.contents)
        block = f'<p>{img_html}</p>'
        if cap_text:
            block += f'<p>FIGCAPSTART{cap_text}FIGCAPEND</p>'
        fig.replace_with(BeautifulSoup(block, "html.parser"))
    # footnote refs <sup><a class="footnote-ref">N</a></sup> -> [^N]
    for sup in soup.find_all("sup"):
        a = sup.find("a", class_="footnote-ref")
        if a:
            sup.replace_with(f"XXFNREF{a.get_text(strip=True)}XX")
        else:
            sup.replace_with(f"^{sup.get_text(strip=True)}^")
    # footnote definition block -> [^N]: text
    fndiv = soup.find("div", class_="footnotes")
    fn_defs = []
    if fndiv:
        conv = MarkdownConverter(heading_style="ATX", bullets="-")
        for li in fndiv.find_all("li"):
            fid = li.get("id", "").replace("fn:", "")
            back = li.find("a", class_="footnote-backref")
            if back:
                back.extract()
            txt = conv.convert_soup(li).strip()
            txt = re.sub(r"^\s*(?:\d+\.|-)\s*", "", txt).replace("\n", " ")
            fn_defs.append((fid, txt))
        fndiv.decompose()

    md = MarkdownConverter(heading_style="ATX", bullets="-").convert_soup(soup)
    md = md.replace("FIGCAPSTART", "*").replace("FIGCAPEND", "*")
    # footnote refs / defs (defs may contain math placeholders -> append before restore)
    md = re.sub(r"XXFNREF(\d+)XX", r"[^\1]", md)
    if fn_defs:
        md = md.rstrip() + "\n\n" + "\n".join(f"[^{n}]: {t}" for n, t in fn_defs) + "\n"
    # restore code + math placeholders last
    for key, content in CODE_PH:
        md = md.replace(key, content)
    for key, content in MATH_PH:
        md = md.replace(key, content)
    return md


def extract_post_html(page: Path):
    raw = page.read_text(encoding="utf-8")
    soup = BeautifulSoup(raw, "html.parser")
    h1 = soup.select_one("h1.post-title") or soup.find("h1")
    title = h1.get_text(strip=True) if h1 else ""
    meta = soup.select_one(".post-meta")
    date = ""
    tags = ""
    if meta:
        m = re.search(r"Date:\s*([A-Z][a-z]+ \d+, \d{4})", meta.get_text())
        if m:
            import datetime
            date = datetime.datetime.strptime(m.group(1), "%B %d, %Y").strftime("%Y-%m-%d")
    kw = soup.find("meta", attrs={"name": "keywords"})
    if kw:
        tags = kw.get("content", "")
    content = soup.select_one("div.post-content") or soup.select_one("article")
    return title, date, tags, content.decode_contents()


def main():
    build_old_posts()
    for slug in NEW_POSTS:
        title, date, tags, content = extract_post_html(SITE / "posts" / slug / "index.html")
        MATH_PH.clear(); CODE_PH.clear()
        md = convert_new(slug, content)
        write_post(slug, title, date, tags, md, "post")
    # FAQ page
    title, date, tags, content = extract_post_html(SITE / "faq" / "index.html")
    MATH_PH.clear(); CODE_PH.clear()
    md = convert_new("faq", content)
    (OUT).mkdir(parents=True, exist_ok=True)
    path = OUT / "faq.md"
    path.write_text(f"---\ntitle: \"{title}\"\nsource: {BASE}/faq/\ncrawled: {CRAWLED}\n---\n\n" + md.strip() + "\n", encoding="utf-8")
    report.append({"slug": "faq", "title": title, "date": "", "words": len(md.split()), "file": "faq.md"})

    (OUT / "_archive_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Done: {len(report)} entries")


if __name__ == "__main__":
    main()
