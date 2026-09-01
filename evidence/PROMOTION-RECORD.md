# Promotion record contract

This contract is for a human-reviewed promotion decision. Extraction may create candidates, but it must never manufacture a promotion record.

## Required fields

```yaml
record_id: CAND-...
decision: verified | verified-free | reject | conditional
reviewed_at: YYYY-MM-DD
reviewer: human identifier or team handle
credential_url: https://...
source_page: https://...
evidence:
  issuer_identity: true
  exact_name_observed: true
  credential_type_identified: true
  issuance_or_assessment_observed: true
  current_free_route_observed: true | false | null
notes: concise factual rationale
```

## Decision semantics

`verified` confirms that the exact credential is issued or awarded by the named issuer and is supported by an issuer-controlled page. It does not assert that the credential is free.

`verified-free` additionally confirms a current no-cost route for the exact credential or activity. This is the only promotion state eligible for `data/free-core.csv`.

`conditional` is used when access depends on eligibility, voucher, scholarship, region, employer, student/educator status, partner campaign, or another explicit condition.

`reject` means the observed item is not suitable for the claimed credential record, the issuer evidence is insufficient, or the identity cannot be established.

## Evidence rules

A course, learning path, article, or training page is not automatically a credential. A reachable HTTP URL is not sufficient proof of credential validity. A general provider statement such as "many courses are free" is not sufficient proof that one exact credential is free.

Promotion records should cite the smallest issuer-controlled source page(s) that establish the decision. Keep the original observed URL and do not replace it with a search-engine result.

## Automation boundary

Automation may detect candidate records, check schema, compare identifiers, validate URL shape, detect missing provenance, and prepare a review queue. Automation must not set `verified-free` from extraction alone.
