# Evidence Promotion Rules

OpenCertAtlas separates discovery from verification. A record may be promoted only when the required evidence is present and current.

## Promotion ladder

`credential-candidate` → `credential` requires all of:

1. The credential name is observed on an issuer-controlled page.
2. The page is an official issuer source or an explicitly authorized issuer channel.
3. The credential type is identifiable: certification, certificate, badge, microcredential, or equivalent.
4. The official URL is reachable during review.
5. The record has a review date and source-page provenance.

`credential` → `Free` additionally requires current issuer evidence that a no-cost route exists for the exact credential/activity. Free preparation material alone is not sufficient.

## Conditional status

Use `⚠️ Conditional` when access depends on a student/educator program, voucher, scholarship, partner campaign, region, employer, or other eligibility condition.

## Never auto-promote

Extraction alone must never promote a candidate to verified or free. HTTP success alone is not proof of credential validity, and a course page is not automatically a credential page.

## Evidence confidence

- `high` — explicit issuer credential statement + current URL + identifiable credential type.
- `medium` — issuer page clearly names the learning/credential item but type or issuance conditions need confirmation.
- `low` — discovered from issuer navigation/anchor without enough issuance detail.

Promotion automation may propose candidates, but publication into `free-core.csv` remains gated by these rules.
