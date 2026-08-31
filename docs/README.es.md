# Free Certification Course — Español

Catálogo basado en fuentes oficiales de certificados, certifications, digital badges y credenciales verificables.

> **Idiomas** · [Русский](README.ru.md) · [English](README.en.md) · [Українська](README.uk.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Français](README.fr.md) · [Português](README.pt.md) · [Polski](README.pl.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [العربية](README.ar.md)

## Objetivo

Crear una biblioteca práctica de credenciales gratuitas sin inventar certificados. Los nombres concretos proceden de páginas de los emisores; la taxonomía amplía la cobertura, pero no crea nombres de credenciales.

## Escala

El pipeline está diseñado para **5.000–10.000+ registros observados** y crecimiento adicional. La escala se basa en nombres reales de páginas oficiales y en la conservación de la procedencia.

## Cobertura

AI · Generative AI · LLM · AI Agents · RAG · Machine Learning · MLOps · Python · Java · C/C++ · C# · Rust · Go · Web · Mobile · APIs · Databases · Data Engineering · Cybersecurity · AppSec · SOC · DFIR · Cloud · DevOps · SRE · Kubernetes · Networking · 5G/6G · Telecommunications · IoT · Embedded · RISC-V · FPGA · ASIC · Electronics · PCB · EDA · RF · SDR · Antennas · Microwave · EMC/EMI · DSP · Radar · Control Systems · Robotics · ROS · PLC/SCADA · Industrial Automation · Mechatronics · CAD/CAM/CAE · BIM · CFD/FEA · Digital Twins · CNC · 3D Printing · Metrology · Semiconductors · Materials · Mathematics · Statistics · Physics · Quantum · GIS · Remote Sensing · Aerospace · Avionics · Automotive · Energy · Medical Devices · Biotechnology · Chemistry · Environment · Smart Cities · Game/XR · Open Source · Software Supply Chain · Observability · Testing/QA · Technical Writing y más.

## Arquitectura

`providers/` — proveedores, países, URLs oficiales y metadatos regionales y lingüísticos.

`credentials/` — credenciales nombradas, candidatos extraídos y documentación del registro.

`taxonomy/` — taxonomía técnica controlada y niveles de progreso.

`evidence/` — procedencia, evidencias de extracción y verificación.

`status/` — actualización, estadísticas y reglas de progreso.

`data/` — datasets y exports generados.

`scripts/` — extracción determinista, normalización, validación y freshness.

`site/` — catálogo web compacto y tracker personal.

`.github/workflows/` — extracción, validación y comprobaciones de freshness programadas.

## Modelo de registros

- `credential` — credencial o badge con nombre confirmado.
- `credential-reference` — professional certification legítima para contexto; no implica gratuidad.
- `credential-candidate` — nombre exacto observado en una página del emisor, pendiente de clasificación.
- `source-watch` — monitorización de proveedor/dominio; nunca se muestra como certificado.
- `regional-source` — fuente regional.
- `language-watch` — monitor de disponibilidad lingüística.

## Modelo de estado

✅ **Free** · ⚠️ **Conditional** · ⚪ **Unknown** · ❌ **Paid / reference**

`Free` significa que la fuente oficial actual admite una vía sin coste obligatorio. `Conditional` incluye acceso para estudiantes/docentes, vouchers, scholarships, campañas, partners y reglas propias del curso.

Los nombres oficiales de empresas, productos, credentials, estándares y las abreviaturas no se traducen.

## Sistema de aprendizaje personal

La aplicación web ofrece búsqueda, filtros, controles de inicio/finalización, XP, rangos, porcentaje de progreso y JSON export/import. El progreso permanece local en el navegador.

Progression: **Explore → Beginner → Foundation → Intermediate → Advanced → Professional → Expert → Master**.

## Automatización

El extractor utiliza JSON-LD, encabezados, enlaces same-origin y sitemaps. Cada registro conserva la URL de origen, método y fecha de extracción. Freshness mide accesibilidad, pero la accesibilidad por sí sola no demuestra validez ni gratuidad.

Última revisión base: 31-08-2026.
