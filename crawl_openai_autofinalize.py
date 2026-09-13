#!/usr/bin/env python3
"""Finalize every fetched HTML in /tmp/oai_html that has no posts/<slug>.md yet.

Reads slug->url/category from openai-articles/meta.json. Safe to re-run.
Calls crawl_openai_finalize.py in-process (no subprocess).
"""
import json
import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HTML_DIR = Path("/tmp/oai_html")
meta = json.loads((ROOT / "openai-articles" / "meta.json").read_text())
by_slug = {m["slug"]: m for m in meta}

done, skipped, failed = [], [], []
for html in sorted(HTML_DIR.glob("*.html")):
    slug = html.stem
    m = by_slug.get(slug)
    if m is None:
        skipped.append((slug, "not in meta.json"))
        continue
    out = ROOT / "openai-articles" / "posts" / f"{slug}.md"
    if out.exists() and out.stat().st_size > 1000:
        skipped.append((slug, "md exists"))
        continue
    sys.argv = [str(ROOT / "crawl_openai_finalize.py"), slug, m["url"], m["category"]]
    import io
    from contextlib import redirect_stdout, redirect_stderr
    buf_out, buf_err = io.StringIO(), io.StringIO()
    try:
        with redirect_stdout(buf_out), redirect_stderr(buf_err):
            runpy.run_path(str(ROOT / "crawl_openai_finalize.py"), run_name="__main__")
        done.append(slug)
        print(f"FINALIZED {slug}: {buf_out.getvalue().strip()}")
    except SystemExit as e:
        msg = (buf_out.getvalue() + buf_err.getvalue()).strip() or f"exit {e.code}"
        failed.append((slug, msg.splitlines()[-1] if msg else "unknown"))
        print(f"FAILED {slug}: {failed[-1][1]}")
    except Exception as e:  # noqa: BLE001
        failed.append((slug, repr(e)))
        print(f"FAILED {slug}: {e!r}")

print(f"\ndone={len(done)} skipped={len(skipped)} failed={len(failed)}")
for slug, why in failed:
    print(f"  NEEDS-ATTENTION {slug}: {why}")
