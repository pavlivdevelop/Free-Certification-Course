# Reproducible releases

OpenCertAtlas publishes a machine-readable `status/release-manifest.json` with each generated catalog refresh.

The manifest records:

- the commit SHA used for the build;
- catalog and queue counts from `status/CATALOG-STATS.md`;
- SHA-256 hashes for the canonical catalog, browser payloads, pathway graph and review queue;
- the extractor and catalog-builder source hashes;
- the active schema/data-contract references;
- the project rules that prevent discovery records from being treated as verified credentials or free credentials.

## What a snapshot proves

A manifest binds a published dataset to a specific repository state and content hashes. It does **not** prove that every credential is currently free or valid. Those claims remain evidence-driven and are tracked separately.

## Local reproducibility

Run:

```bash
python scripts/build_release_manifest.py
```

For a hosted catalog refresh, the same script is executed after extraction, canonical build, validation, lightweight payload generation and review-queue generation.

## Stable references

- Canonical data: `data/catalog-expanded.json`
- Browser data: `data/catalog-lite.json`
- Free core: `data/free-core.csv`
- Review queue: `status/REVIEW-QUEUE.csv`
- Release manifest: `status/release-manifest.json`
- Data contract: `docs/DATA-CONTRACT.md`
