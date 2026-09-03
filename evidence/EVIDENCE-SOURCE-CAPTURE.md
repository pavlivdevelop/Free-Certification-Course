# Evidence source metadata capture

OpenCertAtlas can run a bounded source-metadata capture pass over the highest-value rows in the promotion preview. This is an observation tool, not a verification system.

## What it records

For at most 50 selected preview rows, the workflow records the requested URL, HTTP status, final URL, content type, bytes read, a SHA-256 fingerprint of the captured body, redirect-domain information and any network error class.

The capture is tied to the exact `catalog_sha256` and promotion-preview schema version used for the run. A stale promotion preview is rejected before any source request is attempted.

## What it does not prove

A reachable page is not proof that a credential exists. An HTTP success is not proof of currentness, price, eligibility, credential-bearing activity or issuer ownership. A body fingerprint identifies an observed response; it does not establish the meaning of that response.

The capture artifact deliberately contains no verification decision, reviewer decision, canonical price status or promotion authority. Manual evidence review remains required before any catalog promotion.

## Bounds and handling

The capture uses a 12-second timeout per source, reads at most 1 MB per response and spaces requests by 0.75 seconds. Individual network errors are retained as metadata so one inaccessible provider does not invalidate the complete batch.

The workflow runs on GitHub-hosted `ubuntu-latest`, is manually dispatchable and is scheduled weekly. Its generated JSON is uploaded as an Actions artifact rather than committed into canonical catalog data.

## Review workflow

1. Run the **Evidence source capture** workflow for the current main snapshot.
2. Inspect the uploaded `opencertatlas-evidence-source-capture` artifact.
3. Use the `requested_url`, `final_url`, content type and fingerprint as navigation/audit aids only.
4. Open the issuer-controlled source and perform the manual checks defined by `evidence/EVIDENCE-PACKETS.md`.
5. Record any authoritative change through the controlled repository review process.

The capture layer is intentionally non-authoritative and cannot promote or verify a catalog record.
