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
GENERATED_ASSETS = {ROOT / "data/pathways.json": ROOT / "taxonomy/pathways.json"}


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
    if not path or any(token in path for token in ("${", "{{", "<", ">")):
        return None
    return (source.parent / path).resolve()


def check_target(source: Path, target: Path, raw_url: str) -> None:
    try:
        target.relative_to(ROOT)
    except ValueError:
        fail(f"{source.relative_to(ROOT)} references path outside repository: {raw_url!r}")
    if target.exists():
        return
    generator = GENERATED_ASSETS.get(target)
    if generator is not None and generator.exists():
        return
    fail(f"{source.relative_to(ROOT)} references missing local asset: {raw_url!r}")


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
            check_target(path, target, match.group(1))
    return checked


def main() -> int:
    for path in HTML_FILES + [SW_FILE]:
        if not path.exists():
            fail(f"missing expected file {path.relative_to(ROOT)}")

    checked = sum(inspect_file(path) for path in HTML_FILES + [SW_FILE])
    for generated, source in GENERATED_ASSETS.items():
        if not source.exists():
            fail(f"generator source is missing for {generated.relative_to(ROOT)}: {source.relative_to(ROOT)}")
    catalog = ROOT / "data/catalog-lite.json"
    if not catalog.exists() or catalog.stat().st_size == 0:
        fail("required published asset is missing or empty: data/catalog-lite.json")

    print(f"local_asset_references_checked={checked}")
    print("site_assets=passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
