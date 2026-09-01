# OpenCertAtlas

Source-first knowledge base for certificates, certifications, digital badges and technical learning paths.

> **Language** · [Русский](docs/README.ru.md) · [English](docs/README.en.md) · [Українська](docs/README.uk.md) · [Deutsch](docs/README.de.md) · [Español](docs/README.es.md) · [Français](docs/README.fr.md) · [Português](docs/README.pt.md) · [Polski](docs/README.pl.md) · [中文](docs/README.zh.md) · [日本語](docs/README.ja.md) · [한국어](docs/README.ko.md) · [العربية](docs/README.ar.md)

OpenCertAtlas is a source-first catalogue and learning-path system for certificates, certifications, digital badges and technical education. It scales through observed issuer data, explicit evidence and reproducible automation rather than synthetic rows.

## What this project is

**A searchable credential map + evidence layer + personal learning roadmap.**

Official company names, product names, credential titles, standards and abbreviations stay unchanged across translations. Interface text can be localized without changing the canonical dataset.

## Use the project

- Catalogue: `site/index.html`
- Personal progress: `site/progress.html`
- **Recommended next steps:** `site/recommend.html`
- **Prerequisite pathways:** `site/pathways.html`

The recommender reads the local progress file in the browser, filters already-completed items, and ranks the next learning options by goal, level, free-status preference and credential evidence. The pathway explorer adds an explicit prerequisite graph for major technical tracks. No account is required.

## Data model

- `credential` — curated named credential/badge with supporting evidence.
- `credential-candidate` — exact name observed on an issuer-owned page; not automatically verified or free.
- `credential-reference` — legitimate professional certification tracked for context; price is not implied.
- `source-watch` — official provider/domain monitoring record; never presented as a certificate.
- `regional-source` — regional discovery source.
- `language-watch` — language availability monitoring record.

## Status model

✅ **Free** · ⚠️ **Conditional** · ⚪ **Unknown** · ❌ **Paid / reference**

`Free` requires current official evidence for a no-cost route. Conditional covers student/educator access, vouchers, scholarships, campaigns, partner access and course-specific rules. A paid professional exam is never labelled free merely because its preparation material is free.

## Coverage

AI · Generative AI · LLM · AI Agents · RAG · Machine Learning · MLOps · Python · Java · C/C++ · C# · Rust · Go · Web · Mobile · APIs · Databases · Data Engineering · Cybersecurity · AppSec · SOC · DFIR · Cloud · DevOps · SRE · Kubernetes · Networking · 5G/6G · Telecommunications · IoT · Embedded · RISC-V · FPGA · ASIC · Electronics · PCB · EDA · RF · SDR · Antennas · Microwave · EMC/EMI · DSP · Radar · Control Systems · Robotics · ROS · PLC/SCADA · Industrial Automation · Mechatronics · CAD/CAM/CAE · BIM · CFD/FEA · Digital Twins · CNC · 3D Printing · Metrology · Semiconductors · Materials · Mathematics · Statistics · Physics · Quantum · GIS · Remote Sensing · Aerospace · Avionics · Automotive · Energy · Medical Devices · Biotechnology · Chemistry · Environment · Smart Cities · Game/XR · Open Source · Software Supply Chain · Observability · Testing/QA · Technical Writing and more.

## Repository architecture

`providers/` — issuer and source registry.

`credentials/` — canonical credential records and extraction candidates.

`taxonomy/` — controlled domains, skills, levels and prerequisite pathways.

`evidence/` — source URLs, extraction provenance and verification material.

`status/` — freshness, provenance, schema and roadmap state.

`data/` — generated CSV/JSON datasets.

`scripts/` — extraction, normalization, validation, quality and operational checks.

`site/` — compact public catalogue, recommender, pathway explorer and local-first progress tracker.

`.github/workflows/` — scheduled extraction, validation, freshness, provenance, repository and site checks.

## Automation

The catalogue builder runs on GitHub-hosted runners. Extraction observes issuer-owned pages using HTML/JSON-LD, qualifying same-origin links and sitemap discovery. Each candidate keeps provenance fields so later evidence can promote or reject it.

Generated data must pass structural and provenance checks before publication. Freshness checks monitor source reachability separately from credential validity and price status.

## Personal roadmap

The browser tools support search, filtering, progress states, XP/ranks, prerequisite pathways, next-step recommendations and JSON export/import. Personal progress stays local to the browser by default.

Progression: **Explore → Beginner → Foundation → Intermediate → Advanced → Professional → Expert → Master**.

## Quality rule

**Discovery is not verification. Reachability is not proof of current status. A candidate is not a free credential.**

## Language and portability

The project includes multilingual repository documentation plus a browser language selector. The static site can be copied locally; service-worker assets provide an offline-first foundation after the application is first loaded.

## Start here

- Catalogue: `site/index.html`
- Personal progress: `site/progress.html`
- Recommended next steps: `site/recommend.html`
- Pathways: `site/pathways.html`
- Data contract: `docs/DATA-CONTRACT.md`
- Methodology: `docs/METHODOLOGY.md`
- Architecture: `docs/ARCHITECTURE.md`
- Progression: `docs/PROGRESSION.md`
- Status rules: `docs/STATUS-LABELS.md`
- Taxonomy: `docs/TAXONOMY.md`
- Current continuation context: `status/ROADMAP-CONTEXT.json`

Last baseline review: 2026-09-01.
