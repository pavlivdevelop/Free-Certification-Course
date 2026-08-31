# Free Certification Course — English

A source-first catalogue of certificates, certifications, digital badges and verifiable credentials.

> **Languages** · [Русский](README.ru.md) · [English](README.en.md) · [Українська](README.uk.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Français](README.fr.md) · [Português](README.pt.md) · [Polski](README.pl.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [العربية](README.ar.md)

## Mission

Build a practical free-credential discovery library without manufacturing fake credentials. Concrete names come from issuer-owned pages; taxonomy expands coverage but never invents credential names.

## Scale

The pipeline is designed for **5,000–10,000+ observed records** and further growth. Scale comes from extracting real names from official provider pages and preserving provenance rather than generating provider × topic combinations.

## Coverage

AI · Generative AI · LLM · AI Agents · RAG · Machine Learning · MLOps · Python · Java · C/C++ · C# · Rust · Go · Web · Mobile · APIs · Databases · Data Engineering · Cybersecurity · AppSec · SOC · DFIR · Cloud · DevOps · SRE · Kubernetes · Networking · 5G/6G · Telecommunications · IoT · Embedded · RISC-V · FPGA · ASIC · Electronics · PCB · EDA · RF · SDR · Antennas · Microwave · EMC/EMI · DSP · Radar · Control Systems · Robotics · ROS · PLC/SCADA · Industrial Automation · Mechatronics · CAD/CAM/CAE · BIM · CFD/FEA · Digital Twins · CNC · 3D Printing · Metrology · Semiconductors · Materials · Mathematics · Statistics · Physics · Quantum · GIS · Remote Sensing · Aerospace · Avionics · Automotive · Energy · Medical Devices · Biotechnology · Chemistry · Environment · Smart Cities · Game/XR · Open Source · Software Supply Chain · Observability · Testing/QA · Technical Writing and more.

## Architecture

`providers/` — organizations, countries, official URLs, language and regional metadata.

`credentials/` — named credentials, extraction candidates and registry documentation.

`taxonomy/` — controlled technical taxonomy and progression levels.

`evidence/` — provenance, extraction evidence and verification records.

`status/` — freshness, statistics and progression rules.

`data/` — generated datasets and exports.

`scripts/` — deterministic extraction, normalization, validation and freshness tooling.

`site/` — compact browser catalogue and personal progress tracker.

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

`Free` means the current official source supports a no-cost path. `Conditional` covers student/educator access, vouchers, scholarships, campaigns, partner access and course-specific rules. Paid professional exams stay outside the free core unless the issuer explicitly provides a free route.

Official company names, product names, credential names, standards and abbreviations remain unchanged.

## Personal learning system

The browser application provides search, category/status filters, start and completion controls, XP, ranks, progress percentage and JSON export/import. Progress is stored locally in the user's browser and is not part of the public dataset.

Progression: **Explore → Beginner → Foundation → Intermediate → Advanced → Professional → Expert → Master**.

## Automation

The extractor reads issuer-owned HTML using JSON-LD, headings, qualifying same-origin links and available sitemaps. Each extracted record keeps its source URL, source page, extraction method and extraction date. The builder validates uniqueness and scale.

Scheduled freshness checks measure source reachability. Reachability alone never proves that a credential remains active or free; free-status promotion requires evidence.

## Repository use

Start with `site/index.html` for the catalogue and `site/progress.html` for the personal tracker. The tracker is portable and local-first.

Last baseline review: 2026-08-31.
