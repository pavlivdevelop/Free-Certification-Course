# Free Certification Course

Source-first knowledge base for certificates, certifications, digital badges and technical learning paths.

## Mission

Build the largest practical free-credential discovery library without manufacturing fake credentials. Concrete names come from issuer-owned pages; taxonomy expands coverage but never invents certificate names.

## Scale target

The build pipeline is designed for **5,000–10,000+ observed records**. Large scale is achieved by extracting real names from official provider pages and preserving provenance, not by multiplying provider × topic combinations and calling them certificates.

## Coverage

AI · Generative AI · LLM · AI Agents · RAG · Machine Learning · MLOps · Python · Java · C/C++ · C# · Rust · Go · Web · Mobile · APIs · Databases · Data Engineering · Cybersecurity · AppSec · SOC · DFIR · Cloud · DevOps · SRE · Kubernetes · Networking · 5G/6G · Telecommunications · IoT · Embedded · RISC-V · FPGA · ASIC · Electronics · PCB · EDA · RF · SDR · Antennas · Microwave · EMC/EMI · DSP · Radar · Control Systems · Robotics · ROS · PLC/SCADA · Industrial Automation · Mechatronics · CAD/CAM/CAE · BIM · CFD/FEA · Digital Twins · CNC · 3D Printing · Metrology · Semiconductors · Materials · Mathematics · Statistics · Physics · Quantum · GIS · Remote Sensing · Aerospace · Avionics · Automotive · Energy · Medical Devices · Biotechnology · Chemistry · Environment · Smart Cities · Game/XR · Open Source · Software Supply Chain · Observability · Testing/QA · Technical Writing and more.

## Architecture

`providers/` — providers, countries, official source URLs, language/region metadata.

`credentials/` — named credentials, extraction candidates and registry documentation.

`taxonomy/` — controlled technical domains and progression levels.

`evidence/` — provenance and extraction evidence.

`status/` — freshness, catalog statistics and progression rules.

`data/` — generated CSV/JSON datasets.

`scripts/` — deterministic extraction, normalization and freshness tooling.

`site/` — compact browser application and portable personal progress tracker.

`.github/workflows/` — scheduled extraction, validation and freshness automation.

## Record model

- `credential` — named credential/badge from the curated seed set.
- `credential-reference` — legitimate professional certification tracked for context; free status is not implied.
- `credential-candidate` — exact name observed on an issuer-owned page, awaiting evidence classification.
- `source-watch` — provider/domain monitoring record; never displayed as a certificate.
- `regional-source` — regional discovery source.
- `language-watch` — language availability monitor.

## Free-status model

✅ `0 ₽` · ⚠️ conditional · ⚪ unknown · ❌ paid/reference.

A badge stays a badge. A completion certificate stays a completion certificate. A professional exam certification is not marked free without issuer evidence.

## Personal learning system

The browser UI provides search, category/price/status filters, start/complete controls, XP, ranks, progress percentage and JSON export/import. Progress remains local to the user's browser; the public dataset does not contain personal state.

Progression: **Explore → Beginner → Foundation → Intermediate → Advanced → Professional → Expert → Master**.

## Languages

Русский · English · Українська · Deutsch · Español · Français · Português · Polski · 中文 · 日本語 · 한국어 · العربية.

## Automation

The extractor reads issuer-owned HTML using JSON-LD, headings and qualifying same-origin links, and can inspect sitemap URLs. Every extracted record keeps the source URL, source page, extraction method and date. The builder validates uniqueness and the 5,000-record scale target.

Scheduled freshness checks measure source reachability. Reachability alone never proves that a credential remains free or active; promotion requires evidence.

## Verification sources

Current provider documentation supports the free-learning/credential models used by major sources such as IBM SkillsBuild, AWS Educate, Salesforce Trailhead, Cisco Networking Academy, HubSpot Academy, Google developer resources and Raspberry Pi training. citeturn208266search4turn208266search7turn208266search5turn208266search10

Last baseline review: 2026-08-31.
