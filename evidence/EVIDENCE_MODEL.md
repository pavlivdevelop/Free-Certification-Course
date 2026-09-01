# Evidence model

Every catalog record carries provenance fields so the database can be expanded without lowering factual quality.

## Evidence states

- `Current-catalog signal` — current provider material supports the discovered learning/credential item; this is a discovery/observation state, not a publication-grade free verification.
- `Legacy-import` — imported from the previous project dataset and scheduled for re-check.
- `Reference credential` — named professional credential tracked as a reference; free status is not claimed.
- `Source watch — auto review` — provider/domain monitoring record; not a certificate claim.
- `Language watch — auto review` — language availability monitoring record.
- `Regional source index` — regional discovery record.
- `verified` — manual evidence review confirms the exact credential exists on an issuer-controlled source and the credential type is identifiable.
- `verified-free` — manual/current evidence review confirms the exact credential/activity has a current no-cost route on an issuer-controlled source. Only this state can enter `data/free-core.csv`.

## Free-status rule

`✅ 0 ₽` in the canonical catalog represents a current free-price signal supported by provider material. It must not be interpreted as equivalent to publication-grade verification when `Evidence Status` is still a discovery state such as `Current-catalog signal`.

The **free core** is intentionally stricter: a row must be `Record Type=credential`, have `Price Status` beginning with `✅`, contain a `Source Page`, have a `Last Reviewed` value, and have `Evidence Status=verified-free` (or an explicitly approved equivalent promotion state). This prevents course pages, candidate records, or stale discovery signals from being presented as verified free credentials.

`⚠️` means a condition or current-offer check is required. `❌` is paid/reference and is excluded from the free core.

The automated checker validates URL shape, provenance fields, record semantics, and review metadata. It does not infer pricing from page text and therefore cannot silently convert a paid credential into a free one.
