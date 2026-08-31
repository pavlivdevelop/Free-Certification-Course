# Free Certification Course — Deutsch

Quellenbasierter Katalog von Zertifikaten, Certifications, Digital Badges und verifizierbaren Credentials.

> **Sprachen** · [Русский](README.ru.md) · [English](README.en.md) · [Українська](README.uk.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Français](README.fr.md) · [Português](README.pt.md) · [Polski](README.pl.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [العربية](README.ar.md)

## Ziel

Eine praktische Bibliothek für kostenlose Credentials ohne erfundene Zertifikate. Konkrete Namen stammen von Seiten der jeweiligen Herausgeber. Die Taxonomie erweitert die Abdeckung, erzeugt aber keine Credential-Namen.

## Umfang

Die Pipeline ist für **5.000–10.000+ beobachtete Datensätze** und weiteres Wachstum ausgelegt. Die Skalierung basiert auf echten Namen offizieller Anbieter und gespeicherter Provenienz.

## Themen

AI · Generative AI · LLM · AI Agents · RAG · Machine Learning · MLOps · Python · Java · C/C++ · C# · Rust · Go · Web · Mobile · APIs · Databases · Data Engineering · Cybersecurity · AppSec · SOC · DFIR · Cloud · DevOps · SRE · Kubernetes · Networking · 5G/6G · Telecommunications · IoT · Embedded · RISC-V · FPGA · ASIC · Electronics · PCB · EDA · RF · SDR · Antennas · Microwave · EMC/EMI · DSP · Radar · Control Systems · Robotics · ROS · PLC/SCADA · Industrial Automation · Mechatronics · CAD/CAM/CAE · BIM · CFD/FEA · Digital Twins · CNC · 3D Printing · Metrology · Semiconductors · Materials · Mathematics · Statistics · Physics · Quantum · GIS · Remote Sensing · Aerospace · Avionics · Automotive · Energy · Medical Devices · Biotechnology · Chemistry · Environment · Smart Cities · Game/XR · Open Source · Software Supply Chain · Observability · Testing/QA · Technical Writing und weitere Bereiche.

## Architektur

`providers/` — Anbieter, Länder, offizielle URLs sowie Sprach- und Regionsdaten.

`credentials/` — benannte Credentials, Extraktionskandidaten und Registry-Dokumentation.

`taxonomy/` — kontrollierte technische Taxonomie und Progressionsstufen.

`evidence/` — Provenienz, Extraktionsnachweise und Verifikationsdaten.

`status/` — Aktualität, Statistiken und Progressionsregeln.

`data/` — generierte Datensätze und Exporte.

`scripts/` — deterministische Extraktion, Normalisierung, Validierung und Freshness-Tools.

`site/` — kompakter Katalog und persönlicher Progress-Tracker.

`.github/workflows/` — geplante Extraktion, Validierung und Freshness-Prüfungen.

## Datensatzmodell

- `credential` — benanntes Credential oder Badge aus dem kuratierten Register.
- `credential-reference` — legitime Professional Certification als Referenz; kostenlos wird nicht behauptet.
- `credential-candidate` — exakter Name auf einer offiziellen Anbieter-Seite, noch ohne vollständige Evidence-Klassifizierung.
- `source-watch` — Monitoring-Eintrag; wird nie als Zertifikat dargestellt.
- `regional-source` — regionale Quelle.
- `language-watch` — Überwachung der Sprachverfügbarkeit.

## Statusmodell

✅ **Free** · ⚠️ **Conditional** · ⚪ **Unknown** · ❌ **Paid / reference**

`Free` bedeutet, dass die aktuelle offizielle Quelle einen kostenlosen Weg unterstützt. `Conditional` umfasst Student/Teacher-Zugang, Voucher, Scholarship, Kampagnen, Partnerzugang und kursabhängige Regeln.

Offizielle Firmen-, Produkt-, Credential-, Standard- und Abkürzungsnamen bleiben unverändert.

## Persönliches Lernsystem

Die Web-App bietet Suche, Filter, Start/Abschluss, XP, Ränge, Fortschrittsanzeige sowie JSON-Export/Import. Der persönliche Fortschritt bleibt lokal im Browser und wird nicht in den öffentlichen Datensatz geschrieben.

Progression: **Explore → Beginner → Foundation → Intermediate → Advanced → Professional → Expert → Master**.

## Automatisierung

Der Extractor nutzt JSON-LD, Überschriften, qualifizierte Same-Origin-Links und verfügbare Sitemaps. Jeder Datensatz speichert Quelle, Extraktionsmethode und Datum. Freshness-Prüfungen messen die Erreichbarkeit; Erreichbarkeit allein beweist weder Gültigkeit noch kostenlose Nutzung.

Letzte Basisprüfung: 31.08.2026.
