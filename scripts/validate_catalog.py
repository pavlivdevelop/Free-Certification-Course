#!/usr/bin/env python3
"""Deterministic structural and semantic validation for OpenCertAtlas catalog data."""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data/catalog-expanded.csv"
JSON_PATH = ROOT / "data/catalog-expanded.json"
MIN_RECORDS = 5_000

REQUIRED = {"ID", "Organization", "Certificate/Badge", "Official URL", "Record Type", "Price Status"}
ALLOWED_TYPES = {"credential", "credential-reference", "credential-candidate", "source-watch", "regional-source", "language-watch"}
ALLOWED_PRICE_SYMBOLS = {"✅", "⚠️", "⚪", "❌"}
NON_CREDENTIAL_TYPES = {"credential-candidate", "source-watch", "regional-source", "language-watch"}
PROHIBITED_PATTERNS = ("generated certificate", "synthetic credential", "placeholder credential", "fake certificate", "sample credential")


def fail(message: str) -> None:
    raise SystemExit(f"VALIDATION ERROR: {message}")


def main() -> int:
    if not CSV_PATH.exists(): fail(f"missing {CSV_PATH.relative_to(ROOT)}")
    if not JSON_PATH.exists(): fail(f"missing {JSON_PATH.relative_to(ROOT)}")
    with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))
    if len(rows) < MIN_RECORDS: fail(f"minimum catalog size is {MIN_RECORDS}; got {len(rows)}")
    if not rows: fail("catalog CSV is empty")
    missing = REQUIRED - set(rows[0].keys())
    if missing: fail(f"missing required columns: {sorted(missing)}")

    ids: set[str] = set(); identity: set[tuple[str, str, str]] = set(); type_counts: dict[str, int] = {}; url_warnings = 0
    free_count = conditional_count = 0
    for index, row in enumerate(rows, start=2):
        for field in ("ID", "Organization", "Certificate/Badge", "Official URL"):
            if not str(row.get(field, "")).strip(): fail(f"row {index}: blank required field {field!r}")
        record_type = str(row.get("Record Type", "")).strip()
        if record_type not in ALLOWED_TYPES: fail(f"row {index}: unsupported Record Type {record_type!r}")
        type_counts[record_type] = type_counts.get(record_type, 0) + 1
        price = str(row.get("Price Status", "")).strip()
        if not any(price.startswith(symbol) for symbol in ALLOWED_PRICE_SYMBOLS): fail(f"row {index}: unsupported Price Status {price!r}")
        if price.startswith("✅"): free_count += 1
        if price.startswith("⚠️"): conditional_count += 1

        # A row can only enter the free core when its record type is credential and free status is explicit.
        if record_type in NON_CREDENTIAL_TYPES and price.startswith("✅"):
            fail(f"row {index}: non-credential record type {record_type!r} cannot have Free status")
        if record_type == "credential-reference" and price.startswith("✅"):
            fail(f"row {index}: credential-reference cannot have Free status")
        if record_type == "credential" and price.startswith("✅") and not str(row.get("Evidence Status", "")).strip():
            fail(f"row {index}: Free credential requires Evidence Status")

        url = str(row["Official URL"]).strip(); parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc: fail(f"row {index}: invalid Official URL {url!r}")
        if not parsed.path and not parsed.query: url_warnings += 1

        row_id = str(row["ID"]).strip()
        if row_id in ids: fail(f"row {index}: duplicate ID {row_id!r}")
        ids.add(row_id)
        key = (str(row["Organization"]).strip().casefold(), str(row["Certificate/Badge"]).strip().casefold(), url)
        if key in identity: fail(f"row {index}: duplicate organization/name/URL identity")
        identity.add(key)

        text = f"{row['Organization']} {row['Certificate/Badge']}".casefold()
        if any(pattern in text for pattern in PROHIBITED_PATTERNS): fail(f"row {index}: prohibited synthetic-credential marker detected")

    try: payload = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc: fail(f"invalid JSON: {exc}")
    if not isinstance(payload, list): fail("catalog-expanded.json must contain a JSON array")
    if len(payload) != len(rows): fail(f"CSV/JSON count mismatch: csv={len(rows)} json={len(payload)}")
    csv_ids = {str(r["ID"]).strip() for r in rows}; json_ids = {str(r.get("ID", "")).strip() for r in payload}
    if csv_ids != json_ids: fail("CSV/JSON ID sets differ")
    if free_count != sum(1 for r in rows if str(r.get("Price Status", "")).startswith("✅")): fail("free count integrity mismatch")

    print(f"catalog_records={len(rows)}")
    print(f"free_core_records={free_count}")
    print(f"conditional_records={conditional_count}")
    for key in sorted(type_counts): print(f"record_type[{key}]={type_counts[key]}")
    print(f"url_shape_warnings={url_warnings}")
    print("catalog_validation=passed")
    return 0


if __name__ == "__main__": sys.exit(main())
