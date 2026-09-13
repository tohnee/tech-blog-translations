#!/usr/bin/env python3
"""Slow retry loop: verify the last 4 webReader-era files against live pages.

Fetches /tmp/oai_job_final5.json slugs (skips existing HTML) until all 5 OK
or 8 rounds pass. Pure orchestration of crawl_openai_fetch.py via runpy.
"""
import runpy
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LOG = Path("/tmp/oai_final5.log")
JOB = "/tmp/oai_job_final5.json"
TARGET_OK = 5
MAX_ROUNDS = 8
ROUND_SLEEP_S = 400


def log(msg):
    with LOG.open("a", encoding="utf-8") as f:
        f.write(msg + "\n")
    print(msg, flush=True)


def ok_count() -> int:
    n = 0
    for line in LOG.read_text().splitlines() if LOG.exists() else []:
        n += line.startswith("OK ")
    return n


log(f"=== final5 loop start {time.strftime('%F %T')} ===")
for rnd in range(1, MAX_ROUNDS + 1):
    log(f"--- round {rnd} ---")
    sys.argv = [str(ROOT / "crawl_openai_fetch.py"), "chrome", JOB]
    try:
        runpy.run_path(str(ROOT / "crawl_openai_fetch.py"), run_name="__main__")
    except SystemExit:
        pass
    n = ok_count()
    log(f"round {rnd}: total OK={n}")
    if n >= TARGET_OK:
        log(f"ALL VERIFIED {time.strftime('%F %T')}")
        break
    time.sleep(ROUND_SLEEP_S)
log(f"=== final5 loop end {time.strftime('%F %T')} ===")
