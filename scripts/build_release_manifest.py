#!/usr/bin/env python3
"""Build a reproducible machine-readable release manifest from the repository state."""
from __future__ import annotations
import hashlib, json, os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'status' / 'release-manifest.json'
STATS = ROOT / 'status' / 'CATALOG-STATS.md'
TRACKED = [
    ROOT / 'data' / 'catalog-expanded.json',
    ROOT / 'data' / 'catalog-lite.json',
    ROOT / 'data' / 'free-core.csv',
    ROOT / 'data' / 'conditional.csv',
    ROOT / 'taxonomy' / 'pathways.json',
    ROOT / 'status' / 'REVIEW-QUEUE.csv',
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def stat_value(text: str, key: str) -> int:
    prefix = f'- {key}: '
    for line in text.splitlines():
        if line.startswith(prefix):
            try:
                return int(line[len(prefix):].strip())
            except ValueError:
                return 0
    return 0


def line_count(path: Path) -> int:
    with path.open(encoding='utf-8-sig', newline='') as f:
        return sum(1 for _ in f)


def main() -> int:
    stats_text = STATS.read_text(encoding='utf-8') if STATS.exists() else ''
    build_trigger_sha = os.environ.get('GITHUB_SHA') or 'local'
    manifest = {
        'manifest_version': '1.1',
        'project': 'OpenCertAtlas',
        'generated_at_utc': datetime.now(timezone.utc).isoformat(),
        'build_trigger_sha': build_trigger_sha,
        'schema': {
            'catalog': 'status/CATALOG-SCHEMA.json',
            'data_contract': 'docs/DATA-CONTRACT.md',
            'pathways': 'taxonomy/pathways.json',
        },
        'extractor': {
            'path': 'scripts/extract_official_credentials.py',
            'sha256': sha256(ROOT / 'scripts' / 'extract_official_credentials.py'),
        },
        'builder': {
            'path': 'scripts/build_official_catalog.py',
            'sha256': sha256(ROOT / 'scripts' / 'build_official_catalog.py'),
        },
        'catalog': {
            'records': stat_value(stats_text, 'records'),
            'free_signals': stat_value(stats_text, 'free signals'),
            'verified_free_core': stat_value(stats_text, 'verified free-core'),
            'conditional': stat_value(stats_text, 'conditional'),
            'candidates': stat_value(stats_text, 'candidates'),
        },
        'queue': {
            'review_queue_rows_including_header': line_count(ROOT / 'status' / 'REVIEW-QUEUE.csv') if (ROOT / 'status' / 'REVIEW-QUEUE.csv').exists() else 0,
        },
        'artifacts': {
            str(p.relative_to(ROOT)): {'bytes': p.stat().st_size, 'sha256': sha256(p)}
            for p in TRACKED if p.exists()
        },
        'reproducibility': {
            'source_first': True,
            'generated_outputs_are_not_seed_inputs': True,
            'discovery_is_not_verification': True,
            'free_status_requires_verified_free_evidence': True,
            'build_trigger_sha_is_not_the_publication_commit_sha': True,
        },
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'release_manifest={OUT.relative_to(ROOT)}')
    print(f'catalog_records={manifest["catalog"]["records"]}')
    print(f'build_trigger_sha={build_trigger_sha}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
