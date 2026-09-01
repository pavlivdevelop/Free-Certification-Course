# OpenCertAtlas Human Review Protocol

## Purpose

OpenCertAtlas separates automated discovery from human verification. Automated extraction may discover a concrete credential, badge, course, learning path, or certification name on an issuer-owned page. That discovery is not sufficient to publish the record as verified or to claim that access is free.

## Promotion boundary

A record may remain `credential-candidate` / `official-page-extraction` until a reviewer verifies the relevant claims. Automated jobs must not convert an observation into `verified-free` merely because a page is reachable or contains words such as "free", "certificate", or "course".

## Minimum review evidence

For a promotion to a canonical verified credential, the reviewer should capture:

1. **Exact identity** — the title/name unambiguously identifies the credential, badge, certificate, or assessment rather than a generic course or marketing category.
2. **Issuer ownership** — the evidence is on an issuer-controlled page or an issuer-controlled verification/credential platform explicitly linked from the issuer.
3. **Credential semantics** — the page establishes what is actually awarded and, where applicable, whether there is an exam, assessment, completion requirement, or separate credential issuance step.
4. **Current access/price** — the current page or official terms support the stated price/access status. A free trial, financial-aid route, audit-only path, promotional offer, or conditional waiver is not equivalent to an unqualified free credential.
5. **Eligibility constraints** — country, region, student/employment status, partner access, invitation, subscription, bundle, or other restrictions are recorded instead of inferred away.
6. **Validity** — expiration, renewal, retake, or time-limited access terms are recorded when the issuer provides them.
7. **Verification method** — the official badge/credential verification mechanism is recorded when available.
8. **Review date** — the date of verification is recorded so that stale claims can be rechecked.

## What does not count as proof

Search snippets, third-party directories, affiliate pages, social posts, cached copies, provider-wide claims without credential-level support, and automated classification are discovery aids only. They must not independently promote a record.

## Review queue priorities

- **10** — free-price signal; inspect first because it may yield high-value verified-free entries.
- **15** — credential/free-price relationship needs direct promotion review.
- **20** — credential identity needs issuer-level verification.
- **30** — issuer evidence or credential semantics need deeper review.

## Source health boundary

`status/source-health.json` measures provider seed URL reachability only. `reachable` means an HTTP response was obtained in the expected success range; `reachable-restricted` represents access/rate-limit responses. Source health never proves credential existence, price, eligibility, validity, or verification.

## Safe operating principle

Prefer an explicit `unknown` or `needs-review` state over an attractive but weak claim. OpenCertAtlas is designed to preserve provenance and uncertainty rather than manufacture certainty.
