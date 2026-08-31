# Free Certification Course

Source-first knowledge base for certificates, digital badges and technical learning credentials.

## Current scale

- **2,700+ tracked records** generated from a maintained provider/source registry.
- **149 providers** across multiple countries and regions.
- **100+ technical domains** from AI and Python to RF, semiconductors, robotics, physics, GIS, aerospace, energy and more.
- Free-first filtering with explicit `✅ 0 ₽`, `⚠️ condition`, and `❌ paid/reference` states.
- Personal learning roadmap with local progress, XP, ranks and export/import.
- Automated weekly source freshness checks.

## Record types

`credential` — named credential/badge from the seed catalog.

`credential-reference` — named professional certification tracked for context; free status is not claimed.

`source-watch` — provider × technical domain monitoring record. It is deliberately **not** presented as a certificate.

`language-watch` — provider × language availability monitor.

`regional-source` — regional discovery source.

## Technical coverage

AI · Machine Learning · LLM · AI Agents · MLOps · Python · Java · C++ · C# · JavaScript · Web · Mobile · APIs · Databases · Data Engineering · Data Analytics · Cybersecurity · AppSec · SecOps · Digital Forensics · Cloud · Cloud Architecture · DevOps · SRE · Platform Engineering · Kubernetes · Containers · Networking · 5G · 6G · Telecommunications · IoT · Embedded · RISC-V · FPGA · ASIC · Electronics · PCB · EDA · RF · SDR · Antennas · Microwave · Signal Processing · DSP · Control Systems · Robotics · ROS · PLC · SCADA · Industrial Automation · Mechatronics · CAD · BIM · CAE · CFD · FEA · Digital Twins · CNC · 3D Printing · Metrology · Semiconductors · Materials Science · Physics · Mathematics · Statistics · Quantum Computing · GIS · Remote Sensing · Aerospace · Automotive · Energy · Renewables · Power Systems · Medical Devices · Biotechnology · Chemistry · Environmental Technology · Agricultural Technology · Technical Writing · Project Management · Product Management · UX Engineering · Accessibility · Open Source · Software Supply Chain · Observability · Testing · QA Automation · Game Development · XR · Blockchain · HealthTech · EdTech · Maritime · Rail · Smart Cities · Cyber-Physical Systems.

## Free-status policy

- ✅ **0 ₽** — the current official source supports free access/credential.
- ⚠️ **condition** — student/educator, voucher, scholarship, campaign, partner access, or course-specific rule.
- ❌ **paid/reference** — kept outside the free core.

A badge stays a badge. A completion certificate stays a completion certificate. A professional exam certification is not represented as free unless the issuer explicitly provides a free path.

## Repository structure

- `providers/` — provider and source registry.
- `credentials/` — named credentials and reference certifications.
- `taxonomy/` — controlled technical taxonomy.
- `evidence/` — provenance and verification model.
- `status/` — manifests, progression and freshness reports.
- `data/` — generated CSV/JSON datasets.
- `scripts/` — deterministic catalog generation and freshness checking.
- `site/` — browser-based personal roadmap UI.
- `.github/workflows/` — scheduled generation and freshness checks.

## Personal roadmap

Open `site/index.html` via GitHub Pages. Mark items as in progress or completed, earn XP, move through ranks, filter by skill track, and export/import your local progress JSON. No account or remote tracking is required.

Languages: Русский · English · Українська · Deutsch · Español · Français · Português · Polski · 中文 · 日本語 · 한국어 · العربية.

## Automation

`build-catalog.yml` rebuilds the 2k+ catalog from source registry + seed data. `freshness.yml` checks official URLs and review age weekly. Automation never upgrades a source-watch row into a free credential automatically; that still requires evidence.

## Evidence basis

Current provider documentation confirms the free-learning/credential models used by core sources such as IBM SkillsBuild, AWS Educate, Salesforce Trailhead, Cisco Networking Academy, HubSpot Academy, Raspberry Pi Training Hub and Linux Foundation free learning programs. citeturn808734search2turn808734search4turn808734search0turn961954search0turn961954search2turn685079search1turn685079search3turn685079search4turn685079search15turn685079search16

Last baseline review: 2026-08-31.
