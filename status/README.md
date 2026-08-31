# Status layer

`status/` contains machine-readable state and quality metadata.

- `progression.json` — XP/rank model for the browser roadmap.
- `freshness-report.json` — generated URL/review-age report from the scheduled freshness job.
- `STATUS_SCHEMA.md` — meaning of lifecycle/evidence fields.
- `manifest.json` — repository data contract and expected generated artifacts.

The website keeps individual user progress in local browser storage. This directory never contains personal learner data.
