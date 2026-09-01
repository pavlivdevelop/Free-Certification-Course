#!/usr/bin/env python3
"""Generate a deterministic, advisory promotion preview without mutating catalog records."""
from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import defaultdict
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

# Discovery often finds learning-content pages whose titles look like credentials.
# These signals only affect review ordering; they never reject or promote a record.
CREDENTIAL_TERMS = (
    "certificate",
    "certification",
    "certified",
    "credential",
    "digital badge",
    "badge",
    "microcredential",
    "professional certificate",
    "exam",
    "assessment",
)
LEARNING_TITLE_TERMS = (
    "course",
    "training",
    "tutorial",
    "introduction",
    "fundamentals",
    "getting started",
    "101",
    "lesson",
    "workshop",
    "bootcamp",
    "beginner",
    "guide",
    "learning path",
    "academy",
)
LEARNING_PATH_TERMS = (
    "/course",
    "/courses/",
    "/learn/",
    "/training",
    "/tutorial",
    "/lessons/",
    "/workshop",
)
TOKEN_RE = re.compile(r"[^a-z0-9]+", re.I)


def is_http_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def hostname(value: str) -> str:
    if not is_http_url(value):
        return ""
    return urlparse(value).hostname or ""


def credential_identity_signals(name: str, url: str) -> tuple[int, str, list[str]]:
    normalized_name = " " + TOKEN_RE.sub(" ", name.casefold()).strip() + " "
    normalized_url = url.casefold()
    positive = [term for term in CREDENTIAL_TERMS if term in normalized_name]
    learning_title = [term for term in LEARNING_TITLE_TERMS if term in normalized_name]
    learning_path = [term for term in LEARNING_PATH_TERMS if term in normalized_url]

    score = 0
    reasons: list[str] = []
    if positive:
        score += min(3, len(positive))
        reasons.append("credential language in title")
    if learning_title:
        score -= min(3, len(learning_title))
        reasons.append("learning-content language in title")
    if learning_path:
        score -= 3
        reasons.append("learning-content URL pattern")

    if positive and not learning_title:
        triage = "likely credential identity"
    elif learning_title or learning_path:
        triage = "learning-content signal"
    else:
        triage = "uncertain credential identity"
    return score, triage, reasons


def provider_key(organization: str, url: str) -> tuple[str, str]:
    """Stable issuer grouping key: organization plus official host."""
    org = organization.strip() or "Unspecified organization"
    host = hostname(url).casefold()
    return org, host or "no-host"


def main() -> int:
    catalog_bytes = CAT.read_bytes()
    catalog_sha256 = hashlib.sha256(catalog_bytes).hexdigest()
    with CAT.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    candidates = [r for r in rows if r.get("Record Type", "").strip() == "credential-candidate"]
    proposals: list[dict] = []
    providers: dict[tuple[str, str], dict[str, int | str]] = defaultdict(lambda: {
        "organization": "",
        "host": "",
        "candidate_records": 0,
        "reviewable": 0,
        "high_confidence": 0,
        "likely_credential_identity": 0,
        "learning_content_signals": 0,
        "uncertain_credential_identity": 0,
    })

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

        identity_delta, triage, identity_reasons = credential_identity_signals(name, url)
        score = max(0, score + identity_delta)
        reasons.extend(identity_reasons)

        if score >= 8:
            tier = "high-confidence review candidate"
        elif score >= 6:
            tier = "review candidate"
        else:
            tier = "needs additional evidence"

        proposals.append({
            "score": score,
            "tier": tier,
            "triage": triage,
            "organization": org,
            "name": name,
            "evidence": evidence or "unclassified",
            "method": method or "unknown",
            "url": url,
            "source": source,
            "reasons": reasons,
        })

        org_key, host_key = provider_key(org, url)
        aggregate = providers[(org_key, host_key)]
        aggregate["organization"] = org_key
        aggregate["host"] = host_key
        aggregate["candidate_records"] = int(aggregate["candidate_records"]) + 1
        aggregate["reviewable"] = int(aggregate["reviewable"]) + int(score >= 6)
        aggregate["high_confidence"] = int(aggregate["high_confidence"]) + int(score >= 8)
        aggregate["likely_credential_identity"] = int(aggregate["likely_credential_identity"]) + int(triage == "likely credential identity")
        aggregate["learning_content_signals"] = int(aggregate["learning_content_signals"]) + int(triage == "learning-content signal")
        aggregate["uncertain_credential_identity"] = int(aggregate["uncertain_credential_identity"]) + int(triage == "uncertain credential identity")

    proposals.sort(key=lambda x: (-x["score"], x["tier"], x["triage"], x["organization"].casefold(), x["name"].casefold()))
    provider_rows = sorted(
        providers.values(),
        key=lambda x: (
            -int(x["reviewable"]),
            -int(x["high_confidence"]),
            -int(x["candidate_records"]),
            str(x["organization"]).casefold(),
            str(x["host"]).casefold(),
        ),
    )
    high = sum(p["score"] >= 8 for p in proposals)
    reviewable = sum(p["score"] >= 6 for p in proposals)
    likely_credentials = sum(p["triage"] == "likely credential identity" for p in proposals)
    learning_signals = sum(p["triage"] == "learning-content signal" for p in proposals)

    JSON_OUT.write_text(json.dumps({
        "schema_version": "1.3",
        "catalog_sha256": catalog_sha256,
        "candidate_records": len(candidates),
        "reviewable": reviewable,
        "high_confidence": high,
        "likely_credential_identity": likely_credentials,
        "learning_content_signals": learning_signals,
        "provider_count": len(provider_rows),
        "providers_shown": min(100, len(provider_rows)),
        "rows_shown": min(500, len(proposals)),
        "advisory_only": True,
        "auto_promotion": False,
        "providers": provider_rows[:100],
        "records": proposals[:500],
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Promotion preview",
        "",
        f"- candidate records reviewed: {len(candidates)}",
        f"- deterministic review candidates (score ≥ 6): {reviewable}",
        f"- high-confidence review candidates (score ≥ 8): {high}",
        f"- likely credential identities: {likely_credentials}",
        f"- learning-content signals: {learning_signals}",
        f"- issuer/provider groups: {len(provider_rows)} (top {min(100, len(provider_rows))} shown)",
        f"- rows shown: {min(500, len(proposals))}",
        f"- catalog SHA-256: `{catalog_sha256}`",
        "",
        "This report is advisory only. It never changes catalog records, Evidence Status, or free status.",
        "Credential-language and learning-content heuristics affect triage only; they are not proof of credential identity.",
        "Provider aggregation is for batch review and does not imply that all rows from a provider share the same evidence quality.",
        "A row is not eligible for automatic promotion merely because it scores highly.",
        "Manual review must confirm the issuer page, credential-bearing activity, current free route, eligibility and source date before any promotion decision.",
        "",
        "## Issuer/provider review groups",
        "",
        "| Provider | Official host | Candidates | Reviewable | High-confidence | Likely credential | Learning signal | Uncertain |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for p in provider_rows[:100]:
        def cell(value: str) -> str:
            return str(value or "").replace("|", "\\|").replace("\n", " ")
        lines.append(
            f"| {cell(str(p['organization']))} | {cell(str(p['host']))} | {p['candidate_records']} | {p['reviewable']} | {p['high_confidence']} | "
            f"{p['likely_credential_identity']} | {p['learning_content_signals']} | {p['uncertain_credential_identity']} |"
        )
    lines.extend([
        "",
        "## Candidate records",
        "",
        "| Score | Tier | Triage | Organization | Candidate | Evidence | Method | Official URL | Reasons |",
        "|---:|---|---|---|---|---|---|---|---|",
    ])
    for p in proposals[:500]:
        def cell(value: str) -> str:
            return str(value or "").replace("|", "\\|").replace("\n", " ")
        lines.append(
            f"| {p['score']} | {cell(p['tier'])} | {cell(p['triage'])} | {cell(p['organization'])} | {cell(p['name'])} | "
            f"{cell(p['evidence'])} | {cell(p['method'])} | {cell(p['url'])} | {cell('; '.join(p['reasons']))} |"
        )

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"promotion_candidates={len(candidates)}")
    print(f"promotion_reviewable={reviewable}")
    print(f"promotion_high_confidence={high}")
    print(f"promotion_likely_credential_identity={likely_credentials}")
    print(f"promotion_learning_content_signals={learning_signals}")
    print(f"promotion_provider_count={len(provider_rows)}")
    print(f"promotion_catalog_sha256={catalog_sha256}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
