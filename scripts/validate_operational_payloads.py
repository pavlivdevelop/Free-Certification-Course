#!/usr/bin/env python3
"""Validate generated operational payloads without changing their semantics."""
from __future__ import annotations

import csv
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "status/review-queue-lite.json"
HEALTH = ROOT / "status/source-health.json"
QUEUE = ROOT / "status/REVIEW-QUEUE.csv"


def url_ok(value: str) -> bool:
    parsed = urlparse(value or "")
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def main() -> int:
    for path in (REVIEW, HEALTH, QUEUE):
        if not path.is_file() or path.stat().st_size == 0:
            raise SystemExit(f"missing or empty operational payload: {path.relative_to(ROOT)}")

    review = json.loads(REVIEW.read_text(encoding="utf-8"))
    if review.get("schema_version") != "1.0":
        raise SystemExit("review payload schema_version must be 1.0")
    records = review.get("records")
    if not isinstance(records, list):
        raise SystemExit("review payload records must be a list")
    if len(records) > int(review.get("browser_limit", 600)):
        raise SystemExit("review payload exceeds browser_limit")
    allowed_priorities = {10, 15, 20, 30}
    required_review = {"id", "organization", "name", "record_type", "review_reason", "queue_priority", "official_url"}
    for row in records:
        if not required_review.issubset(row):
            raise SystemExit(f"review record missing keys: {sorted(required_review - set(row))}")
        if int(row["queue_priority"]) not in allowed_priorities:
            raise SystemExit(f"unexpected queue priority: {row['queue_priority']}")
        if row.get("evidence_status") == "verified-free":
            raise SystemExit(f"review payload must not promote evidence status: {row['id']}")
        if row.get("official_url") and not url_ok(row["official_url"]):
            raise SystemExit(f"invalid official URL in review payload: {row['id']}")

    health = json.loads(HEALTH.read_text(encoding="utf-8"))
    if health.get("schema_version") != "1.0":
        raise SystemExit("source health schema_version must be 1.0")
    states = {"reachable", "reachable-restricted", "http-error", "unreachable"}
    items = health.get("items")
    if not isinstance(items, list):
        raise SystemExit("source health items must be a list")
    for row in items:
        if row.get("state") not in states:
            raise SystemExit(f"unexpected source-health state: {row.get('state')}")
        if not url_ok(str(row.get("url", ""))):
            raise SystemExit(f"invalid provider URL: {row.get('organization', '<unknown>')}")

    with QUEUE.open(encoding="utf-8-sig", newline="") as fh:
        queue = list(csv.DictReader(fh))
    if len(queue) != int(review.get("total", -1)):
        raise SystemExit(f"review payload total {review.get('total')} != queue rows {len(queue)}")

    print(f"operational_payloads=passed review={len(records)} source_health={len(items)} queue={len(queue)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
