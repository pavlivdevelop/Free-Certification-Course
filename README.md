# OpenCertAtlas

Source-first knowledge base for certificates, certifications, digital badges and technical learning paths.

> **Language** · [Русский](docs/README.ru.md) · [English](docs/README.en.md) · [Українська](docs/README.uk.md) · [Deutsch](docs/README.de.md) · [Español](docs/README.es.md) · [Français](docs/README.fr.md) · [Português](docs/README.pt.md) · [Polski](docs/README.pl.md) · [中文](docs/README.zh.md) · [日本語](docs/README.ja.md) · [한국어](docs/README.ko.md) · [العربية](docs/README.ar.md)

The language files contain the full README, not a shortened summary. Official company names, product names, credential names, standards and abbreviations remain unchanged.

## Mission

Build a practical free-credential discovery library without manufacturing fake credentials. Concrete names come from issuer-owned pages; taxonomy expands coverage but never invents certificate names.

## Scale

The pipeline is designed for **5,000–10,000+ observed records** and can grow further. Scale comes from extracting real names from official provider pages and preserving provenance, not from multiplying provider × topic combinations and calling them certificates.

## Coverage

AI · Generative AI · LLM · AI Agents · RAG · Machine Learning · MLOps · Python · Java · C/C++ · C# · Rust · Go · Web · Mobile · APIs · Databases · Data Engineering · Cybersecurity · AppSec · SOC · DFIR · Cloud · DevOps · SRE · Kubernetes · Networking · 5G/6G · Telecommunications · IoT · Embedded · RISC-V · FPGA · ASIC · Electronics · PCB · EDA · RF · SDR · Antennas · Microwave · EMC/EMI · DSP · Radar · Control Systems · Robotics · ROS · PLC/SCADA · Industrial Automation · Mechatronics · CAD/CAM/CAE · BIM · CFD/FEA · Digital Twins · CNC · 3D Printing · Metrology · Semiconductors · Materials · Mathematics · Statistics · Physics · Quantum · GIS · Remote Sensing · Aerospace · Avionics · Automotive · Energy · Medical Devices · Biotechnology · Chemistry · Environment · Smart Cities · Game/XR · Open Source · Software Supply Chain · Observability · Testing/QA · Technical Writing and more.

## Architecture

`providers/` — providers, countries, official source URLs, language and regional metadata.

`credentials/` — named credentials, extraction candidates and credential documentation.

`taxonomy/` — controlled technical domains and progression levels.

`evidence/` — provenance, extraction evidence and verification records.

`status/` — freshness, catalog statistics and progression rules.

`data/` — generated datasets and exports.

`scripts/` — deterministic extraction, normalization, validation and freshness tooling.

`site/` — compact browser catalogue and portable personal progress tracker.

`.github/workflows/` — scheduled extraction, validation and freshness automation.

## Record model

- `credential` — named credential or badge from the curated registry.
- `credential-reference` — legitimate professional certification tracked for context; free status is not implied.
- `credential-candidate` — exact name observed on an issuer-owned page, awaiting evidence classification.
- `source-watch` — provider/domain monitoring record; never presented as a certificate.
- `regional-source` — regional discovery source.
- `language-watch` — language availability monitor.

## Status model

✅ **Free** · ⚠️ **Conditional** · ⚪ **Unknown** · ❌ **Paid / reference**

`Free` means the current official source supports a no-cost path. `Conditional` covers student/educator access, voucher or scholarship programs, campaigns, partner access and course-specific rules. Paid professional exams remain outside the free core unless the issuer explicitly provides a free route.

A badge stays a badge. A completion certificate stays a completion certificate. A professional exam certification is never labelled free without issuer evidence.

See [`docs/STATUS-LABELS.md`](docs/STATUS-LABELS.md) for the canonical status specification.

## Personal learning system

The browser application provides search, category/status filters, start and completion controls, XP, ranks, progress percentage and JSON export/import. Progress remains local to the user's browser; the public dataset contains no personal state.

Progression: **Explore → Beginner → Foundation → Intermediate → Advanced → Professional → Expert → Master**.

## Automation

The extractor reads issuer-owned HTML using JSON-LD, headings, qualifying same-origin links and available sitemap URLs. Each extracted record keeps its source URL, source page, extraction method and extraction date. The builder validates uniqueness and the scale target.

Scheduled freshness checks measure source reachability. Reachability alone never proves that a credential remains active or free; free-status promotion requires evidence.

## Quality principles

OpenCertAtlas treats provenance and classification as first-class data. Discovery is not verification, reachability is not proof of current status, and a credential candidate is not automatically a free credential. Generated datasets must pass structural, uniqueness and scale checks before publication.

## Repository use

Start with `site/index.html` for the catalogue and `site/progress.html` for the personal tracker. The tracker works locally and stores progress in the browser; export the JSON file to move your progress between devices.

Last baseline review: 2026-08-31.
