# Evidence model

Every catalog record carries provenance fields so the database can be expanded without lowering factual quality.

## Evidence states

- `Current-catalog signal` — current provider material supports the record.
- `Legacy-import` — imported from the previous project dataset and scheduled for re-check.
- `Reference credential` — named professional credential tracked as a reference; free status is not claimed.
- `Source watch — auto review` — provider/domain monitoring record; not a certificate claim.
- `Language watch — auto review` — language availability monitoring record.
- `Regional source index` — regional discovery record.

## Free-status rule

`✅ 0 ₽` is used only when current provider information supports free access/credential. `⚠️` means a condition or current-offer check is required. `❌` is paid/reference and is excluded from the free core.

The automated checker validates URL reachability and review age. It does not infer pricing from page text and therefore cannot silently convert a paid credential into a free one.
