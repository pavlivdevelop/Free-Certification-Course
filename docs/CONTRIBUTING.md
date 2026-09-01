# Contributing to OpenCertAtlas

## Add a provider

Add the issuer to `providers/` with an official URL and domain coverage. Do not infer credentials from topic names.

## Add a credential

A curated credential must have an official issuer page and enough evidence to establish its credential type. Keep the issuer's official title unchanged.

## Free-status rule

Use `✅ Free` only when current official evidence supports a no-cost route. Use `⚠️ Conditional` for vouchers, scholarships, student/educator access, campaigns or other explicit conditions. Use `⚪ Unknown` when the evidence is insufficient. Paid professional exams remain `❌ Paid / reference`.

## Evidence

Keep source URL, observation date and extraction method. HTTP reachability alone is not proof of current price, eligibility or validity.

## Generated files

Do not hand-edit `data/catalog-expanded.csv`, `data/catalog-expanded.json`, `data/free-core.csv` or `data/conditional.csv`. Change seeds, providers, extraction or evidence inputs and let CI rebuild them.

## Checks

```bash
python scripts/validate_catalog.py
python scripts/score_provenance.py
python scripts/smoke_site.py
```

## Pull requests

Keep changes narrow and factual. Preserve official names, avoid marketing language and do not add synthetic records just to increase catalog size.
