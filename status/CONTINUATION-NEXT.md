# OpenCertAtlas — continuation notes

This file is a durable session hand-off note. The `main` branch is the source of truth for the current HEAD; this note intentionally does **not** hard-code the current commit SHA because merging this file necessarily changes HEAD.

## Confirmed completed state

- Manual evidence packets are bounded, issuer-grouped review scaffolds and never promote records.
- Browser-local evidence review state is bound to `catalog_sha256` and cannot be reused across catalog snapshots.
- Bounded issuer-source capture runs automatically after a successful `main` Promotion preview and remains weekly/manual runnable.
- Source capture rejects embedded credentials, private/reserved destinations and automatic redirects; redirects are recorded but never followed.
- Source capture selects the top 50 rows from the entire advisory promotion preview deterministically.
- The first real automatic source-capture run completed successfully on GitHub-hosted infrastructure: 50 selected rows, 20 unique URLs, 20 HTTP 200 observations, 30 deterministic deduplications, 0 redirects, 0 blocked destinations and 0 network errors.
- Source-capture network-policy regression tests and contract validation passed in the same run.
- Source-capture artifacts are non-authoritative and are not persisted as canonical catalog data.
- A Markdown source-capture summary generator is now part of the capture workflow and is uploaded alongside the JSON artifact.
- `data/REGISTRY.md` explicitly labels its 2026-08-31 counts as a historical baseline rather than current catalog statistics.

## Next autonomous priorities

1. Use future capture summaries to prioritize manual issuer checks; do not infer verification or free status from reachability.
2. Improve issuer/provider batch-review navigation in the static review workspace without adding promotion authority.
3. Expand credential-to-skill/pathway mappings only through explicit reviewed edges; lexical mappings remain candidates.
4. Continue accessibility, security and supply-chain hardening.
5. Improve catalog/extraction observability and performance without synthetic provider-by-taxonomy multiplication.
6. Work through the existing multilingual presentation-layer issue only as a non-destructive UI metadata layer; official credential and company names must remain unchanged.

## Human boundary

Authoritative credential promotion still requires issuer-controlled evidence review. Account-level permissions, secrets or other privileged UI actions are the only expected blockers outside repository tooling.
