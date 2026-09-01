#!/usr/bin/env python3
"""Validate reproducible release-manifest, snapshot-index, and current-pointer contracts."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/'status/release-manifest.json'; INDEX=ROOT/'status/release-index.json'; CURRENT=ROOT/'status/release.json'; ARCHIVE_DIR=ROOT/'status/releases'
def sha256(path:Path)->str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()
def main()->int:
    if not MANIFEST.exists(): raise SystemExit('release-manifest.json is missing')
    manifest=json.loads(MANIFEST.read_text(encoding='utf-8'))
    if manifest.get('manifest_version')!='1.2': raise SystemExit(f"unexpected manifest_version={manifest.get('manifest_version')!r}")
    if not manifest.get('build_trigger_sha'): raise SystemExit('build_trigger_sha is required')
    repro=manifest.get('reproducibility',{})
    if repro.get('build_trigger_sha_is_not_the_publication_commit_sha') is not True: raise SystemExit('manifest must distinguish build trigger SHA from publication commit SHA')
    mapping=manifest.get('pathway_mapping',{})
    if mapping.get('status')!='candidate-only': raise SystemExit('pathway mappings must remain candidate-only')
    if mapping.get('does_not_claim_credential_teaches_node') is not True: raise SystemExit('pathway mapping teaching claim guard missing')
    if mapping.get('does_not_change_verification_or_free_status') is not True: raise SystemExit('pathway mapping verification/free guard missing')
    artifacts=manifest.get('artifacts',{})
    for relative,meta in artifacts.items():
        path=ROOT/relative
        if not path.exists(): raise SystemExit(f'tracked artifact missing: {relative}')
        if path.stat().st_size!=int(meta.get('bytes',-1)): raise SystemExit(f'artifact size mismatch: {relative}')
        if sha256(path)!=meta.get('sha256'): raise SystemExit(f'artifact SHA-256 mismatch: {relative}')
    snapshots=[]
    if INDEX.exists():
        index=json.loads(INDEX.read_text(encoding='utf-8')); snapshots=index.get('snapshots',[])
        if index.get('index_version') not in ('1.0','1.1'): raise SystemExit('unexpected release index version')
        if index.get('snapshot_count')!=len(snapshots): raise SystemExit('snapshot_count does not match snapshots length')
        for item in snapshots:
            snapshot=item.get('snapshot',''); path=ROOT/snapshot
            if not snapshot.startswith('status/releases/') or path.suffix!='.json': raise SystemExit(f'invalid snapshot path: {snapshot}')
            if not path.exists(): raise SystemExit(f'snapshot listed but missing: {snapshot}')
            archived=json.loads(path.read_text(encoding='utf-8'))
            if archived.get('build_trigger_sha')!=item.get('build_trigger_sha'): raise SystemExit(f'snapshot SHA metadata mismatch: {snapshot}')
    archive_count=len(list(ARCHIVE_DIR.glob('*.json'))) if ARCHIVE_DIR.exists() else 0
    if INDEX.exists() and archive_count!=len(snapshots): raise SystemExit('archive/index snapshot count mismatch')
    if CURRENT.exists():
        current=json.loads(CURRENT.read_text(encoding='utf-8'))
        if current.get('current_version')!='1.0': raise SystemExit('unexpected current release pointer version')
        if current.get('manifest')!='status/release-manifest.json': raise SystemExit('current release pointer must reference the canonical manifest')
        snapshot=current.get('snapshot',''); snapshot_path=ROOT/snapshot
        if not snapshot.startswith('status/releases/') or not snapshot_path.exists(): raise SystemExit('current release pointer references a missing snapshot')
        archived=json.loads(snapshot_path.read_text(encoding='utf-8'))
        if current.get('build_trigger_sha')!=archived.get('build_trigger_sha'): raise SystemExit('current release pointer SHA mismatch')
        if snapshots and snapshots[0].get('snapshot')!=snapshot: raise SystemExit('current release pointer must target the newest indexed snapshot')
    print('release_artifacts=passed'); print(f"manifest_version={manifest['manifest_version']}"); print(f'tracked_artifacts={len(artifacts)}'); print(f'archived_snapshots={archive_count}'); print(f"pathway_mapping_rows={mapping.get('csv_rows_including_header',0)}"); print(f"current_release_pointer={'present' if CURRENT.exists() else 'absent'}")
    return 0
if __name__=='__main__': raise SystemExit(main())
