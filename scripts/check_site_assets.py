#!/usr/bin/env python3
"""Verify that local web assets referenced by OpenCertAtlas actually exist."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"

HTML_FILES = [SITE / name for name in ("index.html", "progress.html", "recommend.html", "pathways.html", "offline.html")]
SW_FILE = SITE / "sw.js"
IGNORED_SCHEMES = {"http", "https", "mailto", "javascript", "data", "blob", "tel"}


def fail(message: str) -> None:
    raise SystemExit(f"ASSET ERROR: {message}")


def local_target(source: Path, raw_url: str) -> Path | None:
    value = raw_url.strip().strip("'\"")
    if not value or value.startswith("#"):
        return None
    parsed = urlparse(value)
    if parsed.scheme in IGNORED_SCHEMES or parsed.netloc:
        return None
    path = parsed.path
    if not path:
        return None
    # Ignore templated/dynamic URLs because their value is not statically knowable.
    if any(token in path for token in ("${", "{{", "<", ">")):
        return None
    return (source.parent / path).resolve()


def inspect_file(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    checked = 0
    patterns = [
        r"(?:href|src|action)=[\"']([^\"']+)[\"']",
        r"(?:fetch|import)\(\s*[\"']([^\"']+)[\"']",
        r"(?:cache\.addAll|cache\.add)\(\s*[\"']([^\"']+)[\"']",
    ]
    for pattern in patterns:
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            target = local_target(path, match.group(1))
            if target is None:
                continue
            checked += 1
            try:
                target.relative_to(ROOT)
            except ValueError:
                fail(f"{path.relative_to(ROOT)} references path outside repository: {match.group(1)!r}")
            if not target.exists():
                fail(f"{path.relative_to(ROOT)} references missing local asset: {match.group(1)!r}")
    return checked


def main() -> int:
    for path in HTML_FILES + [SW_FILE]:
        if not path.exists():
            fail(f"missing expected file {path.relative_to(ROOT)}")

    checked = sum(inspect_file(path) for path in HTML_FILES + [SW_FILE])
    required = {
        ROOT / "data/catalog-lite.json",
        ROOT / "data/pathways.json",
    }
    for path in required:
        if not path.exists():
            fail(f"required published asset is missing: {path.relative_to(ROOT)}")

    print(f"local_asset_references_checked={checked}")
    print("site_assets=passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
