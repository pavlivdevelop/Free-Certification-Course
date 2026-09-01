# OpenCertAtlas — Installation and Local Use

OpenCertAtlas is designed to work without a personal server or self-hosted runner.

## Easiest option

Open `site/index.html` in a browser after downloading the repository. The catalog and personal tracker are portable; progress is stored locally in the browser.

## Local HTTP server

For browsers that block local JSON fetches, run one of these from the repository root:

```bash
python3 -m http.server 8080 -d site
```

Then open `http://localhost:8080/`.

## Full development environment

Python 3.13+ is sufficient for the repository automation. Install the extractor dependencies with:

```bash
python -m pip install -r requirements.txt
```

Run deterministic checks with:

```bash
python scripts/validate_catalog.py
python scripts/score_provenance.py
python scripts/smoke_site.py
```

The production catalog pipeline runs on GitHub-hosted runners; a self-hosted runner is optional.

## Portable progress

Use the Progress page to mark items as not started, in progress, completed or skipped. Export creates a JSON file that can be imported on another device.

## Offline distribution

The generated catalog files under `data/` are the portable data layer. Do not edit generated datasets manually; modify provider seeds, evidence or extractor logic and let automation rebuild the canonical outputs.
