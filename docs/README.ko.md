# Free Certification Course — 한국어

공식 출처를 기반으로 한 인증서, certifications, Digital Badges 및 검증 가능한 Credentials 카탈로그입니다.

> **언어** · [Русский](README.ru.md) · [English](README.en.md) · [Українська](README.uk.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Français](README.fr.md) · [Português](README.pt.md) · [Polski](README.pl.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [العربية](README.ar.md)

## 목표

존재하지 않는 인증서를 만들어내지 않고, 무료 credentials를 실용적으로 찾을 수 있는 라이브러리를 구축합니다. 구체적인 이름은 발급 기관의 공식 페이지에서 가져오며, taxonomy는 범위를 넓히지만 Credential 이름을 생성하지 않습니다.

## 규모

Pipeline은 **5,000–10,000+개의 관측 레코드**와 지속적인 확장을 목표로 합니다. 규모는 공식 페이지에서 실제 이름을 추출하고 provenance를 보존하는 방식으로 확장됩니다.

## 범위

AI · Generative AI · LLM · AI Agents · RAG · Machine Learning · MLOps · Python · Java · C/C++ · C# · Rust · Go · Web · Mobile · APIs · Databases · Data Engineering · Cybersecurity · AppSec · SOC · DFIR · Cloud · DevOps · SRE · Kubernetes · Networking · 5G/6G · Telecommunications · IoT · Embedded · RISC-V · FPGA · ASIC · Electronics · PCB · EDA · RF · SDR · Antennas · Microwave · EMC/EMI · DSP · Radar · Control Systems · Robotics · ROS · PLC/SCADA · Industrial Automation · Mechatronics · CAD/CAM/CAE · BIM · CFD/FEA · Digital Twins · CNC · 3D Printing · Metrology · Semiconductors · Materials · Mathematics · Statistics · Physics · Quantum · GIS · Remote Sensing · Aerospace · Avionics · Automotive · Energy · Medical Devices · Biotechnology · Chemistry · Environment · Smart Cities · Game/XR · Open Source · Software Supply Chain · Observability · Testing/QA · Technical Writing 등.

## 아키텍처

`providers/` — 제공 기관, 국가, 공식 URL, 언어 및 지역 메타데이터.

`credentials/` — 명명된 credentials, 추출 후보 및 registry 문서.

`taxonomy/` — 관리되는 기술 taxonomy와 progression 단계.

`evidence/` — provenance, 추출 증거 및 검증 정보.

`status/` — freshness, 통계 및 progression rules.

`data/` — 생성된 datasets와 exports.

`scripts/` — 결정적 추출, 정규화, 검증 및 freshness 도구.

`site/` — 간결한 웹 카탈로그와 개인 progress tracker.

`.github/workflows/` — 예약된 추출, 검증 및 freshness 자동화.

## 레코드 모델

- `credential` — registry에서 확인된 credential 또는 badge.
- `credential-reference` — 실제 professional certification을 참고용으로 추적합니다. 무료라는 의미는 아닙니다.
- `credential-candidate` — 발급 기관의 공식 페이지에서 발견된 정확한 이름이며 evidence 분류를 기다립니다.
- `source-watch` — 제공 기관/도메인 모니터링 레코드이며 인증서로 표시하지 않습니다.
- `regional-source` — 지역별 discovery source.
- `language-watch` — 언어 지원 모니터.

## 상태 모델

✅ **Free** · ⚠️ **Conditional** · ⚪ **Unknown** · ❌ **Paid / reference**

`Free`는 현재 공식 출처에서 의무적인 비용 없이 이용할 수 있는 경로가 있음을 뜻합니다. `Conditional`에는 학생/교육자 접근, voucher, scholarship, campaign, partner access 및 과정별 규칙이 포함됩니다.

회사명, 제품명, credential 이름, 표준 및 약어는 번역하지 않고 원문을 유지합니다.

## 개인 학습 시스템

웹 애플리케이션은 검색, 필터, 시작/완료 상태, XP, 랭크, 진행률 및 JSON export/import를 제공합니다. 진행 정보는 브라우저에 로컬로 저장됩니다.

Progression: **Explore → Beginner → Foundation → Intermediate → Advanced → Professional → Expert → Master**.

## 자동화

Extractor는 JSON-LD, 제목, 적절한 same-origin links 및 sitemap을 사용합니다. 각 레코드에는 source URL, 추출 방법 및 날짜가 저장됩니다. Freshness는 접근 가능성을 확인하지만, 그것만으로 Credential의 유효성이나 무료 여부를 증명하지는 않습니다.

최종 기준 검토: 2026-08-31.
