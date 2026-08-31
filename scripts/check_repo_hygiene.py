#!/usr/bin/env python3
"""Repository hygiene checks for OpenCertAtlas runtime-facing files."""
from __future__ import annotations
from pathlib import Path
import re, sys

ROOT=Path(__file__).resolve().parents[1]
SELF=Path(__file__).resolve()
TEXT_SUFFIXES={".md",".yml",".yaml",".py",".html"}
SCAN_ROOTS=(ROOT/"README.md", ROOT/"site", ROOT/".github", ROOT/"scripts")
PATTERNS={
    "legacy_repository_url": re.compile(r"pavlivdevelop/Free-Certification-Course", re.I),
    "legacy_product_title": re.compile(r"Free Certification Course", re.I),
    "rubles_symbol": re.compile("₽"),
    "legacy_checkout_action": re.compile(r"actions/checkout@v[1-5](?:\b|$)"),
    "legacy_setup_python_action": re.compile(r"actions/setup-python@v[1-6](?:\b|$)"),
}
IGNORED_FILES={ROOT/"scripts/check_repo_hygiene.py",ROOT/"scripts/smoke_site.py"}

def files():
    for root in SCAN_ROOTS:
        if root.is_file():
            yield root; continue
        if root.exists():
            for p in root.rglob("*"):
                if p.is_file() and p.suffix.lower() in TEXT_SUFFIXES and p.resolve() not in IGNORED_FILES:
                    yield p

def main()->int:
    failures=[]
    for p in files():
        try: text=p.read_text(encoding="utf-8")
        except UnicodeDecodeError: continue
        for name,rx in PATTERNS.items():
            if rx.search(text): failures.append((name,p.relative_to(ROOT).as_posix()))
    if failures:
        for kind,path in failures: print(f"HYGIENE ERROR: {kind}: {path}")
        return 1
    print("repository_hygiene=passed"); return 0

if __name__=="__main__": raise SystemExit(main())
