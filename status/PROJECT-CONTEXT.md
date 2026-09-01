# OpenCertAtlas — Continuity Context

## Current state

OpenCertAtlas is a source-first public catalog for certifications, credentials, digital badges, and technical learning paths. `main` contains an automated discovery/catalog pipeline plus a deliberately separate human verification boundary.

Automated discovery extracts concrete names only from issuer-owned HTML/JSON-LD and stores them as candidates. Candidate observations include source URL and extraction method. They are not automatically promoted to verified-free.

## Data flow

`providers/` → `scripts/extract_official_credentials.py` → `credentials/extracted-candidates.jsonl` + `evidence/extraction-evidence.jsonl` → `scripts/build_official_catalog.py` → canonical datasets → `scripts/validate_catalog.py` → lightweight browser payload → `scripts/build_review_queue.py` → `status/REVIEW-QUEUE.csv` → `scripts/build_review_payload.py` → `status/review-queue-lite.json`.

Provider operational reachability is independent: `scripts/check_source_health.py` → `status/source-health.json` + `status/SOURCE-HEALTH.md`.

The static site is assembled from `site/` plus generated catalog/pathway/status payloads by `.github/workflows/deploy-pages.yml`.

## Evidence boundary

The repository treats automated observations as discovery signals. Promotion to verified requires human review of exact credential identity, issuer ownership, credential semantics, current access/price, constraints, validity, verification mechanism, and review date. See `docs/REVIEW-PROTOCOL.md`.

`source-health` is reachability telemetry only and must never be interpreted as credential evidence.

## CI / automation

Primary catalog workflow: `.github/workflows/build-catalog.yml`.
Daily source health workflow: `.github/workflows/source-health.yml`.
Site smoke: `.github/workflows/site-smoke.yml` + `scripts/smoke_site.py`.
Repository hygiene: `.github/workflows/repo-hygiene.yml`.
Pages assembly/deploy: `.github/workflows/deploy-pages.yml`.

The catalog refresh run `33514242001` completed successfully, including extraction, canonical build, validation, lightweight payload, deterministic review queue, compact review payload, and publication.

## Public UI surfaces

`site/index.html` — catalog.
`site/progress.html` — local progress tracking.
`site/recommend.html` — recommendations.
`site/pathways.html` — pathways.
`site/review.html` — reviewer workspace.
`site/sources.html` — provider source-health dashboard.

Operational payloads are copied into the Pages artifact under `_site/status/` so review/source dashboards work when deployed.

## Current human-only boundary

The repository’s Pages workflow detects whether GitHub Pages is configured. When it is not configured, the build is still validated and an ordinary artifact is produced, but deployment is skipped. Configuring Pages at repository/account settings level may require a human depending on available GitHub permissions/API surface.

## Next autonomous priorities

1. Keep all generated payloads schema-validated and deterministic.
2. Strengthen site navigation so review/source operational surfaces are discoverable.
3. Improve review queue ergonomics without creating automatic promotion.
4. Monitor CI runs after generated commits and fix regressions immediately.
5. Keep this file updated whenever architecture, workflows, or the human-only boundary changes.
