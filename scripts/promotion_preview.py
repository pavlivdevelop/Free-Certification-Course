#!/usr/bin/env python3
"""Generate a deterministic, advisory promotion preview without mutating catalog records."""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CAT = ROOT / "data/catalog-expanded.csv"
OUT = ROOT / "status/promotion-preview.md"
JSON_OUT = ROOT / "status/promotion-preview.json"

METHOD_WEIGHTS = {
    "jsonld": 3,
    "heading": 2,
    "table": 2,
    "list": 1,
    "link-text": 1,
    "curated": 1,
}
EVIDENCE_WEIGHTS = {
    "official-page": 3,
    "official-page-extraction": 2,
    "manual-review": 1,
}


def is_http_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def main() -> int:
    catalog_bytes = CAT.read_bytes()
    catalog_sha256 = hashlib.sha256(catalog_bytes).hexdigest()
    with CAT.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    candidates = [r for r in rows if r.get("Record Type", "").strip() == "credential-candidate"]
    proposals = []
    for r in candidates:
        evidence = r.get("Evidence Status", "").strip().lower()
        method = r.get("Extraction Method", "").strip().lower()
        url = r.get("Official URL", "").strip()
        source = r.get("Source Page", "").strip()
        name = r.get("Certificate/Badge", "").strip()
        org = r.get("Organization", "").strip()

        score = 0
        reasons: list[str] = []
        ew = EVIDENCE_WEIGHTS.get(evidence, 0)
        if ew:
            score += ew
            reasons.append(f"evidence={evidence}")
        mw = METHOD_WEIGHTS.get(method, 0)
        if mw:
            score += mw
            reasons.append(f"method={method}")
        if is_http_url(url):
            score += 2
            reasons.append("official URL present")
        if is_http_url(source):
            score += 1
            reasons.append("source page present")
        if len(name) >= 6 and name.casefold() not in {"course", "training", "academy"}:
            score += 1
            reasons.append("specific credential name")

        if score >= 8:
            tier = "high-confidence review candidate"
        elif score >= 6:
            tier = "review candidate"
        else:
            tier = "needs additional evidence"

        proposals.append({
            "score": score,
            "tier": tier,
            "organization": org,
            "name": name,
            "evidence": evidence or "unclassified",
            "method": method or "unknown",
            "url": url,
            "source": source,
            "reasons": reasons,
        })

    proposals.sort(key=lambda x: (-x["score"], x["tier"], x["organization"].casefold(), x["name"].casefold()))
    high = sum(p["score"] >= 8 for p in proposals)
    reviewable = sum(p["score"] >= 6 for p in proposals)

    JSON_OUT.write_text(json.dumps({
        "schema_version": "1.1",
        "catalog_sha256": catalog_sha256,
        "candidate_records": len(candidates),
        "reviewable": reviewable,
        "high_confidence": high,
        "rows_shown": min(500, len(proposals)),
        "advisory_only": True,
        "auto_promotion": False,
        "records": proposals[:500],
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Promotion preview",
        "",
        f"- candidate records reviewed: {len(candidates)}",
        f"- deterministic review candidates (score ≥ 6): {reviewable}",
        f"- high-confidence review candidates (score ≥ 8): {high}",
        f"- rows shown: {min(500, len(proposals))}",
        f"- catalog SHA-256: `{catalog_sha256}`",
        "",
        "This report is advisory only. It never changes catalog records, Evidence Status, or free status.",
        "A row is not eligible for automatic promotion merely because it scores highly.",
        "Manual review must confirm the issuer page, credential-bearing activity, current free route, and eligibility before any promotion decision.",
        "",
        "| Score | Tier | Organization | Candidate | Evidence | Method | Official URL | Reasons |",
        "|---:|---|---|---|---|---|---|---|",
    ]
    for p in proposals[:500]:
        def cell(value: str) -> str:
            return str(value or "").replace("|", "\\|").replace("\n", " ")
        lines.append(
            f"| {p['score']} | {cell(p['tier'])} | {cell(p['organization'])} | {cell(p['name'])} | "
            f"{cell(p['evidence'])} | {cell(p['method'])} | {cell(p['url'])} | {cell('; '.join(p['reasons']))} |"
        )

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"promotion_candidates={len(candidates)}")
    print(f"promotion_reviewable={reviewable}")
    print(f"promotion_high_confidence={high}")
    print(f"promotion_catalog_sha256={catalog_sha256}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
