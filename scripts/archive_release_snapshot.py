#!/usr/bin/env python3
"""Archive the current release manifest and maintain a deterministic release index."""
from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "status" / "release-manifest.json"
ARCHIVE_DIR = ROOT / "status" / "releases"
INDEX = ROOT / "status" / "release-index.json"


def safe_part(value: str) -> str:
    return re.sub(r"[^0-9A-Za-z._-]+", "-", value).strip("-") or "unknown"


def main() -> int:
    if not MANIFEST.exists():
        raise SystemExit("release-manifest.json is missing")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    generated = str(manifest.get("generated_at_utc", ""))
    timestamp = datetime.fromisoformat(generated.replace("Z", "+00:00")) if generated else datetime.now(timezone.utc)
    stamp = timestamp.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    trigger = safe_part(str(manifest.get("build_trigger_sha", "local")))[:12]
    archive_name = f"{stamp}-{trigger}.json"
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    archive_path = ARCHIVE_DIR / archive_name
    archive_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    entries = []
    for path in sorted(ARCHIVE_DIR.glob("*.json"), reverse=True):
        try:
            item = json.loads(path.read_text(encoding="utf-8"))
            entries.append({
                "snapshot": path.relative_to(ROOT).as_posix(),
                "generated_at_utc": item.get("generated_at_utc"),
                "build_trigger_sha": item.get("build_trigger_sha"),
                "catalog_records": item.get("catalog", {}).get("records", 0),
                "verified_free_core": item.get("catalog", {}).get("verified_free_core", 0),
                "candidates": item.get("catalog", {}).get("candidates", 0),
            })
        except (OSError, ValueError, TypeError):
            continue

    index = {
        "index_version": "1.0",
        "project": "OpenCertAtlas",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "snapshot_count": len(entries),
        "snapshots": entries,
    }
    INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"release_snapshot={archive_path.relative_to(ROOT)}")
    print(f"release_snapshot_count={len(entries)}")
    print(f"release_trigger_sha={os.environ.get('GITHUB_SHA', 'local')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
