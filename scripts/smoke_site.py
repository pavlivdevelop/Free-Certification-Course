#!/usr/bin/env python3
"""Fast, dependency-free smoke tests for the portable OpenCertAtlas web UI."""
from __future__ import annotations
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FILES={name:ROOT/'site'/name for name in ('index.html','progress.html','recommend.html','pathways.html','sw.js','offline.html')}
def fail(message:str)->None: raise SystemExit(f"SITE SMOKE ERROR: {message}")
def main()->int:
    for name,path in FILES.items():
        if not path.exists(): fail(f"missing site/{name}")
    index=FILES['index.html'].read_text(encoding='utf-8'); progress=FILES['progress.html'].read_text(encoding='utf-8'); rec=FILES['recommend.html'].read_text(encoding='utf-8'); pathways=FILES['pathways.html'].read_text(encoding='utf-8'); sw=FILES['sw.js'].read_text(encoding='utf-8')
    for needle,label in {'OpenCertAtlas':'canonical brand','catalog-expanded.json':'catalog data source','oca-progress':'local progress persistence','progress.html':'progress route'}.items():
        if needle not in index: fail(f"index.html missing {label}: {needle!r}")
    for needle,label in {'OpenCertAtlas — Progress':'tracker brand','localStorage':'local persistence','opencertatlas-progress.json':'portable export filename','completed':'completion state','in_progress':'in-progress state'}.items():
        if needle not in progress: fail(f"progress.html missing {label}: {needle!r}")
    for needle,label in {'Recommended next steps':'recommender heading','oca-progress':'recommender local state','catalog-expanded.json':'recommender catalog'}.items():
        if needle not in rec: fail(f"recommend.html missing {label}: {needle!r}")
    for needle,label in {'pathways.json':'published pathway graph source','oca-progress':'pathway local state','prerequisite':'prerequisite semantics'}.items():
        if needle.lower() not in pathways.lower(): fail(f"pathways.html missing {label}: {needle!r}")
    if './pathways.html' not in sw: fail('service worker does not cache pathway page')
    if './offline.html' not in sw: fail('service worker does not cache offline page')
    for forbidden in ('free certification course','fcc-progress','my-certification-progress.json'):
        if forbidden in '\n'.join([index,progress,rec,pathways]).lower(): fail(f"legacy marker detected: {forbidden!r}")
    for name,path in FILES.items():
        if '₽' in path.read_text(encoding='utf-8'): fail(f"currency marker remains in site/{name}")
    print('site_smoke=passed'); return 0
if __name__=='__main__': sys.exit(main())
