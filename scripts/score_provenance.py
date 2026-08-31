#!/usr/bin/env python3
"""Compute a conservative provenance-quality score for catalog records.

The score is advisory. It never promotes a record to a verified/free status by itself.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data/catalog-expanded.csv"
OUT_PATH = ROOT / "status/provenance-score.json"


def score(row: dict[str, str]) -> tuple[int, list[str]]:
    points = 0
    reasons: list[str] = []
    url = row.get("Official URL", "").strip()
    source_page = row.get("Source Page", "").strip()
    extraction = row.get("Extraction Method", "").strip()
    record_type = row.get("Record Type", "").strip()
    evidence = row.get("Evidence Status", "").strip()

    if url.startswith("https://"):
        points += 20
    if source_page.startswith("http"):
        points += 20
    if extraction:
        points += 15
    if evidence:
        points += 15
    if record_type == "credential":
        points += 20
    elif record_type == "credential-candidate":
        points += 5
        reasons.append("candidate requires classification evidence")
    else:
        points += 10
    if urlparse(url).netloc:
        points += 10

    if row.get("Price Status", "").startswith("✅") and evidence.lower() not in {"verified", "issuer-verified", "confirmed"}:
        reasons.append("free status should not be trusted without explicit evidence")

    return min(points, 100), reasons


def main() -> int:
    if not CSV_PATH.exists():
        raise SystemExit(f"missing {CSV_PATH.relative_to(ROOT)}")
    with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))
    results = []
    for row in rows:
        s, reasons = score(row)
        results.append({"id": row.get("ID", ""), "score": s, "reasons": reasons})
    payload = {
        "schema_version": "1.0",
        "record_count": len(results),
        "score_bands": {
            "high_80_100": sum(1 for x in results if x["score"] >= 80),
            "medium_50_79": sum(1 for x in results if 50 <= x["score"] < 80),
            "low_0_49": sum(1 for x in results if x["score"] < 50),
        },
        "records": results,
        "advisory_only": True,
        "generated_by": "scripts/score_provenance.py",
    }
    OUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"provenance_scored={len(results)}")
    print("provenance_scoring=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
