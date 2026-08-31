# Architecture

```text
data/          canonical seed + generated datasets
providers/     provider/source registry
credentials/   named credential layer
 taxonomy/     controlled vocabulary and field map
evidence/      evidence states and source policy
status/        manifests, progress, freshness reports
scripts/       deterministic generation and validation
site/          public browser application
docs/          methodology, roadmap, language policy
.github/       scheduled automation
```

## Record types

- `credential` — a named credential/course badge carried by the seed catalog.
- `credential-reference` — a named professional credential whose free status is not claimed.
- `source-watch` — provider × technical-domain monitoring record; not a certificate claim.
- `language-watch` — provider × language availability monitoring record.
- `regional-source` — regional discovery source.

The distinction is intentional: a large knowledge base should not inflate a provider directory into fake certificates.
