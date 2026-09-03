# Manual evidence packets

OpenCertAtlas uses bounded evidence packets to turn automated discovery into a reproducible human-review task without granting automation permission to promote credentials.

## What a packet contains

Each packet preserves the candidate's observed identity, issuer, official URL, source page, price signal, evidence state and extraction metadata. It then adds a fixed review checklist and an initially `pending` decision.

Candidate selection, ordering and the catalog binding are deterministic for the same catalog snapshot. The payload also carries a generation timestamp, so byte-for-byte output is intentionally not deterministic; the `catalog_sha256` is the authoritative snapshot binding for review continuity.

## Local reviewer state

The published evidence workspace may store checklist marks and working notes in the reviewer's browser `localStorage`. This is personal preparation state only. It is never written back into the generated packet payload, catalog CSV/JSON, verification state or price status.

Local reviewer state is explicitly bound to the `catalog_sha256` of the currently displayed packet payload. When the catalog snapshot changes, the workspace starts with an empty local checklist for the new snapshot instead of silently applying marks from an older dataset.

Clearing local reviewer state removes only that browser's checklist/notes. A reviewer must still use the controlled repository process to record any authoritative evidence or promotion decision.

## Required human checks

A reviewer must independently confirm the exact credential identity, credential-bearing activity, current access/price route, eligibility or conditions, and source date/currentness on the issuer-controlled source.

A learning course, training page, exam-preparation page or generic academy page is not itself proof of a credential. A free-price signal is not proof of verified-free status.

## Decision vocabulary

- `pending` — not reviewed.
- `promote` — evidence supports the proposed canonical change; a separate controlled edit still applies the change.
- `reject` — candidate should not be promoted.
- `needs-more-evidence` — review found an unresolved evidence gap.

The generator emits only `pending` packets. Review state must never be inserted into generated catalog data by the packet builder.

## Source metadata capture

The optional source-capture workflow records reachability metadata and a bounded response fingerprint for at most 50 high-value candidates. It is deliberately non-authoritative and exists only to make manual source review faster.

For security, the capture process requires `http`/`https` URLs without embedded credentials, resolves the destination before connecting, permits only destinations whose resolved addresses are globally routable, and does not automatically follow HTTP redirects. Redirect targets are recorded for manual inspection only and are never fetched by the capture process.

The capture reads at most 1 MB per source and applies a 12-second timeout plus a 0.75-second inter-request delay. A response fingerprint can identify an observed body but cannot establish its meaning, currentness, issuer ownership or credential validity.

## Boundaries

Evidence packets are review scaffolds, not evidence themselves. They do not fetch or snapshot issuer pages, do not infer facts from URLs, do not change `Evidence Status`, do not change `Price Status`, and do not authorize automatic promotion.

Source capture is also not verification. A reachable response is not proof that a credential exists, remains current, is free, or is owned by the issuer. The source-capture artifact is uploaded as an Actions artifact rather than persisted into canonical catalog data.

The public payload is deliberately bounded. The complete working review queue remains the archival source for subsequent selection and review.
