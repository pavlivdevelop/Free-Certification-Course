#!/usr/bin/env python3
"""Fast, dependency-free smoke tests for the portable OpenCertAtlas web UI."""
from __future__ import annotations
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FILES={name:ROOT/'site'/name for name in ('index.html','progress.html','recommend.html','pathways.html','release.html','releases.html','review.html','sources.html','promotion.html','evidence-packets.html','sw.js','offline.html','robots.txt','sitemap.xml')}
def fail(message:str)->None: raise SystemExit(f"SITE SMOKE ERROR: {message}")
def main()->int:
    for name,path in FILES.items():
        if not path.exists(): fail(f"missing site/{name}")
    index=FILES['index.html'].read_text(encoding='utf-8'); progress=FILES['progress.html'].read_text(encoding='utf-8'); rec=FILES['recommend.html'].read_text(encoding='utf-8'); pathways=FILES['pathways.html'].read_text(encoding='utf-8'); release=FILES['release.html'].read_text(encoding='utf-8'); releases=FILES['releases.html'].read_text(encoding='utf-8'); review=FILES['review.html'].read_text(encoding='utf-8'); sources=FILES['sources.html'].read_text(encoding='utf-8'); promotion=FILES['promotion.html'].read_text(encoding='utf-8'); evidence=FILES['evidence-packets.html'].read_text(encoding='utf-8'); sw=FILES['sw.js'].read_text(encoding='utf-8'); robots=FILES['robots.txt'].read_text(encoding='utf-8'); sitemap=FILES['sitemap.xml'].read_text(encoding='utf-8')
    for needle,label in {'OpenCertAtlas':'canonical brand','catalog-lite.json':'lightweight catalog data source','oca-progress':'local progress persistence','progress.html':'progress route','recommend.html':'recommendation route','pathways.html':'pathway route'}.items():
        if needle not in index: fail(f"index.html missing {label}: {needle!r}")
    for needle,label in {'OpenCertAtlas — Progress':'tracker brand','localStorage':'local persistence','opencertatlas-progress.json':'portable export filename','completed':'completion state','in_progress':'in-progress state'}.items():
        if needle not in progress: fail(f"progress.html missing {label}: {needle!r}")
    for needle,label in {'Recommended next steps':'recommender heading','oca-progress':'recommender local state','catalog-lite.json':'recommender catalog'}.items():
        if needle not in rec: fail(f"recommend.html missing {label}: {needle!r}")
    for needle,label in {'pathways.json':'published pathway graph source','pathway-candidates-lite.json':'candidate mapping source','mapping_status===\'candidate\'':'candidate-only mapping filter','Candidate catalog matches':'mapping UI heading','non-authoritative candidate evidence':'candidate-only semantics','does not prove that the credential teaches':'no-teaching-claim boundary','oca-progress':'pathway local state','prerequisite':'prerequisite semantics'}.items():
        if needle.lower() not in pathways.lower(): fail(f"pathways.html missing {label}: {needle!r}")
    for needle,label in {'Reproducible release':'release heading','release-manifest.json':'release manifest source','build_trigger_sha':'trigger provenance','pathway mapping rows':'mapping release metric','candidate-only':'mapping safety status','Tracked artifacts':'artifact inventory'}.items():
        if needle.lower() not in release.lower(): fail(f"release.html missing {label}: {needle!r}")
    for needle,label in {'Immutable catalog release history':'release history heading','release-index.json':'release index source','snapshot_count':'snapshot count','build_trigger_sha':'snapshot provenance','catalog_records':'catalog metric','snapshot':'snapshot link'}.items():
        if needle.lower() not in releases.lower(): fail(f"releases.html missing {label}: {needle!r}")
    for needle,label in {'review queue':'review workspace','review-queue-lite.json':'compact review payload','never promotes a record to verified':'manual promotion boundary','status/review-queue-lite.json':'deployed review payload route'}.items():
        if needle.lower() not in review.lower(): fail(f"review.html missing {label}: {needle!r}")
    for needle,label in {'source health':'source-health workspace','source-health.json':'provider health payload','reachability':'reachability semantics','status/source-health.json':'deployed source-health route'}.items():
        if needle.lower() not in sources.lower(): fail(f"sources.html missing {label}: {needle!r}")
    for needle,label in {'Promotion preview':'promotion review workspace','status/promotion-preview.json':'promotion payload','advisory only':'non-authoritative semantics','does not promote':'no-auto-promotion boundary','issuer page':'issuer evidence link','evidence-packets.html':'evidence packet workspace link'}.items():
        if needle.lower() not in promotion.lower(): fail(f"promotion.html missing {label}: {needle!r}")
    for needle,label in {'Evidence packets':'evidence workspace heading','status/evidence-packet-index.json':'packet payload','read-only manual-review':'manual review scope','auto_promotion':'auto-promotion guardrail','required manual checks':'review checklist','issuer page':'issuer evidence link'}.items():
        if needle.lower() not in evidence.lower(): fail(f"evidence-packets.html missing {label}: {needle!r}")
    for needle,label in {'./pathways.html':'pathway page cache','./release.html':'release page cache','./releases.html':'release history cache','./promotion.html':'promotion page cache','./evidence-packets.html':'evidence packet page cache','./offline.html':'offline page cache','./data/pathways.json':'published pathway payload cache','./data/pathway-candidates-lite.json':'pathway candidate payload cache','./data/catalog-lite.json':'lightweight catalog cache','./status/review-queue-lite.json':'review payload cache','./status/source-health.json':'source-health payload cache','./status/release-manifest.json':'release manifest cache','./status/release-index.json':'release index cache','./status/promotion-preview.json':'promotion preview cache','./status/promotion-preview.md':'promotion report cache','./status/evidence-packet-index.json':'evidence packet cache','./status/EVIDENCE-PACKETS-SUMMARY.md':'evidence summary cache','./status/REVIEW-QUEUE.csv':'review CSV cache','./status/SOURCE-HEALTH.md':'source-health report cache','./status/CREDENTIAL-PATHWAY-CANDIDATES.csv':'mapping CSV cache','oca-release-indicator':'release indicator injection','manifest.json':'release metadata reference'}.items():
        if needle not in sw: fail(f"service worker missing {label}: {needle!r}")
    for needle,label in {'User-agent: *':'crawler policy','Sitemap: https://pavlivdevelop.github.io/OpenCertAtlas/sitemap.xml':'sitemap declaration'}.items():
        if needle not in robots: fail(f"robots.txt missing {label}: {needle!r}")
    for needle,label in {'<urlset':'sitemap root','https://pavlivdevelop.github.io/OpenCertAtlas/':'canonical site URL','release.html':'release URL','releases.html':'release history URL','promotion.html':'promotion URL','evidence-packets.html':'evidence workspace URL','review.html':'review URL','sources.html':'source-health URL'}.items():
        if needle not in sitemap: fail(f"sitemap.xml missing {label}: {needle!r}")
    for forbidden in ('free certification course','fcc-progress','my-certification-progress.json'):
        if forbidden in '\n'.join([index,progress,rec,pathways,release,releases,review,sources,promotion,evidence]).lower(): fail(f"legacy marker detected: {forbidden!r}")
    for name,path in FILES.items():
        if '₽' in path.read_text(encoding='utf-8'): fail(f"currency marker remains in site/{name}")
    print('site_smoke=passed'); return 0
if __name__=='__main__': sys.exit(main())
