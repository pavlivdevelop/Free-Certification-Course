#!/usr/bin/env python3
"""Check source reachability and review age.

HTTP reachability is deliberately kept separate from credential validity and price.
"""
from __future__ import annotations

import csv
import datetime as dt
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data/catalog-expanded.csv"
TODAY = dt.date.today()
MAX_AGE = 120
USER_AGENT = "OpenCertAtlas/2026 (+https://github.com/pavlivdevelop/OpenCertAtlas)"


def probe(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            return response.status, response.geturl(), ""
    except Exception as exc:
        return None, url, str(exc)


if not CATALOG.exists():
    raise SystemExit("data/catalog-expanded.csv is missing; run scripts/build_official_catalog.py first")

with CATALOG.open(encoding="utf-8-sig", newline="") as fh:
    rows = list(csv.DictReader(fh))

items = []
for row in rows:
    try:
        last = dt.date.fromisoformat(row.get("Last Reviewed", ""))
    except Exception:
        last = dt.date.min
    age = (TODAY - last).days
    url = row.get("Official URL", "")
    code, final_url, error = probe(url) if url.startswith(("http://", "https://")) else (None, "", "")
    items.append({
        **row,
        "review_due": age > MAX_AGE,
        "review_age_days": age,
        "http_status": code,
        "final_url": final_url,
        "http_error": error,
    })

report = {
    "generated": str(TODAY),
    "max_review_age_days": MAX_AGE,
    "total": len(items),
    "review_due": sum(item["review_due"] for item in items),
    "http_failures": sum(item["http_status"] is None and item["Official URL"] for item in items),
    "items": items,
}

out = ROOT / "status/freshness-report.json"
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"checked={len(items)} review_due={report['review_due']} http_failures={report['http_failures']}")
