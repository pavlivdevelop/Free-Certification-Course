# Free Certification Course — українська версія

Каталог на основі офіційних джерел: сертифікати, certifications, digital badges і перевірювані credentials.

> **Мови** · [Русский](README.ru.md) · [English](README.en.md) · [Українська](README.uk.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Français](README.fr.md) · [Português](README.pt.md) · [Polski](README.pl.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [العربية](README.ar.md)

## Мета

Створити практичну бібліотеку безкоштовних credentials без вигаданих сертифікатів. Конкретні назви надходять зі сторінок видавців; taxonomy розширює охоплення, але не створює назви credentials.

## Масштаб

Pipeline розрахований на **5 000–10 000+ спостережуваних записів** і подальше зростання. Масштабування базується на реальних назвах з офіційних сторінок і збереженні provenance.

## Охоплення

AI · Generative AI · LLM · AI Agents · RAG · Machine Learning · MLOps · Python · Java · C/C++ · C# · Rust · Go · Web · Mobile · APIs · Databases · Data Engineering · Cybersecurity · AppSec · SOC · DFIR · Cloud · DevOps · SRE · Kubernetes · Networking · 5G/6G · Telecommunications · IoT · Embedded · RISC-V · FPGA · ASIC · Electronics · PCB · EDA · RF · SDR · Antennas · Microwave · EMC/EMI · DSP · Radar · Control Systems · Robotics · ROS · PLC/SCADA · Industrial Automation · Mechatronics · CAD/CAM/CAE · BIM · CFD/FEA · Digital Twins · CNC · 3D Printing · Metrology · Semiconductors · Materials · Mathematics · Statistics · Physics · Quantum · GIS · Remote Sensing · Aerospace · Avionics · Automotive · Energy · Medical Devices · Biotechnology · Chemistry · Environment · Smart Cities · Game/XR · Open Source · Software Supply Chain · Observability · Testing/QA · Technical Writing та інші сфери.

## Архітектура

`providers/` — організації, країни, офіційні URLs, мовні та регіональні метадані.

`credentials/` — назви credentials, extraction candidates і документація registry.

`taxonomy/` — контрольована технічна taxonomy та рівні progression.

`evidence/` — provenance, докази видобування та перевірки.

`status/` — freshness, статистика та progression rules.

`data/` — datasets та exports.

`scripts/` — deterministic extraction, normalization, validation і freshness tooling.

`site/` — компактний каталог та персональний progress tracker.

`.github/workflows/` — автоматичне видобування, validation і freshness checks.

## Модель записів

- `credential` — назване credential або badge з реєстру.
- `credential-reference` — реальна professional certification для контексту; безкоштовність не припускається.
- `credential-candidate` — точна назва зі сторінки видавця, яка очікує evidence-класифікації.
- `source-watch` — запис моніторингу джерела; не показується як сертифікат.
- `regional-source` — регіональне джерело.
- `language-watch` — монітор доступності мов.

## Модель статусів

✅ **Free** · ⚠️ **Conditional** · ⚪ **Unknown** · ❌ **Paid / reference**

`Free` означає, що офіційне джерело підтримує шлях без обов’язкової оплати. `Conditional` охоплює student/educator access, voucher, scholarship, campaign, partner access і правила конкретної програми.

Назви компаній, продуктів, credentials, стандартів і абревіатури не перекладаються.

## Особиста система навчання

Веб-застосунок підтримує пошук, фільтри, початок/завершення навчання, XP, ranks, відсоток прогресу і JSON export/import. Прогрес зберігається локально у браузері та не входить до публічного dataset.

Progression: **Explore → Beginner → Foundation → Intermediate → Advanced → Professional → Expert → Master**.

## Автоматизація

Extractor читає issuer-owned HTML через JSON-LD, заголовки, same-origin links та sitemap. Для кожного запису зберігаються source URL, source page, extraction method і дата. Freshness перевіряє доступність, але доступність не доводить активність або безкоштовність credential.

Остання базова перевірка: 31.08.2026.
