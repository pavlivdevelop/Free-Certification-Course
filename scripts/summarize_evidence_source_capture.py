#!/usr/bin/env python3
"""Render a human-readable, non-authoritative summary of a source-capture artifact."""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CAPTURE = ROOT / "status/evidence-source-capture.json"
SUMMARY = ROOT / "status/evidence-source-capture-summary.md"


def host(value: str) -> str:
    try:
        return (urlparse(value).hostname or "no-host").lower()
    except ValueError:
        return "no-host"


def main() -> int:
    data = json.loads(CAPTURE.read_text(encoding="utf-8"))
    results = data.get("results") or []
    statuses = Counter(str(row.get("capture_status") or "unknown") for row in results)
    http = Counter(str(row.get("http_status")) for row in results if row.get("http_status") is not None)
    groups: dict[str, dict[str, int]] = defaultdict(lambda: {"rows": 0, "ok": 0})
    for row in results:
        issuer = str(row.get("organization") or host(str(row.get("requested_url") or "")))
        groups[issuer]["rows"] += 1
        if row.get("capture_status") in {"ok", "truncated"}:
            groups[issuer]["ok"] += 1

    lines = [
        "# Evidence source capture summary",
        "",
        "> Automated reachability metadata only. This report does not establish credential identity, currentness, price, eligibility, issuer ownership, verification, or promotion authority.",
        "",
        f"- Schema: `{data.get('schema_version', '—')}`",
        f"- Catalog snapshot: `{data.get('catalog_sha256', '—')}`",
        f"- Generated: `{data.get('generated_at_utc', '—')}`",
        f"- Selected rows: **{len(results)}**",
        f"- Unique requested URLs: **{data.get('unique_requested_urls', 0)}**",
        f"- Redirect policy: `{data.get('redirect_policy', '—')}`",
        f"- Destination policy: `{data.get('destination_policy', '—')}`",
        "",
        "## Capture status",
        "",
        "| Status | Rows |",
        "| --- | ---: |",
    ]
    lines.extend(f"| `{name}` | {count} |" for name, count in sorted(statuses.items()))
    lines += [
        "",
        "## HTTP observations",
        "",
        "| HTTP status | Rows |",
        "| --- | ---: |",
    ]
    lines.extend(f"| `{code}` | {count} |" for code, count in sorted(http.items(), key=lambda item: item[0]))
    lines += [
        "",
        "## Issuer groups observed",
        "",
        "| Issuer | Rows | Successful observations |",
        "| --- | ---: | ---: |",
    ]
    for issuer, counts in sorted(groups.items(), key=lambda item: (-item[1]["rows"], item[0].lower())):
        safe = issuer.replace("|", "\\|")
        lines.append(f"| {safe} | {counts['rows']} | {counts['ok']} |")
    lines += [
        "",
        "## Review boundary",
        "",
        "Successful HTTP reachability is only a prioritization signal. Any authoritative promotion still requires the controlled evidence-review process and issuer-controlled sources.",
        "",
    ]
    SUMMARY.write_text("\n".join(lines), encoding="utf-8")
    print(f"source_capture_summary_rows={len(results)}")
    print(f"source_capture_summary_groups={len(groups)}")
    print("source_capture_summary=written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
