#!/usr/bin/env python3
"""Capture bounded issuer-source metadata for high-value evidence review candidates.

This tool is deliberately non-authoritative: it records HTTP/reachability metadata
and a body fingerprint only. It never changes catalog status or makes a promotion
or verification decision.
"""
from __future__ import annotations

import hashlib
import ipaddress
import json
import socket
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data/catalog-expanded.csv"
PREVIEW = ROOT / "status/promotion-preview.json"
OUT = ROOT / "status/evidence-source-capture.json"
MAX_ROWS = 50
MAX_BYTES = 1_000_000
TIMEOUT_SECONDS = 12
DELAY_SECONDS = 0.75


def http_url(value: str) -> bool:
    try:
        parsed = urlparse(value)
    except ValueError:
        return False
    return (
        parsed.scheme in {"http", "https"}
        and bool(parsed.netloc)
        and parsed.username is None
        and parsed.password is None
    )


def public_http_url(value: str) -> bool:
    if not http_url(value):
        return False
    parsed = urlparse(value)
    hostname = parsed.hostname
    if not hostname:
        return False
    try:
        address = ipaddress.ip_address(hostname)
        return address.is_global
    except ValueError:
        pass
    try:
        addresses = {
            ipaddress.ip_address(item[4][0])
            for item in socket.getaddrinfo(hostname, parsed.port or (443 if parsed.scheme == "https" else 80), type=socket.SOCK_STREAM)
        }
    except (OSError, ValueError):
        return False
    return bool(addresses) and all(address.is_global for address in addresses)


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


OPENER = build_opener(NoRedirect)


def capture(row: dict, position: int, seen: set[str]) -> dict:
    requested = str(row.get("url") or row.get("source") or "").strip()
    base = {
        "position": position,
        "name": str(row.get("name") or ""),
        "organization": str(row.get("organization") or ""),
        "score": row.get("score"),
        "tier": str(row.get("tier") or ""),
        "triage": str(row.get("triage") or ""),
        "requested_url": requested,
        "capture_status": "not_attempted",
        "http_status": None,
        "final_url": "",
        "content_type": "",
        "bytes_read": 0,
        "body_sha256": "",
        "cross_origin_redirect": False,
        "error_type": "",
    }
    if not requested:
        base["capture_status"] = "invalid_url"
        base["error_type"] = "missing_url"
        return base
    if not http_url(requested):
        base["capture_status"] = "invalid_url"
        base["error_type"] = "non_http_url_or_credentials"
        return base
    if not public_http_url(requested):
        base["capture_status"] = "blocked_url"
        base["error_type"] = "non_public_destination"
        return base
    if requested in seen:
        base["capture_status"] = "deduplicated"
        return base
    seen.add(requested)
    request = Request(
        requested,
        headers={
            "User-Agent": "OpenCertAtlas/evidence-source-capture; +https://github.com/pavlivdevelop/OpenCertAtlas",
            "Accept": "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.5",
        },
    )
    try:
        with OPENER.open(request, timeout=TIMEOUT_SECONDS) as response:
            body = response.read(MAX_BYTES + 1)
            final_url = response.geturl()
            if final_url != requested:
                base["capture_status"] = "blocked_url"
                base["http_status"] = int(getattr(response, "status", 200))
                base["final_url"] = final_url if public_http_url(final_url) else ""
                base["cross_origin_redirect"] = urlparse(final_url).netloc.lower() != urlparse(requested).netloc.lower()
                base["error_type"] = "redirect_not_followed"
                return base
            base["capture_status"] = "ok" if len(body) <= MAX_BYTES else "truncated"
            base["http_status"] = int(getattr(response, "status", 200))
            base["final_url"] = final_url
            base["content_type"] = response.headers.get_content_type() or ""
            base["bytes_read"] = min(len(body), MAX_BYTES)
            base["body_sha256"] = hashlib.sha256(body[:MAX_BYTES]).hexdigest()
    except HTTPError as exc:
        base["http_status"] = int(exc.code)
        location = exc.headers.get("Location") if exc.headers else ""
        if 300 <= exc.code < 400 and location:
            target = urljoin(requested, location)
            base["capture_status"] = "redirect_blocked"
            base["final_url"] = target if public_http_url(target) else ""
            base["cross_origin_redirect"] = urlparse(target).netloc.lower() != urlparse(requested).netloc.lower()
            base["content_type"] = exc.headers.get_content_type() if exc.headers else ""
            base["error_type"] = "redirect_not_followed"
        else:
            base["capture_status"] = "http_error"
            base["final_url"] = exc.geturl() if public_http_url(exc.geturl()) else ""
            base["content_type"] = exc.headers.get_content_type() if exc.headers else ""
            base["error_type"] = "HTTPError"
    except (URLError, TimeoutError, OSError) as exc:
        base["capture_status"] = "network_error"
        base["error_type"] = type(exc).__name__
    except Exception as exc:  # defensive: never make one source abort the whole batch
        base["capture_status"] = "capture_error"
        base["error_type"] = type(exc).__name__
    return base


def main() -> int:
    if not CATALOG.exists() or not CATALOG.stat().st_size:
        raise SystemExit(f"missing {CATALOG.relative_to(ROOT)}")
    if not PREVIEW.exists() or not PREVIEW.stat().st_size:
        raise SystemExit(f"missing {PREVIEW.relative_to(ROOT)}")
    catalog_sha256 = hashlib.sha256(CATALOG.read_bytes()).hexdigest()
    data = json.loads(PREVIEW.read_text(encoding="utf-8"))
    if data.get("advisory_only") is not True or data.get("auto_promotion") is not False:
        raise SystemExit("promotion preview must be advisory-only")
    if data.get("catalog_sha256") != catalog_sha256:
        raise SystemExit("promotion preview is stale: catalog_sha256 does not match data/catalog-expanded.csv")
    records = data.get("records")
    if not isinstance(records, list):
        raise SystemExit("promotion preview records must be a list")

    ranked = sorted(
        enumerate(records),
        key=lambda pair: (-float(pair[1].get("score") or 0), pair[0]),
    )
    selected = ranked[:MAX_ROWS]
    seen: set[str] = set()
    results = []
    for position, (_, row) in enumerate(selected, start=1):
        results.append(capture(row, position, seen))
        if position < len(selected):
            time.sleep(DELAY_SECONDS)

    payload = {
        "schema_version": "1.1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "catalog_sha256": catalog_sha256,
        "promotion_preview_schema_version": str(data.get("schema_version") or ""),
        "candidate_records": int(data.get("candidate_records") or 0),
        "capture_limit": MAX_ROWS,
        "selected_rows": len(selected),
        "unique_requested_urls": len(seen),
        "max_bytes_per_source": MAX_BYTES,
        "timeout_seconds": TIMEOUT_SECONDS,
        "redirect_policy": "do-not-follow",
        "destination_policy": "public-ip-only",
        "advisory_only": True,
        "evidence_role": "reachability-and-content-fingerprint-only",
        "promotion_authority": False,
        "verification_authority": False,
        "results": results,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"source_capture_selected={len(selected)} unique_urls={len(seen)}")
    print(f"source_capture_ok={sum(r['capture_status'] in {'ok','truncated'} for r in results)}")
    print("source_capture_authority=none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
