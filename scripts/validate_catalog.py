#!/usr/bin/env python3
"""Deterministic structural/provenance validation for the generated OpenCertAtlas catalog."""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data/catalog-expanded.csv"
JSON_PATH = ROOT / "data/catalog-expanded.json"

REQUIRED = {
    "ID",
    "Organization",
    "Certificate/Badge",
    "Official URL",
    "Record Type",
    "Price Status",
}
ALLOWED_TYPES = {
    "credential",
    "credential-reference",
    "credential-candidate",
    "source-watch",
    "regional-source",
    "language-watch",
}
ALLOWED_PRICES = {"✅", "⚠️", "⚪", "❌"}


def fail(message: str) -> None:
    raise SystemExit(f"VALIDATION ERROR: {message}")


def main() -> int:
    if not CSV_PATH.exists():
        fail(f"missing {CSV_PATH.relative_to(ROOT)}")
    if not JSON_PATH.exists():
        fail(f"missing {JSON_PATH.relative_to(ROOT)}")

    with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))

    if not rows:
        fail("catalog CSV is empty")

    missing = REQUIRED - set(rows[0].keys())
    if missing:
        fail(f"missing required columns: {sorted(missing)}")

    ids: set[str] = set()
    identity: set[tuple[str, str, str]] = set()
    for index, row in enumerate(rows, start=2):
        for field in ("ID", "Organization", "Certificate/Badge", "Official URL"):
            if not str(row.get(field, "")).strip():
                fail(f"row {index}: blank required field {field!r}")

        record_type = str(row.get("Record Type", "")).strip()
        if record_type not in ALLOWED_TYPES:
            fail(f"row {index}: unsupported Record Type {record_type!r}")

        price = str(row.get("Price Status", "")).strip()
        if not any(price.startswith(symbol) for symbol in ALLOWED_PRICES):
            fail(f"row {index}: unsupported Price Status {price!r}")

        url = str(row["Official URL"]).strip()
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            fail(f"row {index}: invalid Official URL {url!r}")

        row_id = str(row["ID"]).strip()
        if row_id in ids:
            fail(f"row {index}: duplicate ID {row_id!r}")
        ids.add(row_id)

        key = (
            str(row["Organization"]).strip().casefold(),
            str(row["Certificate/Badge"]).strip().casefold(),
            url,
        )
        if key in identity:
            fail(f"row {index}: duplicate organization/name/URL identity")
        identity.add(key)

    try:
        payload = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON: {exc}")

    if not isinstance(payload, list):
        fail("catalog-expanded.json must contain a JSON array")
    if len(payload) != len(rows):
        fail(f"CSV/JSON count mismatch: csv={len(rows)} json={len(payload)}")

    type_counts: dict[str, int] = {}
    for row in rows:
        key = row["Record Type"]
        type_counts[key] = type_counts.get(key, 0) + 1

    print(f"catalog_records={len(rows)}")
    for key in sorted(type_counts):
        print(f"record_type[{key}]={type_counts[key]}")
    print("catalog_validation=passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
