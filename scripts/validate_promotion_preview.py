#!/usr/bin/env python3
"""Validate the deterministic, advisory promotion preview contract."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "status/promotion-preview.md"
PAYLOAD = ROOT / "status/promotion-preview.json"
CATALOG = ROOT / "data/catalog-expanded.csv"
ALLOWED_TIERS = {"high-confidence review candidate", "review candidate", "needs additional evidence"}
ALLOWED_TRIAGE = {"likely credential identity", "learning-content signal", "uncertain credential identity"}


def fail(message: str) -> None:
    raise SystemExit(f"PROMOTION PREVIEW ERROR: {message}")


def main() -> int:
    if not REPORT.exists() or not REPORT.stat().st_size:
        fail("status/promotion-preview.md is missing or empty")
    if not PAYLOAD.exists() or not PAYLOAD.stat().st_size:
        fail("status/promotion-preview.json is missing or empty")
    if not CATALOG.exists() or not CATALOG.stat().st_size:
        fail("data/catalog-expanded.csv is missing or empty")

    data = json.loads(PAYLOAD.read_text(encoding="utf-8"))
    if data.get("schema_version") != "1.3":
        fail("unsupported schema_version")
    if data.get("advisory_only") is not True:
        fail("advisory_only must be true")
    if data.get("auto_promotion") is not False:
        fail("auto_promotion must be false")

    catalog_sha256 = hashlib.sha256(CATALOG.read_bytes()).hexdigest()
    if data.get("catalog_sha256") != catalog_sha256:
        fail("catalog_sha256 does not match data/catalog-expanded.csv")

    records = data.get("records")
    if not isinstance(records, list):
        fail("records must be a list")
    if len(records) != int(data.get("rows_shown", -1)):
        fail("rows_shown does not match records length")
    if len(records) > 500:
        fail("preview payload may contain at most 500 rows")

    providers = data.get("providers")
    if not isinstance(providers, list):
        fail("providers must be a list")
    if len(providers) != int(data.get("providers_shown", -1)):
        fail("providers_shown does not match providers length")
    if len(providers) > 100:
        fail("preview payload may contain at most 100 provider groups")

    previous_provider = None
    provider_totals = {"candidate_records": 0, "reviewable": 0, "high_confidence": 0}
    for provider in providers:
        required = (
            "organization", "host", "candidate_records", "reviewable", "high_confidence",
            "likely_credential_identity", "learning_content_signals", "uncertain_credential_identity",
        )
        for key in required:
            if key not in provider:
                fail(f"provider missing {key}")
        if not provider["organization"]:
            fail("provider organization must not be empty")
        if not provider["host"]:
            fail("provider host must not be empty")
        for key in required[2:]:
            if not isinstance(provider[key], int) or provider[key] < 0:
                fail(f"invalid provider summary field: {key}")
        if provider["reviewable"] > provider["candidate_records"] or provider["high_confidence"] > provider["reviewable"]:
            fail("provider counts must be monotonic")
        if provider["likely_credential_identity"] + provider["learning_content_signals"] + provider["uncertain_credential_identity"] != provider["candidate_records"]:
            fail("provider triage counts do not sum to candidate_records")
        sort_key = (
            -provider["reviewable"], -provider["high_confidence"], -provider["candidate_records"],
            provider["organization"].casefold(), provider["host"].casefold(),
        )
        if previous_provider is not None and sort_key < previous_provider:
            fail("providers are not deterministically sorted")
        previous_provider = sort_key
        for key in provider_totals:
            provider_totals[key] += provider[key]

    previous = None
    for row in records:
        required = ("score", "tier", "triage", "organization", "name", "evidence", "method", "url", "source", "reasons")
        for key in required:
            if key not in row:
                fail(f"row missing {key}")
        score = row["score"]
        if not isinstance(score, int) or score < 0:
            fail(f"invalid score: {score!r}")
        if row["tier"] not in ALLOWED_TIERS:
            fail(f"invalid tier: {row['tier']!r}")
        if row["triage"] not in ALLOWED_TRIAGE:
            fail(f"invalid triage: {row['triage']!r}")
        if not isinstance(row["reasons"], list) or not all(isinstance(x, str) for x in row["reasons"]):
            fail("reasons must be a list of strings")
        for key in ("url", "source"):
            value = row[key]
            if value:
                parsed = urlparse(value)
                if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                    fail(f"invalid {key} URL: {value!r}")

        sort_key = (-score, row["tier"], row["triage"], row["organization"].casefold(), row["name"].casefold())
        if previous is not None and sort_key < previous:
            fail("rows are not deterministically sorted")
        previous = sort_key

    for field in ("candidate_records", "reviewable", "high_confidence", "likely_credential_identity", "learning_content_signals", "provider_count"):
        if not isinstance(data.get(field), int) or data[field] < 0:
            fail(f"invalid summary field: {field}")
    if data["providers_shown"] > data["provider_count"]:
        fail("providers_shown cannot exceed provider_count")
    if data["provider_count"] < len(providers):
        fail("provider_count cannot be smaller than providers shown")

    # The provider payload is intentionally bounded, so its totals need not equal the global catalog totals.
    for key in ("candidate_records", "reviewable", "high_confidence"):
        if provider_totals[key] > data["candidate_records"]:
            fail("provider summary exceeds global candidate count")

    report = REPORT.read_text(encoding="utf-8")
    for marker in (
        "This report is advisory only",
        "never changes catalog records",
        "Credential-language and learning-content heuristics affect triage only",
        "Provider aggregation is for batch review",
        "not eligible for automatic promotion",
        "Manual review must confirm",
    ):
        if marker.lower() not in report.lower():
            fail(f"report missing safety marker: {marker!r}")

    print(f"validated_promotion_rows={len(records)}")
    print(f"validated_promotion_candidates={data.get('candidate_records', 0)}")
    print(f"validated_promotion_reviewable={data.get('reviewable', 0)}")
    print(f"validated_promotion_high_confidence={data.get('high_confidence', 0)}")
    print(f"validated_promotion_likely_credential_identity={data.get('likely_credential_identity', 0)}")
    print(f"validated_promotion_learning_content_signals={data.get('learning_content_signals', 0)}")
    print(f"validated_promotion_provider_count={data.get('provider_count', 0)}")
    print(f"validated_promotion_catalog_sha256={catalog_sha256}")
    print("promotion_preview=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
