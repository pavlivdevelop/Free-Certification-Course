#!/usr/bin/env python3
"""Validate the bounded manual evidence-packet contract."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
PAYLOAD = ROOT / "status/evidence-packet-index.json"
CATALOG = ROOT / "data/catalog-expanded.csv"
ALLOWED_DECISIONS = {"pending", "promote", "reject", "needs-more-evidence"}
REQUIRED_CHECKS = {
    "credential_identity",
    "credential_bearing_activity",
    "current_access_or_price",
    "eligibility_or_conditions",
    "source_date_and_currentness",
}


def fail(message: str) -> None:
    raise SystemExit(f"EVIDENCE PACKET ERROR: {message}")


def is_http_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def main() -> int:
    if not PAYLOAD.exists() or not PAYLOAD.stat().st_size:
        fail("status/evidence-packet-index.json is missing or empty")
    if not CATALOG.exists() or not CATALOG.stat().st_size:
        fail("data/catalog-expanded.csv is missing or empty")

    data = json.loads(PAYLOAD.read_text(encoding="utf-8"))
    if data.get("schema_version") != "1.0":
        fail("unsupported schema_version")
    if data.get("advisory_only") is not True:
        fail("advisory_only must be true")
    if data.get("auto_promotion") is not False:
        fail("auto_promotion must be false")
    if data.get("decision_vocabulary") != ["pending", "promote", "reject", "needs-more-evidence"]:
        fail("decision vocabulary changed unexpectedly")
    if set(data.get("required_checks", [])) != REQUIRED_CHECKS:
        fail("required review checks do not match contract")

    catalog_sha256 = hashlib.sha256(CATALOG.read_bytes()).hexdigest()
    if data.get("catalog_sha256") != catalog_sha256:
        fail("catalog_sha256 does not match data/catalog-expanded.csv")

    packets = data.get("packets")
    if not isinstance(packets, list):
        fail("packets must be a list")
    if len(packets) != int(data.get("packets_shown", -1)):
        fail("packets_shown does not match packets length")
    if len(packets) > 250:
        fail("packet payload may contain at most 250 packets")

    previous_rank = 0
    ids: set[str] = set()
    for packet in packets:
        required = (
            "packet_version", "packet_status", "rank", "record_id", "record_type",
            "organization", "credential_or_badge", "official_url", "source_page",
            "observed_evidence_status", "observed_price_status", "review", "guardrails",
        )
        for key in required:
            if key not in packet:
                fail(f"packet missing {key}")
        if packet["packet_version"] != "1.0":
            fail("unsupported packet version")
        if packet["packet_status"] != "pending":
            fail("generated packets must start in pending state")
        if not isinstance(packet["rank"], int) or packet["rank"] <= previous_rank:
            fail("packet ranks must be unique and strictly increasing")
        previous_rank = packet["rank"]
        record_id = packet["record_id"]
        if not isinstance(record_id, str) or not record_id or record_id in ids:
            fail("packet record_id must be non-empty and unique")
        ids.add(record_id)
        if packet["record_type"] != "credential-candidate":
            fail("evidence packets may only be generated for credential-candidate records")
        if not packet["organization"] or not packet["credential_or_badge"]:
            fail("packet identity fields must be non-empty")
        for key in ("official_url", "source_page"):
            value = packet[key]
            if value and not is_http_url(value):
                fail(f"invalid {key}: {value!r}")

        review = packet["review"]
        if review.get("decision") != "pending":
            fail("generated review decision must be pending")
        if review.get("reviewer") or review.get("reviewed_at") or review.get("notes"):
            fail("generated review metadata must be empty")
        checks = review.get("checks")
        if not isinstance(checks, dict) or set(checks) != REQUIRED_CHECKS:
            fail("review checks do not match required set")
        if any(value is not None for value in checks.values()):
            fail("generated review checks must be null")

        guards = packet["guardrails"]
        for key in ("advisory_only", "auto_promotion", "price_is_not_proof", "reachability_is_not_status_proof", "candidate_is_not_verified"):
            if key not in guards or guards[key] is not True:
                fail(f"guardrail {key} must be true")

    for field in ("candidate_records", "packets_shown", "packet_limit", "provider_count", "providers_shown", "provider_limit"):
        if not isinstance(data.get(field), int) or data[field] < 0:
            fail(f"invalid summary field: {field}")
    if data["packets_shown"] > data["candidate_records"]:
        fail("packets_shown cannot exceed candidate_records")
    if data["providers_shown"] > data["provider_count"]:
        fail("providers_shown cannot exceed provider_count")
    if data["packets_shown"] > data["packet_limit"]:
        fail("packets_shown cannot exceed packet_limit")
    if data["providers_shown"] > data["provider_limit"]:
        fail("providers_shown cannot exceed provider_limit")

    print(f"validated_evidence_packets={len(packets)}")
    print(f"validated_evidence_candidates={data['candidate_records']}")
    print(f"validated_evidence_provider_groups={data['provider_count']}")
    print(f"validated_evidence_catalog_sha256={catalog_sha256}")
    print("evidence_packet_contract=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
