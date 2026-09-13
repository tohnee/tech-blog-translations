#!/usr/bin/env python3
"""Restore markdown heading levels in flattened OpenAI article archives.

webReader's text-mode extraction flattens headings (and list markers) into
plain paragraphs for roughly half of the articles. This script re-marks
heading lines conservatively:

- a single-line block of 2-8 words / 3-60 chars that starts with a capital
  and carries no sentence-final punctuation, NOT preceded by a
  colon-ending paragraph, becomes `## …`
- `Citation` is always a heading
- a first block identical to the frontmatter title becomes `# …`

Anything ambiguous stays a paragraph. List items are intentionally left as
paragraphs; translators normalize those.
"""
import re
import sys
from pathlib import Path

POSTS = Path(__file__).parent / "openai-articles" / "posts"

TRAIL_OK = (";", ".", ",", ":", "!", "?", "—", "–")


def heading_candidate(line: str) -> bool:
    s = line.strip()
    if not (3 <= len(s) <= 60):
        return False
    words = s.split()
    if not (2 <= len(words) <= 8):
        return False
    if not re.match(r"^[A-Z0-9\u2018\u201c]", s):
        return False
    if s.endswith(TRAIL_OK):
        return False
    # reject sentences: contain a mid-line period+space or multiple commas
    if re.search(r"[a-z]\.\s", s) or s.count(",") > 1:
        return False
    return True


def process(path: Path, apply: bool = False) -> list[str]:
    text = path.read_text()
    m = re.match(r"\A---\n.*?\n---\n\n", text, re.S)
    if not m:
        return ["no frontmatter"]
    fm, body = text[: m.end()], text[m.end():]
    if re.search(r"^## ", body, re.M):
        return ["already has headings"]
    title = re.search(r'^title: "(.*)"$', fm, re.M)
    title = title.group(1) if title else ""

    blocks = body.split("\n\n")
    out, report = [], []
    in_list = False  # colon-intro list run: short blocks are items, not headings
    for i, block in enumerate(blocks):
        stripped = block.strip()
        if i == 0 and title and stripped.rstrip() == title.rstrip():
            out.append(f"# {stripped}")
            report.append(f"  H1(dup title): {stripped!r}")
            in_list = False
            continue
        if "\n" not in stripped and heading_candidate(stripped) and not in_list:
            out.append(f"## {stripped}")
            report.append(f"  H2: {stripped!r}")
            in_list = False
            continue
        if stripped == "Citation":
            out.append("## Citation")
            report.append("  H2: 'Citation'")
            in_list = False
            continue
        # a long paragraph or one ending with sentence punctuation ends a list run
        if len(stripped) > 60 or re.search(r"[.…?!\u201d]\s*$", stripped):
            in_list = False
        if stripped.rstrip().endswith(":"):
            in_list = True
        out.append(block)
    new_text = fm + "\n\n".join(out)
    if apply and new_text != text:
        path.write_text(new_text)
    return report or ["  (no changes)"]


def main():
    apply = "--apply" in sys.argv
    for path in sorted(POSTS.glob("*.md")):
        report = process(path, apply=apply)
        if report != ["already has headings"] and report != ["  (no changes)"]:
            print(path.name)
            for line in report:
                print(line)
    print(f"\nmode: {'APPLY' if apply else 'DRY-RUN (pass --apply to write)'}")


if __name__ == "__main__":
    main()
