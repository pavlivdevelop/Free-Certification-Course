#!/usr/bin/env python3
"""Validate the generated credential-to-pathway candidate mapping contract."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATHWAYS = ROOT / "taxonomy" / "pathways.json"
MAPPINGS = ROOT / "status" / "CREDENTIAL-PATHWAY-CANDIDATES.csv"
LITE = ROOT / "data" / "pathway-candidates-lite.json"


def main() -> int:
    taxonomy = json.loads(PATHWAYS.read_text(encoding="utf-8"))
    valid_nodes = set(taxonomy.get("node_levels", {}))
    with MAPPINGS.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    if not rows:
        raise SystemExit("mapping candidate CSV is empty")

    seen = set()
    for row in rows:
        key = (row.get("credential_id", ""), row.get("pathway_node", ""))
        if key in seen:
            raise SystemExit(f"duplicate mapping: {key}")
        seen.add(key)
        if not row.get("credential_id"):
            raise SystemExit("mapping row has empty credential_id")
        if row.get("pathway_node") not in valid_nodes:
            raise SystemExit(f"unknown pathway node: {row.get('pathway_node')}")
        if row.get("mapping_status") != "candidate":
            raise SystemExit("mapping status must remain candidate")
        score = int(row.get("match_score", "0"))
        if score < 35 or score > 100:
            raise SystemExit(f"invalid match score: {score}")

        # This payload is explicitly forbidden from acting as verification state.
        if row.get("mapping_status") in {"verified", "promoted", "authoritative"}:
            raise SystemExit("authoritative mapping status is forbidden")

    lite = json.loads(LITE.read_text(encoding="utf-8"))
    if not isinstance(lite, list) or len(lite) != len(rows):
        raise SystemExit("lite mapping payload must be a list with matching row count")
    for item in lite:
        if item.get("mapping_status") != "candidate":
            raise SystemExit("lite mapping payload contains non-candidate status")

    print(f"validated_mapping_rows={len(rows)}")
    print(f"validated_mapping_credentials={len({r['credential_id'] for r in rows})}")
    print(f"validated_mapping_nodes={len({r['pathway_node'] for r in rows})}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
