# Data layer

The canonical generated catalogue is published as:

- `catalog-expanded.csv` — tabular export;
- `catalog-expanded.json` — JSON export;
- `free-core.csv` — records currently classified as free;
- `conditional.csv` — records with conditional access/pricing.

Supporting data includes extracted candidate records and evidence metadata.

`providers/` is the broader official-source registry. A provider entry is **not** a claim that the provider currently offers a free credential. A source-watch record is not a certificate.

Generated files are rebuilt by the official extraction pipeline and must pass the canonical validator before publication.

Last baseline review: 2026-08-31.
