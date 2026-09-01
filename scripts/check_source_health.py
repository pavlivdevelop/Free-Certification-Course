#!/usr/bin/env python3
"""Probe issuer seed URLs and publish a compact source-health report.

Reachability is operational metadata only. A reachable URL is not evidence that a
credential is free, current, or even a credential page.

Report schema: source-health/v1.
"""
from __future__ import annotations

import csv
import datetime as dt
import json
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
PROVIDER_FILES = [ROOT / "providers/providers.csv", ROOT / "providers/providers-additional.csv"]
OUT_JSON = ROOT / "status/source-health.json"
OUT_MD = ROOT / "status/SOURCE-HEALTH.md"
TIMEOUT = 18
MAX_WORKERS = 16
UA = "OpenCertAtlas/2026 (+https://github.com/pavlivdevelop/OpenCertAtlas)"


def load_providers() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for path in PROVIDER_FILES:
        if not path.exists():
            continue
        with path.open(encoding="utf-8-sig", newline="") as fh:
            for row in csv.DictReader(fh):
                org = (row.get("Organization") or row.get("organization") or row.get("name") or "").strip()
                url = (row.get("Official URL") or row.get("official_url") or "").strip()
                country = (row.get("Country") or row.get("country") or "International").strip()
                if not org or not url or not url.startswith(("http://", "https://")):
                    continue
                key = (org.casefold(), url)
                if key in seen:
                    continue
                seen.add(key)
                rows.append({"organization": org, "country": country, "url": url})
    return rows


def probe(provider: dict[str, str]) -> dict[str, object]:
    url = provider["url"]
    req = Request(url, headers={"User-Agent": UA, "Accept": "text/html,application/xhtml+xml"}, method="GET")
    started = time.monotonic()
    try:
        with urlopen(req, timeout=TIMEOUT) as response:
            elapsed = round((time.monotonic() - started) * 1000)
            status = int(response.status)
            final_url = response.geturl()
            state = "reachable" if 200 <= status < 400 else "http-error"
            return {**provider, "state": state, "http_status": status, "final_url": final_url, "latency_ms": elapsed, "error": ""}
    except HTTPError as exc:
        elapsed = round((time.monotonic() - started) * 1000)
        status = int(exc.code)
        state = "reachable-restricted" if status in (401, 403, 405, 429) else "http-error"
        return {**provider, "state": state, "http_status": status, "final_url": exc.geturl(), "latency_ms": elapsed, "error": str(exc.reason)}
    except (URLError, TimeoutError, OSError) as exc:
        elapsed = round((time.monotonic() - started) * 1000)
        return {**provider, "state": "unreachable", "http_status": None, "final_url": url, "latency_ms": elapsed, "error": str(exc)}


def main() -> int:
    providers = load_providers()
    items: list[dict[str, object]] = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = [pool.submit(probe, provider) for provider in providers]
        for future in as_completed(futures):
            items.append(future.result())
    items.sort(key=lambda x: str(x["organization"]).casefold())

    states = Counter(str(item["state"]) for item in items)
    generated = dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")
    payload = {
        "schema_version": "1.0",
        "generated_at": generated,
        "total": len(items),
        "states": dict(sorted(states.items())),
        "items": items,
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Source health",
        "",
        f"Generated: {generated}",
        "",
        f"- Provider seed URLs checked: **{len(items):,}**",
        f"- Reachable: **{states.get('reachable', 0):,}**",
        f"- Reachable but restricted/rate-limited: **{states.get('reachable-restricted', 0):,}**",
        f"- HTTP errors: **{states.get('http-error', 0):,}**",
        f"- Unreachable: **{states.get('unreachable', 0):,}**",
        "",
        "## Interpretation",
        "",
        "This report measures source reachability only. Reachability does not prove credential existence, price, eligibility, validity, or verification status.",
        "",
        "The public dashboard exposes provider-level health to avoid presenting a false sense of precision for individual credentials.",
    ]
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"providers={len(items)} states={dict(states)} workers={MAX_WORKERS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
