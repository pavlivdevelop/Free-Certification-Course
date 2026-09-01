# OpenCertAtlas Architecture

OpenCertAtlas is a source-first credential knowledge base with a portable learning layer.

## Pipeline

```text
Provider registry
      ↓
Official-page discovery
      ↓
Concrete-name extraction
      ↓
Provenance evidence
      ↓
Canonical normalization
      ↓
Schema + semantic validation
      ↓
Credential classification
      ↓
Free / Conditional / Unknown / Paid status
      ↓
Freshness monitoring
      ↓
Learning-path graph
      ↓
Public catalog + local progress tracker
```

## Core rule

Discovery never implies verification. HTTP reachability never proves current credential status. A credential candidate is not a free credential.

## Repository layers

- `providers/` — issuer/source registry and monitoring metadata.
- `credentials/` — credential records and observed candidates.
- `taxonomy/` — controlled domains, skills and levels.
- `evidence/` — provenance and verification material.
- `status/` — freshness, quality, schema and continuation state.
- `data/` — generated canonical datasets.
- `scripts/` — deterministic discovery, extraction, normalization and validation.
- `site/` — static catalog and local-first progress application.
- `.github/workflows/` — unattended CI and scheduled maintenance.

## Record lifecycle

`observed → candidate → classified → evidence-reviewed → verified`

A record may also move to `rejected`, `stale` or `retired` without being deleted, preserving provenance and audit history.

## Status semantics

- `✅ Free` — explicit current evidence supports a no-cost route.
- `⚠️ Conditional` — free only with a stated condition such as voucher, scholarship, student/educator access or campaign.
- `⚪ Unknown` — not enough current evidence to make a price/status claim.
- `❌ Paid / reference` — tracked for context but not represented as free.

## Quality gates

Every generated catalog must satisfy schema constraints, minimum scale, unique identity, valid URLs, CSV/JSON parity and record-type/status boundaries. Extracted candidates remain candidates until promoted by evidence; the provenance score is advisory and cannot perform promotion by itself.

## Scaling principle

Generated catalog size is not a quality metric by itself. New records must come from issuer-owned observations or explicit curated evidence. Taxonomy is never used to manufacture credential names.

## Continuation

`status/ROADMAP-CONTEXT.json` is the canonical hand-off state for future development sessions.
