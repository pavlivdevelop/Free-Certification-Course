# Manual evidence packets

OpenCertAtlas uses bounded evidence packets to turn automated discovery into a reproducible human-review task without granting automation permission to promote credentials.

## What a packet contains

Each packet preserves the candidate's observed identity, issuer, official URL, source page, price signal, evidence state and extraction metadata. It then adds a fixed review checklist and an initially `pending` decision.

The generated payload is deterministic for the same catalog ordering and records the catalog SHA-256 so a reviewer can tie the packet to a specific dataset snapshot.

## Required human checks

A reviewer must independently confirm the exact credential identity, credential-bearing activity, current access/price route, eligibility or conditions, and source date/currentness on the issuer-controlled source.

A learning course, training page, exam-preparation page or generic academy page is not itself proof of a credential. A free-price signal is not proof of verified-free status.

## Decision vocabulary

- `pending` — not reviewed.
- `promote` — evidence supports the proposed canonical change; a separate controlled edit still applies the change.
- `reject` — candidate should not be promoted.
- `needs-more-evidence` — review found an unresolved evidence gap.

The generator emits only `pending` packets. Review state must never be inserted into generated catalog data by the packet builder.

## Boundaries

Evidence packets are review scaffolds, not evidence themselves. They do not fetch or snapshot issuer pages, do not infer facts from URLs, do not change `Evidence Status`, do not change `Price Status`, and do not authorize automatic promotion.

The public payload is deliberately bounded. The complete working review queue remains the archival source for subsequent selection and review.
