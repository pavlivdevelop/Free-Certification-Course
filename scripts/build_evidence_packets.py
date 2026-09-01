#!/usr/bin/env python3
"""Generate bounded, issuer-grouped manual evidence packets.

Packets are review scaffolds only. They preserve observed catalog facts and URLs,
add an explicit checklist, and never infer verification, price, eligibility, or
credential identity. Every packet starts in a pending state.
"""
from __future__ import annotations

import csv
import hashlib
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data/catalog-expanded.csv"
OUT = ROOT / "status/evidence-packet-index.json"
SUMMARY = ROOT / "status/EVIDENCE-PACKETS-SUMMARY.md"
MAX_PACKETS = 250
MAX_PROVIDERS = 100

REQUIRED_CHECKS = (
    "credential_identity",
    "credential_bearing_activity",
    "current_access_or_price",
    "eligibility_or_conditions",
    "source_date_and_currentness",
)


def host(url: str) -> str:
    try:
        parsed = urlparse(url)
    except ValueError:
        return ""
    return (parsed.hostname or "").casefold()


def provider_key(row: dict[str, str]) -> tuple[str, str]:
    org = (row.get("Organization") or "Unspecified organization").strip()
    return org, host(row.get("Official URL", "")) or "no-host"


def packet_for(row: dict[str, str], rank: int) -> dict:
    return {
        "packet_version": "1.0",
        "packet_status": "pending",
        "rank": rank,
        "record_id": row.get("ID", ""),
        "record_type": row.get("Record Type", ""),
        "organization": row.get("Organization", ""),
        "credential_or_badge": row.get("Certificate/Badge", ""),
        "category": row.get("Category", ""),
        "official_url": row.get("Official URL", ""),
        "source_page": row.get("Source Page", ""),
        "observed_evidence_status": row.get("Evidence Status", ""),
        "observed_price_status": row.get("Price Status", ""),
        "observed_extraction_method": row.get("Extraction Method", ""),
        "observed_extraction_date": row.get("Extraction Date", ""),
        "review": {
            "decision": "pending",
            "reviewer": "",
            "reviewed_at": "",
            "notes": "",
            "checks": {name: None for name in REQUIRED_CHECKS},
        },
        "guardrails": {
            "advisory_only": True,
            "auto_promotion": False,
            "price_is_not_proof": True,
            "reachability_is_not_status_proof": True,
            "candidate_is_not_verified": True,
        },
    }


def main() -> int:
    if not CATALOG.exists():
        raise SystemExit(f"missing {CATALOG.relative_to(ROOT)}")

    catalog_sha256 = hashlib.sha256(CATALOG.read_bytes()).hexdigest()
    with CATALOG.open("r", encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))

    candidates = [r for r in rows if (r.get("Record Type") or "").strip() == "credential-candidate"]
    # Keep the packet set deterministic and aligned with promotion-preview ordering inputs.
    candidates.sort(key=lambda r: (
        (r.get("Organization") or "").casefold(),
        host(r.get("Official URL", "")),
        (r.get("Certificate/Badge") or "").casefold(),
        r.get("ID") or "",
    ))

    groups: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in candidates:
        groups[provider_key(row)].append(row)

    packets = [packet_for(row, rank) for rank, row in enumerate(candidates[:MAX_PACKETS], start=1)]
    providers = []
    for (organization, provider_host), provider_rows in sorted(
        groups.items(),
        key=lambda item: (-len(item[1]), item[0][0].casefold(), item[0][1]),
    )[:MAX_PROVIDERS]:
        shown_ids = [row.get("ID", "") for row in provider_rows if row.get("ID")][:25]
        providers.append({
            "organization": organization,
            "host": provider_host,
            "candidate_records": len(provider_rows),
            "packet_rows_shown": sum(1 for p in packets if p["organization"] == organization and host(p["official_url"]) == provider_host),
            "candidate_ids_sample": shown_ids,
        })

    generated_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    payload = {
        "schema_version": "1.0",
        "generated_at": generated_at,
        "catalog_sha256": catalog_sha256,
        "candidate_records": len(candidates),
        "packets_shown": len(packets),
        "packet_limit": MAX_PACKETS,
        "provider_count": len(groups),
        "providers_shown": len(providers),
        "provider_limit": MAX_PROVIDERS,
        "decision_vocabulary": ["pending", "promote", "reject", "needs-more-evidence"],
        "advisory_only": True,
        "auto_promotion": False,
        "required_checks": list(REQUIRED_CHECKS),
        "providers": providers,
        "packets": packets,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Evidence packet summary",
        "",
        f"Generated: {generated_at}",
        "",
        f"- Candidate records: **{len(candidates):,}**",
        f"- Packets shown: **{len(packets):,}**",
        f"- Issuer groups: **{len(groups):,}** (top {len(providers):,} shown)",
        f"- Catalog SHA-256: `{catalog_sha256}`",
        "",
        "## Purpose",
        "",
        "These packets are bounded, deterministic review scaffolds. They preserve observed catalog facts and source URLs, but they do not assert that a candidate is a credential, verified, current, free, or eligible for promotion.",
        "",
        "## Required human checks",
        "",
        "1. Confirm exact credential identity on the issuer-controlled source.",
        "2. Confirm credential-bearing activity (certificate, certification, badge or equivalent), not merely a course/training page.",
        "3. Confirm the current access/price route and record conditions precisely.",
        "4. Confirm eligibility, exclusions, vouchers, partner/student rules or other conditions.",
        "5. Record the source date/currentness and a concise reviewer note.",
        "",
        "The starting decision is always `pending`. No packet field grants automatic promotion authority.",
    ]
    SUMMARY.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"evidence_packet_candidates={len(candidates)} packets_shown={len(packets)} providers={len(groups)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
