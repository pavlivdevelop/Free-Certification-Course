# Free Certification Course — Polski

Katalog oparty na oficjalnych źródłach: certyfikaty, certifications, Digital Badges i weryfikowalne Credentials.

> **Języki** · [Русский](README.ru.md) · [English](README.en.md) · [Українська](README.uk.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Français](README.fr.md) · [Português](README.pt.md) · [Polski](README.pl.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [العربية](README.ar.md)

## Cel

Tworzenie praktycznej biblioteki bezpłatnych credentials bez wymyślania nieistniejących certyfikatów. Konkretne nazwy pochodzą z oficjalnych stron wystawców; taxonomy rozszerza zakres, ale nie tworzy nazw credentials.

## Skala

Pipeline jest przygotowany na **5 000–10 000+ obserwowanych rekordów** i dalszy rozwój. Skalowanie opiera się na rzeczywistych nazwach z oficjalnych stron oraz zachowaniu informacji o źródłach.

## Zakres

AI · Generative AI · LLM · AI Agents · RAG · Machine Learning · MLOps · Python · Java · C/C++ · C# · Rust · Go · Web · Mobile · APIs · Databases · Data Engineering · Cybersecurity · AppSec · SOC · DFIR · Cloud · DevOps · SRE · Kubernetes · Networking · 5G/6G · Telecommunications · IoT · Embedded · RISC-V · FPGA · ASIC · Electronics · PCB · EDA · RF · SDR · Antennas · Microwave · EMC/EMI · DSP · Radar · Control Systems · Robotics · ROS · PLC/SCADA · Industrial Automation · Mechatronics · CAD/CAM/CAE · BIM · CFD/FEA · Digital Twins · CNC · 3D Printing · Metrology · Semiconductors · Materials · Mathematics · Statistics · Physics · Quantum · GIS · Remote Sensing · Aerospace · Avionics · Automotive · Energy · Medical Devices · Biotechnology · Chemistry · Environment · Smart Cities · Game/XR · Open Source · Software Supply Chain · Observability · Testing/QA · Technical Writing i inne.

## Architektura

`providers/` — dostawcy, kraje, oficjalne URL oraz metadane językowe i regionalne.

`credentials/` — nazwane credentials, kandydaci z ekstrakcji i dokumentacja registry.

`taxonomy/` — kontrolowana taxonomia techniczna i poziomy progression.

`evidence/` — provenance, dowody ekstrakcji i weryfikacji.

`status/` — freshness, statystyki i reguły progression.

`data/` — generowane datasety i eksporty.

`scripts/` — deterministyczna ekstrakcja, normalizacja, walidacja i narzędzia freshness.

`site/` — kompaktowy katalog webowy i osobisty tracker postępów.

`.github/workflows/` — zaplanowana ekstrakcja, walidacja i kontrole freshness.

## Model rekordów

- `credential` — nazwane credential lub badge z rejestru.
- `credential-reference` — prawdziwa professional certification śledzona dla kontekstu; bezpłatność nie jest zakładana.
- `credential-candidate` — dokładna nazwa znaleziona na oficjalnej stronie, oczekująca klasyfikacji evidence.
- `source-watch` — rekord monitorujący dostawcę/domenę; nigdy nie jest prezentowany jako certyfikat.
- `regional-source` — źródło regionalne.
- `language-watch` — monitor dostępności językowej.

## Model statusów

✅ **Free** · ⚠️ **Conditional** · ⚪ **Unknown** · ❌ **Paid / reference**

`Free` oznacza, że aktualne oficjalne źródło udostępnia ścieżkę bez obowiązkowej opłaty. `Conditional` obejmuje dostęp dla studentów/nauczycieli, voucher, scholarship, kampanie, partner access oraz zasady konkretnego kursu.

Nazwy firm, produktów, credentials, standardów i skróty pozostają bez tłumaczenia.

## Osobisty system nauki

Aplikacja webowa oferuje wyszukiwanie, filtry, rozpoczęcie/zakończenie, XP, rangi, procent postępu oraz JSON export/import. Postęp pozostaje lokalnie w przeglądarce.

Progression: **Explore → Beginner → Foundation → Intermediate → Advanced → Professional → Expert → Master**.

## Automatyzacja

Extractor wykorzystuje JSON-LD, nagłówki, kwalifikowane linki same-origin i dostępne sitemapy. Każdy rekord zachowuje source URL, metodę ekstrakcji i datę. Freshness sprawdza dostępność, ale sama dostępność nie dowodzi ważności ani bezpłatności credential.

Ostatni przegląd bazowy: 31.08.2026.
