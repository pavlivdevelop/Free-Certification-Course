# Human review queue

`status/REVIEW-QUEUE.csv` is a generated work queue derived from `data/catalog-expanded.csv`.

It is intentionally separate from the canonical catalog and evidence decisions. A queue row means **review is useful**, not that the underlying claim is true.

## Priority order

| Priority | Meaning |
|---|---|
| 10 | Candidate credential with an explicit free-price signal; highest-value review target. |
| 15 | Credential with a free-price signal that still lacks an approved `verified-free` evidence state. |
| 20 | Candidate credential whose identity/type needs issuer-level verification. |
| 30 | Credential requiring issuer-level evidence review. |

Source-watch, regional-source and language-watch records are excluded because they are monitoring/index records rather than direct credential claims.

## Review outcome

A reviewer should use `evidence/PROMOTION-RECORD.md` and inspect the issuer-controlled source page. Outcomes are `verified`, `verified-free`, `conditional`, or `reject`.

A review decision changes the evidence state only through an explicit human action. Regenerating the queue never promotes or demotes a catalog record automatically.

## Regeneration

The queue is rebuilt during the canonical catalog workflow. Sorting is deterministic by queue priority, organization and credential name so diffs remain reviewable and repeatable.
