#!/usr/bin/env python3
"""Generate a conservative promotion proposal without mutating canonical records."""
from __future__ import annotations
import csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CAT=ROOT/'data/catalog-expanded.csv'; OUT=ROOT/'status/promotion-preview.md'

def main()->int:
    with CAT.open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
    proposals=[]
    for r in rows:
        if r.get('Record Type')!='credential-candidate': continue
        evidence=r.get('Evidence Status','').strip().lower()
        method=r.get('Extraction Method','').strip().lower()
        url=r.get('Official URL','').strip()
        name=r.get('Certificate/Badge','').strip(); org=r.get('Organization','').strip()
        score=0
        if 'official-page' in evidence: score+=2
        if method in {'jsonld','heading'}: score+=2
        if url.startswith(('https://','http://')): score+=1
        if len(name)>=6 and name.lower() not in {'course','training','academy'}: score+=1
        if score>=5: proposals.append((score,org,name,url))
    proposals.sort(key=lambda x:(-x[0],x[1].casefold(),x[2].casefold()))
    lines=['# Promotion preview','',f'- candidate records reviewed: {sum(r.get("Record Type")=="credential-candidate" for r in rows)}',f'- proposals: {len(proposals)}','', 'This report is advisory. It never changes catalog records or free status.','', '| Score | Organization | Candidate | Official URL |','|---:|---|---|---|']
    lines += [f'| {s} | {o} | {n.replace("|","\\|")} | {u} |' for s,o,n,u in proposals[:500]]
    OUT.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(f'promotion_proposals={len(proposals)}')
    return 0
if __name__=='__main__': raise SystemExit(main())
