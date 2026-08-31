# Free Certification Course — русский

Каталог на основе официальных источников: сертификаты, certifications, digital badges и проверяемые credentials.

> **Языки** · [Русский](README.ru.md) · [English](README.en.md) · [Українська](README.uk.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Français](README.fr.md) · [Português](README.pt.md) · [Polski](README.pl.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [العربية](README.ar.md)

## Цель

Создать практическую библиотеку бесплатных credentials без выдуманных сертификатов. Конкретные названия должны приходить со страниц издателей; taxonomy расширяет покрытие, но не создаёт названия credentials.

## Масштаб

Pipeline рассчитан на **5 000–10 000+ наблюдаемых записей** и дальнейшее расширение. Масштабирование строится на извлечении реальных названий с официальных страниц и сохранении provenance, а не на механическом умножении организаций и тем.

## Охват

AI · Generative AI · LLM · AI Agents · RAG · Machine Learning · MLOps · Python · Java · C/C++ · C# · Rust · Go · Web · Mobile · APIs · Databases · Data Engineering · Cybersecurity · AppSec · SOC · DFIR · Cloud · DevOps · SRE · Kubernetes · Networking · 5G/6G · Telecommunications · IoT · Embedded · RISC-V · FPGA · ASIC · Electronics · PCB · EDA · RF · SDR · Antennas · Microwave · EMC/EMI · DSP · Radar · Control Systems · Robotics · ROS · PLC/SCADA · Industrial Automation · Mechatronics · CAD/CAM/CAE · BIM · CFD/FEA · Digital Twins · CNC · 3D Printing · Metrology · Semiconductors · Materials · Mathematics · Statistics · Physics · Quantum · GIS · Remote Sensing · Aerospace · Avionics · Automotive · Energy · Medical Devices · Biotechnology · Chemistry · Environment · Smart Cities · Game/XR · Open Source · Software Supply Chain · Observability · Testing/QA · Technical Writing и другие направления.

## Архитектура

`providers/` — организации, страны, официальные URLs, языковые и региональные метаданные.

`credentials/` — имена credentials, extraction candidates и registry-документация.

`taxonomy/` — контролируемая техническая taxonomy и уровни progression.

`evidence/` — provenance, доказательства извлечения и проверки.

`status/` — freshness, статистика и progression rules.

`data/` — генерируемые datasets и exports.

`scripts/` — deterministic extraction, normalization, validation и freshness tooling.

`site/` — компактный каталог и персональный progress tracker.

`.github/workflows/` — автоматическое извлечение, validation и freshness checks.

## Модель записей

- `credential` — настоящее named credential или badge.
- `credential-reference` — реальная professional certification; бесплатность не предполагается.
- `credential-candidate` — точное название со страницы издателя, ожидающее классификации evidence.
- `source-watch` — запись мониторинга источника; она не показывается как сертификат.
- `regional-source` — региональный discovery source.
- `language-watch` — монитор языковой доступности.

## Модель статуса

✅ **Free** · ⚠️ **Conditional** · ⚪ **Unknown** · ❌ **Paid / reference**

`Free` означает, что официальный источник поддерживает путь без обязательной оплаты. `Conditional` охватывает student/educator доступ, vouchers, scholarships, campaigns, partner access и правила конкретной программы.

Названия компаний, продуктов, credentials, стандартов и аббревиатуры не переводятся.

## Личный roadmap

Веб-приложение поддерживает поиск, фильтры, начало/завершение обучения, XP, ranks, процент прогресса и JSON export/import. Прогресс хранится локально в браузере и не попадает в публичный dataset.

Progression: **Explore → Beginner → Foundation → Intermediate → Advanced → Professional → Expert → Master**.

## Обновление

Extractor сохраняет source URL, source page, метод извлечения и дату. Freshness проверяет доступность источников, но доступность страницы сама по себе не доказывает актуальность или бесплатность credential.

Последняя базовая проверка: 31.08.2026.
