# Free Certification Course — Português

Catálogo baseado em fontes oficiais de certificados, certifications, Digital Badges e Credentials verificáveis.

> **Idiomas** · [Русский](README.ru.md) · [English](README.en.md) · [Українська](README.uk.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Français](README.fr.md) · [Português](README.pt.md) · [Polski](README.pl.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [العربية](README.ar.md)

## Objetivo

Criar uma biblioteca prática de credentials gratuitos sem inventar certificados. Os nomes concretos vêm das páginas oficiais dos emissores; a taxonomy amplia a cobertura, mas não cria nomes de credentials.

## Escala

O pipeline foi projetado para **5.000–10.000+ registros observados** e crescimento contínuo. A expansão usa nomes reais das páginas oficiais e preserva a proveniência.

## Cobertura

AI · Generative AI · LLM · AI Agents · RAG · Machine Learning · MLOps · Python · Java · C/C++ · C# · Rust · Go · Web · Mobile · APIs · Databases · Data Engineering · Cybersecurity · AppSec · SOC · DFIR · Cloud · DevOps · SRE · Kubernetes · Networking · 5G/6G · Telecommunications · IoT · Embedded · RISC-V · FPGA · ASIC · Electronics · PCB · EDA · RF · SDR · Antennas · Microwave · EMC/EMI · DSP · Radar · Control Systems · Robotics · ROS · PLC/SCADA · Industrial Automation · Mechatronics · CAD/CAM/CAE · BIM · CFD/FEA · Digital Twins · CNC · 3D Printing · Metrology · Semiconductors · Materials · Mathematics · Statistics · Physics · Quantum · GIS · Remote Sensing · Aerospace · Avionics · Automotive · Energy · Medical Devices · Biotechnology · Chemistry · Environment · Smart Cities · Game/XR · Open Source · Software Supply Chain · Observability · Testing/QA · Technical Writing e muito mais.

## Arquitetura

`providers/` — provedores, países, URLs oficiais e metadados regionais e linguísticos.

`credentials/` — credentials nomeados, candidatos extraídos e documentação do registry.

`taxonomy/` — taxonomia técnica controlada e níveis de progression.

`evidence/` — proveniência, evidências de extração e verificação.

`status/` — freshness, estatísticas e regras de progression.

`data/` — datasets e exports gerados.

`scripts/` — extração determinística, normalização, validação e ferramentas de freshness.

`site/` — catálogo web compacto e tracker pessoal.

`.github/workflows/` — extração, validação e verificações de freshness agendadas.

## Modelo de registros

- `credential` — credential ou badge com nome confirmado.
- `credential-reference` — professional certification legítima para contexto; não implica gratuidade.
- `credential-candidate` — nome exato observado em página do emissor, aguardando classificação por evidence.
- `source-watch` — registro de monitoramento; nunca apresentado como certificado.
- `regional-source` — fonte regional.
- `language-watch` — monitor de disponibilidade linguística.

## Modelo de status

✅ **Free** · ⚠️ **Conditional** · ⚪ **Unknown** · ❌ **Paid / reference**

`Free` significa que a fonte oficial atual oferece um caminho sem pagamento obrigatório. `Conditional` cobre acesso para estudantes/professores, voucher, scholarship, campanhas, partners e regras específicas do curso.

Nomes de empresas, produtos, credentials, padrões e abreviações permanecem sem tradução.

## Sistema de aprendizagem pessoal

A aplicação web oferece busca, filtros, início/conclusão, XP, ranks, porcentagem de progresso e JSON export/import. O progresso permanece local no navegador e não entra no dataset público.

Progression: **Explore → Beginner → Foundation → Intermediate → Advanced → Professional → Expert → Master**.

## Automação

O extractor usa JSON-LD, títulos, links same-origin qualificados e sitemaps disponíveis. Cada registro preserva source URL, método de extração e data. Freshness verifica acessibilidade, mas acessibilidade sozinha não prova validade nem gratuidade.

Última revisão de base: 31-08-2026.
