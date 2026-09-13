#!/usr/bin/env python3
"""Self-healing driver: fetch missing OpenAI articles until all 69 are archived.

Loop: run crawl_openai_fetch.py (headed chrome) over the missing job list,
finalize new HTML, recompute the missing set; stop when zero or max rounds.
"""
import json
import runpy
import sys
import time
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LOG = Path("/tmp/oai_loop.log")
JOB = Path("/tmp/oai_job_missing.json")
MAX_ROUNDS = 24
ROUND_SLEEP_S = 180


def log(msg: str) -> None:
    with LOG.open("a", encoding="utf-8") as f:
        f.write(f"{msg}\n")
    print(msg, flush=True)


def missing_slugs() -> list[str]:
    meta = json.loads((ROOT / "openai-articles" / "meta.json").read_text())
    posts = ROOT / "openai-articles" / "posts"
    return [m["slug"] for m in meta if not (posts / f"{m['slug']}.md").exists()]


def run_module(path: Path, argv: list[str]) -> None:
    sys.argv = [str(path)] + argv
    buf_out, buf_err = Path("/dev/null"), None
    import io
    out, err = io.StringIO(), io.StringIO()
    try:
        with redirect_stdout(out), redirect_stderr(err):
            runpy.run_path(str(path), run_name="__main__")
    except SystemExit:
        pass
    log((out.getvalue() + err.getvalue()).strip()[-2000:] or "(no output)")


log(f"=== loop start {time.strftime('%F %T')} ===")
for rnd in range(1, MAX_ROUNDS + 1):
    missing = missing_slugs()
    log(f"--- round {rnd}: {len(missing)} missing ---")
    if not missing:
        log(f"ALL DONE {time.strftime('%F %T')}")
        break
    meta = json.loads((ROOT / "openai-articles" / "meta.json").read_text())
    by_slug = {m["slug"]: m for m in meta}
    job = [{"slug": s, "url": by_slug[s]["url"]} for s in missing]
    JOB.write_text(json.dumps(job))
    run_module(ROOT / "crawl_openai_fetch.py", ["chrome", str(JOB)])
    run_module(ROOT / "crawl_openai_autofinalize.py", [])
    log(f"round {rnd} done, remaining={len(missing_slugs())}")
    if rnd < MAX_ROUNDS:
        time.sleep(ROUND_SLEEP_S)
log(f"=== loop end {time.strftime('%F %T')} ===")
