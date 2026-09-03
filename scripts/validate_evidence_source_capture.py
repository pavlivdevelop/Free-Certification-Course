#!/usr/bin/env python3
"""Validate the non-authoritative source-metadata capture artifact."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
PREVIEW = ROOT / "status/promotion-preview.json"
CAPTURE = ROOT / "status/evidence-source-capture.json"
ALLOWED = {"ok", "truncated", "invalid_url", "deduplicated", "http_error", "network_error", "capture_error", "not_attempted"}


def fail(message: str) -> None:
    raise SystemExit(f"SOURCE CAPTURE ERROR: {message}")


def is_http_url(value: str) -> bool:
    try:
        parsed = urlparse(value)
    except ValueError:
        return False
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def main() -> int:
    if not PREVIEW.exists() or not PREVIEW.stat().st_size:
        fail("promotion preview is missing")
    if not CAPTURE.exists() or not CAPTURE.stat().st_size:
        fail("capture artifact is missing or empty")
    preview = json.loads(PREVIEW.read_text(encoding="utf-8"))
    data = json.loads(CAPTURE.read_text(encoding="utf-8"))
    if preview.get("advisory_only") is not True or preview.get("auto_promotion") is not False:
        fail("source capture must consume an advisory-only promotion preview")
    if data.get("schema_version") != "1.0":
        fail("unsupported schema_version")
    if data.get("advisory_only") is not True:
        fail("advisory_only must be true")
    if data.get("promotion_authority") is not False:
        fail("promotion_authority must be false")
    if data.get("verification_authority") is not False:
        fail("verification_authority must be false")
    if data.get("evidence_role") != "reachability-and-content-fingerprint-only":
        fail("unexpected evidence role")
    if data.get("catalog_sha256") != preview.get("catalog_sha256"):
        fail("catalog snapshot binding does not match promotion preview")
    if data.get("promotion_preview_schema_version") != preview.get("schema_version"):
        fail("promotion preview schema binding does not match")
    results = data.get("results")
    if not isinstance(results, list) or len(results) > 50:
        fail("results must be a bounded list of at most 50 rows")
    for result in results:
        for key in ("position", "requested_url", "capture_status", "http_status", "final_url", "content_type", "bytes_read", "body_sha256", "cross_origin_redirect", "error_type"):
            if key not in result:
                fail(f"result missing {key}")
        if result["capture_status"] not in ALLOWED:
            fail(f"unknown capture_status: {result['capture_status']!r}")
        if result["requested_url"] and not is_http_url(result["requested_url"]):
            fail(f"non-http requested URL: {result['requested_url']!r}")
        if result["final_url"] and not is_http_url(result["final_url"]):
            fail(f"non-http final URL: {result['final_url']!r}")
        if not isinstance(result["position"], int) or result["position"] <= 0:
            fail("positions must be positive integers")
        if not isinstance(result["bytes_read"], int) or result["bytes_read"] < 0 or result["bytes_read"] > 1_000_000:
            fail("bytes_read is outside the capture bound")
        if result["body_sha256"] and len(result["body_sha256"]) != 64:
            fail("body_sha256 must be a SHA-256 hex digest")
        if result["capture_status"] == "ok" and (result["http_status"] is None or not result["body_sha256"]):
            fail("successful capture must include HTTP status and body fingerprint")
        if any(key in result for key in ("decision", "reviewer", "notes", "verified", "price_status", "evidence_status")):
            fail("capture result must not contain promotion/review authority fields")
    print(f"validated_source_capture_rows={len(results)}")
    print(f"validated_source_capture_unique_urls={data.get('unique_requested_urls', 0)}")
    print("source_capture_contract=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
