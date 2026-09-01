#!/usr/bin/env python3
"""Build a small browser payload from the canonical catalog without changing source data."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'data/catalog-expanded.json'; OUT=ROOT/'data/catalog-lite.json'
FIELDS=['ID','Country','Organization','Certificate/Badge','Record Type','Category','Subcategory','Level','Price Status','Available from Russia','Official URL','Priority','Evidence Status']
def main()->int:
    rows=json.loads(SRC.read_text(encoding='utf-8'))
    if not isinstance(rows,list): raise SystemExit('catalog-expanded.json must be an array')
    lite=[{k:r.get(k,'') for k in FIELDS} for r in rows]
    OUT.write_text(json.dumps(lite,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
    print(f'catalog_lite_records={len(lite)}')
    print(f'catalog_lite_bytes={OUT.stat().st_size}')
    return 0
if __name__=='__main__': raise SystemExit(main())
