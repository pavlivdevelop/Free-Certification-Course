# OpenCertAtlas data contract

## Purpose

The catalog is a source-first dataset. A record must preserve what was observed at an issuer-owned source and must not be promoted beyond the available evidence.

## Record types

- `credential` — curated, evidence-backed credential or badge.
- `credential-reference` — legitimate certification tracked for context; free status is not implied.
- `credential-candidate` — exact title observed on an issuer-owned page that still needs classification/evidence.
- `source-watch` — monitoring record for a provider/source.
- `regional-source` — regional discovery record.
- `language-watch` — language availability monitor.

## Price status

- `✅ Free` — the current official source supports a no-cost path.
- `⚠️ Conditional` — free only through a defined condition such as student/educator access, voucher, scholarship, campaign or partner program.
- `⚪ Unknown` — the current evidence does not establish price.
- `❌ Paid / reference` — paid or reference-only; never included in the free core.

## Provenance minimum

Every published credential record should retain:

1. an issuer/organization;
2. an official URL;
3. a concrete observed title;
4. a record type;
5. a price-status classification;
6. extraction/source evidence when machine-discovered;
7. an extraction or review timestamp where available.

## Promotion rule

`credential-candidate` → `credential` requires evidence. A successful HTTP request, a taxonomy match, or a plausible title is not sufficient evidence of a credential or free status.

## Pathway mapping contract

Credential-to-pathway mappings are a separate presentation/recommendation layer. The generated `CREDENTIAL-PATHWAY-CANDIDATES.csv` and `pathway-candidates-lite.json` files are **candidate mappings only**. They may use lexical/category signals to suggest relevant prerequisite nodes, but they must not claim that a credential teaches a node, must not alter `Evidence Status`, and must not promote `Price Status` or verification.

Candidate mappings must reference an existing node from `taxonomy/pathways.json`, use `mapping_status=candidate`, preserve the credential ID, and remain independently reviewable.

## Compatibility

Schema version is tracked separately from generated datasets. Additive fields are preferred. Renaming/removing fields requires a documented migration and validator update.
