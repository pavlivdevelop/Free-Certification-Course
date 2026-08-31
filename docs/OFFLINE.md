# Offline use

OpenCertAtlas is designed so the catalogue and personal progress UI can be used without a backend.

## From a checkout

1. Open `site/index.html` in a modern browser for the catalogue.
2. Open `site/progress.html` for the personal tracker.
3. Keep `data/catalog-expanded.json` beside the `site/` directory so the browser can load the catalogue.
4. Use the built-in JSON export/import to move personal progress between devices.

## Data boundary

The repository contains public catalogue metadata only. Personal completion state is stored in browser-local storage and is not committed by the application.

## Reproducibility

Use the repository's generated dataset plus `status/manifest.json` to identify the expected files and schema. Generated data should be treated as a snapshot; scheduled workflows refresh it from official issuer sources.

## Recommended local server

For browsers that block local `file://` fetches, serve the repository directory with any simple static HTTP server and open `site/index.html` through that server.
