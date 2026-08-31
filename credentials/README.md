# Credentials

`catalog-master.csv` is the unified catalogue.

Record types:

- `Credential / badge` — an existing curated certificate, credential or badge record.
- `Learning-source discovery` — a source-backed discovery record that must pass verification before it can be promoted to a verified credential.

This distinction prevents the database from inventing certificates merely to reach a target count.

The catalogue is split into small CSV parts under `credentials/parts/` so it can be maintained through GitHub's text-file API without requiring binary uploads.

The public catalogue should never contain personal completion data.
