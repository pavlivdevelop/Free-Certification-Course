#!/usr/bin/env python3
"""Validate the deterministic, advisory promotion preview contract."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "status/promotion-preview.md"
PAYLOAD = ROOT / "status/promotion-preview.json"
ALLOWED_TIERS = {"high-confidence review candidate", "review candidate", "needs additional evidence"}


def fail(message: str) -> None:
    raise SystemExit(f"PROMOTION PREVIEW ERROR: {message}")


def main() -> int:
    if not REPORT.exists() or not REPORT.stat().st_size:
        fail("status/promotion-preview.md is missing or empty")
    if not PAYLOAD.exists() or not PAYLOAD.stat().st_size:
        fail("status/promotion-preview.json is missing or empty")

    data = json.loads(PAYLOAD.read_text(encoding="utf-8"))
    if data.get("schema_version") != "1.0":
        fail("unsupported schema_version")
    if data.get("advisory_only") is not True:
        fail("advisory_only must be true")
    if data.get("auto_promotion") is not False:
        fail("auto_promotion must be false")

    records = data.get("records")
    if not isinstance(records, list):
        fail("records must be a list")
    if len(records) != int(data.get("rows_shown", -1)):
        fail("rows_shown does not match records length")
    if len(records) > 500:
        fail("preview payload may contain at most 500 rows")

    previous = None
    for row in records:
        required = ("score", "tier", "organization", "name", "evidence", "method", "url", "source", "reasons")
        for key in required:
            if key not in row:
                fail(f"row missing {key}")
        score = row["score"]
        if not isinstance(score, int) or score < 0:
            fail(f"invalid score: {score!r}")
        if row["tier"] not in ALLOWED_TIERS:
            fail(f"invalid tier: {row['tier']!r}")
        if not isinstance(row["reasons"], list) or not all(isinstance(x, str) for x in row["reasons"]):
            fail("reasons must be a list of strings")
        for key in ("url", "source"):
            value = row[key]
            if value:
                parsed = urlparse(value)
                if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                    fail(f"invalid {key} URL: {value!r}")

        sort_key = (-score, row["tier"], row["organization"].casefold(), row["name"].casefold())
        if previous is not None and sort_key < previous:
            fail("rows are not deterministically sorted")
        previous = sort_key

    report = REPORT.read_text(encoding="utf-8")
    for marker in (
        "This report is advisory only",
        "never changes catalog records",
        "not eligible for automatic promotion",
        "Manual review must confirm",
    ):
        if marker.lower() not in report.lower():
            fail(f"report missing safety marker: {marker!r}")

    print(f"validated_promotion_rows={len(records)}")
    print(f"validated_promotion_candidates={data.get('candidate_records', 0)}")
    print(f"validated_promotion_reviewable={data.get('reviewable', 0)}")
    print(f"validated_promotion_high_confidence={data.get('high_confidence', 0)}")
    print("promotion_preview=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
