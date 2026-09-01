#!/usr/bin/env python3
"""Validate that the published free core contains only promoted free credentials."""
from __future__ import annotations

import csv
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data/free-core.csv"
REQUIRED = {
    "ID", "Organization", "Certificate/Badge", "Record Type", "Price Status",
    "Official URL", "Evidence Status", "Last Reviewed", "Source Page",
}
ALLOWED_EVIDENCE = {"verified-free", "issuer-verified-free", "manual-verified-free"}


def fail(message: str) -> None:
    raise SystemExit(f"FREE-CORE ERROR: {message}")


def main() -> int:
    if not PATH.exists():
        fail(f"missing {PATH.relative_to(ROOT)}")
    with PATH.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
        fields = set(reader.fieldnames or [])
    missing = REQUIRED - fields
    if missing:
        fail(f"missing required columns: {sorted(missing)}")

    ids: set[str] = set()
    for line, row in enumerate(rows, start=2):
        record_type = str(row.get("Record Type", "")).strip()
        evidence = str(row.get("Evidence Status", "")).strip().casefold()
        price = str(row.get("Price Status", "")).strip()
        source = str(row.get("Source Page", "")).strip()
        official = str(row.get("Official URL", "")).strip()
        reviewed = str(row.get("Last Reviewed", "")).strip()
        row_id = str(row.get("ID", "")).strip()

        if record_type != "credential":
            fail(f"row {line}: Record Type must be credential; got {record_type!r}")
        if evidence not in ALLOWED_EVIDENCE:
            fail(f"row {line}: Evidence Status must be an explicit verified-free state; got {evidence!r}")
        if not price.startswith("✅"):
            fail(f"row {line}: verified-free row must carry explicit Free status")
        if not reviewed:
            fail(f"row {line}: missing Last Reviewed")
        if not source:
            fail(f"row {line}: missing Source Page")
        for field, value in (("Official URL", official), ("Source Page", source)):
            parsed = urlparse(value)
            if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                fail(f"row {line}: invalid {field}: {value!r}")
        if not row_id:
            fail(f"row {line}: blank ID")
        if row_id in ids:
            fail(f"row {line}: duplicate ID {row_id!r}")
        ids.add(row_id)

    print(f"free_core_records={len(rows)}")
    print("free_core_validation=passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
