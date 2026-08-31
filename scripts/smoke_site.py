#!/usr/bin/env python3
"""Fast, dependency-free smoke tests for the portable OpenCertAtlas web UI."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "site" / "index.html"
PROGRESS = ROOT / "site" / "progress.html"


def fail(message: str) -> None:
    raise SystemExit(f"SITE SMOKE ERROR: {message}")


def main() -> int:
    for path in (INDEX, PROGRESS):
        if not path.exists():
            fail(f"missing {path.relative_to(ROOT)}")

    index = INDEX.read_text(encoding="utf-8")
    progress = PROGRESS.read_text(encoding="utf-8")

    required_index = {
        "OpenCertAtlas": "canonical brand",
        "catalog-expanded.json": "catalog data source",
        "localStorage": "local progress persistence",
        "Export": "progress export hook",
        "Import": "progress import hook",
        "Official URL": "official source link field",
    }
    for needle, label in required_index.items():
        if needle not in index:
            fail(f"index.html missing {label}: {needle!r}")

    required_progress = {
        "Certification Progress": "tracker heading",
        "localStorage": "local persistence",
        "my-certification-progress.json": "portable export filename",
        "completed": "completion state",
        "in_progress": "in-progress state",
    }
    for needle, label in required_progress.items():
        if needle not in progress:
            fail(f"progress.html missing {label}: {needle!r}")

    legacy = (index + "\n" + progress).lower()
    for forbidden in ("free certification course", "fcc-progress"):
        if forbidden in legacy:
            fail(f"legacy branding/storage key detected: {forbidden!r}")

    for path in (INDEX, PROGRESS):
        if "₽" in path.read_text(encoding="utf-8"):
            fail(f"currency-specific ₽ marker remains in {path.relative_to(ROOT)}")

    print("site_smoke=passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
