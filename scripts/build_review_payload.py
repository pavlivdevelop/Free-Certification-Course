#!/usr/bin/env python3
"""Build a compact browser payload for the human review queue.

The canonical review queue may be several megabytes, which is appropriate for
machine/archive use but unnecessarily expensive for the public site. This script
creates a small, deterministic top-of-queue payload plus a reviewer-facing summary.
It never promotes records or changes evidence status.
"""
from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "status/REVIEW-QUEUE.csv"
JSON_OUT = ROOT / "status/review-queue-lite.json"
MD_OUT = ROOT / "status/REVIEW-QUEUE-SUMMARY.md"
MAX_BROWSER_RECORDS = 600


def main() -> int:
    if not INPUT.exists():
        raise SystemExit(f"missing {INPUT.relative_to(ROOT)}")

    with INPUT.open("r", encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))

    rows.sort(
        key=lambda r: (
            int(r.get("Queue Priority", "99") or 99),
            (r.get("Organization") or "").casefold(),
            (r.get("Certificate/Badge") or "").casefold(),
            r.get("ID") or "",
        )
    )

    by_priority = Counter(r.get("Queue Priority", "") for r in rows)
    by_reason = Counter(r.get("Review Reason", "") for r in rows)
    generated_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    payload = {
        "schema_version": "1.0",
        "generated_at": generated_at,
        "total": len(rows),
        "browser_limit": MAX_BROWSER_RECORDS,
        "priorities": {k: by_priority[k] for k in sorted(by_priority, key=lambda x: int(x or 99))},
        "review_reasons": dict(sorted(by_reason.items(), key=lambda item: (item[0], item[1]))),
        "records": [
            {
                "queue_priority": int(r.get("Queue Priority", "99") or 99),
                "review_reason": r.get("Review Reason", ""),
                "id": r.get("ID", ""),
                "organization": r.get("Organization", ""),
                "name": r.get("Certificate/Badge", ""),
                "record_type": r.get("Record Type", ""),
                "category": r.get("Category", ""),
                "price_status": r.get("Price Status", ""),
                "evidence_status": r.get("Evidence Status", ""),
                "official_url": r.get("Official URL", ""),
                "source_page": r.get("Source Page", ""),
                "last_reviewed": r.get("Last Reviewed", ""),
                "current_priority": r.get("Current Priority", ""),
            }
            for r in rows[:MAX_BROWSER_RECORDS]
        ],
    }

    JSON_OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Review queue summary",
        "",
        f"Generated: {generated_at}",
        "",
        f"- Queue records: **{len(rows):,}**",
        f"- Browser batch: **{min(len(rows), MAX_BROWSER_RECORDS):,}**",
        "- Promotion: **manual only**; this artifact does not change Evidence Status.",
        "",
        "## Priority distribution",
        "",
        "| Priority | Meaning | Records |",
        "| ---: | --- | ---: |",
        "| 10 | Candidate with free-price signal | " + f"{by_priority.get('10', 0):,} |",
        "| 15 | Credential free-price signal needs promotion review | " + f"{by_priority.get('15', 0):,} |",
        "| 20 | Candidate credential identity needs verification | " + f"{by_priority.get('20', 0):,} |",
        "| 30 | Credential needs issuer-level evidence review | " + f"{by_priority.get('30', 0):,} |",
        "",
        "## Operating rule",
        "",
        "Reviewers should verify the credential identity and the current issuer evidence before changing any canonical record. Free-price signals are leads, not proof of permanent free access.",
        "",
        "The public review page intentionally exposes only the deterministic top batch. The full CSV remains the archival working queue.",
    ]
    MD_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"review_queue_total={len(rows)} browser_records={min(len(rows), MAX_BROWSER_RECORDS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
