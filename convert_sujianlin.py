#!/usr/bin/env python3
"""科学空间文章 HTML → Markdown 转换与整理。

- 正文取 div#PostContent 的元素子节点，从「转载到请包括本文地址」起裁掉全部样板
- 公式以原始 LaTeX 直接内嵌于 HTML 文本，转换前用占位符保护，转换后还原
- 输出按分类分目录：sujianlin-articles/<分类>/<ID>-<标题>.md
"""
import json
import re
from html import unescape
from pathlib import Path

from bs4 import BeautifulSoup, Comment, Tag
from markdownify import MarkdownConverter

BASE = Path(__file__).resolve().parent
SRC = BASE / "sujianlin-src" / "posts"
OUT = BASE / "sujianlin-articles"
OUT.mkdir(exist_ok=True)

# ---------- 公式占位符保护 ----------

MATH_PATTERNS = [
    # display 环境（equation/align/gather/multline/eqnarray 及星号版本）
    re.compile(
        r"\\begin\{((?:equation|align|alignat|flalign|gather|multline|eqnarray|split|aligned|gathered|array|cases|dcases|subequations|matrix|pmatrix|bmatrix|Bmatrix|vmatrix|Vmatrix|smallmatrix)\*?)\}.*?\\end\{\1\*?\}",
        re.S,
    ),
    re.compile(r"\$\$.+?\$\$", re.S),          # $$...$$
    re.compile(r"\\\[.*?\\\]", re.S),           # \[...\]
    re.compile(r"\\\(.*?\\\)", re.S),           # \(...\)
    re.compile(r"(?<!\\)\$(?!\$)(?:\\.|[^$\n])+?(?<!\\)\$(?!\$)"),  # $...$（单行内）
]
TOKEN_RE = re.compile(r"ZZMATH(\d+)ZZ")


def protect_math(html: str):
    """把公式段替换为 ZZMATHiZZ 占位符，返回 (新HTML, 公式列表)。公式内的 HTML 实体已反转义。"""
    store = []

    def _sub(m):
        # 公式内部源码里的 <br/> 是编辑器插入的冗余换行，LaTeX 的 \\ 已负责换行
        s = re.sub(r"<br\s*/?>", "", unescape(m.group(0)))
        store.append(s)
        return f"ZZMATH{len(store)-1}ZZ"

    for pat in MATH_PATTERNS:
        html = pat.sub(_sub, html)
    return html, store


def restore_math(md: str, store) -> str:
    for _ in range(4):  # 嵌套公式需多轮
        if "ZZMATH" not in md:
            break
        md = TOKEN_RE.sub(lambda m: store[int(m.group(1))], md)
    return md


# ---------- HTML → Markdown 转换器 ----------

class KexueConverter(MarkdownConverter):
    """针对科学空间定制的转换器。"""

    def convert_pre(self, el, text, parent_tags=None):
        code = el.get_text()
        lang = ""
        for cls in el.get("class", []) or []:
            for c in cls.split():
                if c.startswith("language-"):
                    lang = c.split("-", 1)[1]
        fenced = f"```{lang}\n{code}\n```\n\n" if code.strip() else ""
        return fenced

    def convert_table(self, el, text, parent_tags=None):
        # markdownify 无表格支持，保留原始 HTML（Markdown 渲染器支持内嵌 HTML）
        html = str(el)
        return html + "\n\n"

    def convert_iframe(self, el, text, parent_tags=None):
        src = el.get("src", "")
        return f"[嵌入内容]({src})\n\n" if src else ""


def make_converter() -> KexueConverter:
    return KexueConverter(
        heading_style="ATX",
        bullets="-",
        escape_underscores=False,
        escape_asterisks=False,
        escape_misc=False,
        strip=["script", "style", "form", "button", "input", "select", "ins", "del"],
    )


# ---------- 元数据与正文提取 ----------

HEADING_TAIL = re.compile(r"(?m)^(#{1,6}\s.+?)\s*(?:\[#\]\(#[^)]*\)|#+)\s*$")
BOILER_IMG = re.compile(r"!\[[^\]]*\]\((https://kexue\.fm/usr/themes/[^)]*)\)")


def extract_meta(soup: BeautifulSoup, pid: int) -> dict:
    meta = {"id": pid, "category": "", "tags": [], "title": ""}
    h1 = soup.find("h1")
    if h1 and h1.a:
        meta["title"] = h1.a.get_text(strip=True)
    sub = soup.find("span", class_="submitted")
    if sub:
        m = re.search(r"(\d{4}-\d{2}-\d{2})", sub.get_text())
        if m:
            meta["date"] = m.group(1)
    cat = soup.find("span", class_="cat")
    if cat:
        a = cat.find("a", href=re.compile(r"/category/"))
        if a:
            meta["category"] = a.get_text(strip=True)
        tag_links = cat.find_all("a", href=re.compile(r"/tag/"))
        meta["tags"] = [t.get_text(strip=True) for t in tag_links if t.get_text(strip=True)]
    return meta


BOILER_MARKERS = (
    "转载到请包括本文地址",
    "更详细的转载事宜请参考",
    'id="content_tips"',
    'id="pay"',
    'id="how_to_cite"',
    'id="similar"',
    'id="entrynavigation"',
)


def extract_content_html(soup: BeautifulSoup) -> str:
    div = soup.find("div", id="PostContent")
    if div is None:
        return ""
    html = str(div)
    # 在原始字符串上裁掉尾部样板（部分文章 HTML 畸形、全文嵌在单个 <p> 里，
    # 必须按标记回溯开标签裁剪，不能按 DOM 子节点文字判断）
    cut = len(html)
    for marker in BOILER_MARKERS:
        pos = html.find(marker)
        if pos == -1:
            continue
        start = max(html.rfind("<p ", 0, pos), html.rfind("<p>", 0, pos), html.rfind("<div", 0, pos))
        if start != -1 and start < cut:
            cut = start
    html = html[:cut]
    inner = BeautifulSoup(html, "html.parser")
    # 站内相对链接/图片绝对化
    for a in inner.find_all("a", href=True):
        if a["href"].startswith("/"):
            a["href"] = "https://kexue.fm" + a["href"]
    for img in inner.find_all("img", src=True):
        if img["src"].startswith("/"):
            img["src"] = "https://kexue.fm" + img["src"]
        if "/usr/themes/" in img.get("src", ""):
            img.decompose()  # 付款码/版权徽章等主题图片
    return inner.decode_contents()


def html_to_markdown(content_html: str, conv: KexueConverter) -> str:
    if not content_html.strip():
        return ""
    protected, store = protect_math(content_html)
    md = conv.convert(protected)
    md = restore_math(md, store)
    # 标题尾部的锚点 "#"
    md = HEADING_TAIL.sub(r"\1", md)
    # 残留注释与样板图片
    md = re.sub(r"<!--.*?-->", "", md, flags=re.S)
    md = BOILER_IMG.sub("", md)
    # 旧博客伪标签
    md = md.replace("[separator]", "")
    # 展平多余空行
    md = re.sub(r"\n{3,}", "\n\n", md)
    md = "\n".join(line.rstrip() for line in md.split("\n")).strip()
    return md


SAFE_TITLE_RE = re.compile(r'[\\/:*?"<>|\x00-\x1f]')


def safe_title(title: str, max_len: int = 90) -> str:
    t = SAFE_TITLE_RE.sub("－", title).strip().strip(".")
    return t[:max_len]


def frontmatter(meta: dict) -> str:
    lines = ["---"]
    lines.append(f'title: "{meta["title"].replace(chr(34), chr(39))}"')
    lines.append(f'date: "{meta.get("date", "")}"')
    lines.append(f'author: "苏剑林"')
    lines.append(f'category: "{meta.get("category", "")}"')
    tags = meta.get("tags") or []
    lines.append("tags: [" + ", ".join(f'"{t}"' for t in tags) + "]")
    lines.append(f'url: "https://kexue.fm/archives/{meta["id"]}"')
    lines.append(f'blog: "科学空间 | Scientific Spaces"')
    lines.append("---")
    return "\n".join(lines)


def convert_post(pid: int) -> dict:
    f = SRC / f"{pid}.html"
    html = f.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")
    meta = extract_meta(soup, pid)
    content_html = extract_content_html(soup)
    md = html_to_markdown(content_html, make_converter())
    meta["chars"] = len(md)
    doc = frontmatter(meta) + "\n\n" + md + "\n"
    cat_dir = meta.get("category") or "未分类"
    cat_dir = cat_dir.replace("/", "-")
    d = OUT / cat_dir
    d.mkdir(parents=True, exist_ok=True)
    name = f"{pid}-{safe_title(meta['title'] or str(pid))}.md"
    (d / name).write_text(doc, encoding="utf-8")
    return meta


def main():
    posts = json.loads((BASE / "sujianlin-src" / "posts_index.json").read_text(encoding="utf-8"))
    stats = {"ok": 0, "empty": 0, "missing": 0}
    index_rows = []
    for p in posts:
        f = SRC / f"{p['id']}.html"
        if not f.exists():
            stats["missing"] += 1
            continue
        try:
            meta = convert_post(p["id"])
        except Exception as e:
            stats["missing"] += 1
            print(f"[ERR] {p['id']}: {e}")
            continue
        if meta["chars"] < 100:
            stats["empty"] += 1
        stats["ok"] += 1
        index_rows.append(meta)
    (BASE / "sujianlin-src" / "convert_report.json").write_text(
        json.dumps({"stats": stats, "rows": index_rows}, ensure_ascii=False, indent=1),
        encoding="utf-8",
    )
    print("convert stats:", stats)
    by_cat = {}
    for r in index_rows:
        by_cat[r.get("category") or "未分类"] = by_cat.get(r.get("category") or "未分类", 0) + 1
    for k, v in sorted(by_cat.items(), key=lambda x: -x[1]):
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
