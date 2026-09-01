#!/usr/bin/env python3
"""Build a deterministic human-review queue from the canonical catalog.

The queue is operational metadata only. It never changes Evidence Status and never
promotes a record automatically. It prioritizes exact credential candidates and
free-price signals that need issuer-level review.
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data/catalog-expanded.csv"
OUTPUT = ROOT / "status/REVIEW-QUEUE.csv"

FIELDS = [
    "Queue Priority", "Review Reason", "ID", "Organization", "Certificate/Badge",
    "Record Type", "Category", "Price Status", "Evidence Status", "Official URL",
    "Source Page", "Last Reviewed", "Current Priority",
]

EXCLUDED_TYPES = {"source-watch", "regional-source", "language-watch"}
VERIFIED = {"verified", "verified-free", "issuer-verified-free", "manual-verified-free"}


def score(row: dict[str, str]) -> tuple[int, str]:
    record_type = row.get("Record Type", "").strip()
    evidence = row.get("Evidence Status", "").strip().casefold()
    price = row.get("Price Status", "").strip()
    if record_type == "credential-candidate" and price.startswith("✅"):
        return 10, "candidate with free-price signal"
    if record_type == "credential-candidate":
        return 20, "candidate credential identity needs verification"
    if record_type == "credential" and price.startswith("✅") and evidence not in VERIFIED:
        return 15, "free-price signal needs credential-level promotion review"
    if record_type == "credential" and evidence not in VERIFIED:
        return 30, "credential needs issuer-level evidence review"
    return 99, "manual follow-up"


def main() -> int:
    if not INPUT.exists():
        raise SystemExit(f"missing {INPUT.relative_to(ROOT)}")
    with INPUT.open("r", encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))

    queue: list[tuple[tuple[int, str, str], dict[str, str]]] = []
    for row in rows:
        if row.get("Record Type", "").strip() in EXCLUDED_TYPES:
            continue
        evidence = row.get("Evidence Status", "").strip().casefold()
        record_type = row.get("Record Type", "").strip()
        if evidence in VERIFIED and record_type == "credential":
            continue
        priority, reason = score(row)
        if priority >= 99:
            continue
        queue.append(((priority, row.get("Organization", "").casefold(), row.get("Certificate/Badge", "").casefold()), {**row, "Queue Priority": str(priority), "Review Reason": reason}))

    queue.sort(key=lambda x: x[0])
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS)
        writer.writeheader()
        for _, row in queue:
            writer.writerow({field: row.get(field, "") for field in FIELDS})

    print(f"review_queue_records={len(queue)}")
    for priority in (10, 15, 20, 30):
        print(f"priority_{priority}={sum(1 for key, _ in queue if key[0] == priority)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
