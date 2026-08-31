# Free Certification Course — 日本語

公式ソースを基盤とした、証明書、certifications、Digital Badges、検証可能な Credentials のカタログです。

> **言語** · [Русский](README.ru.md) · [English](README.en.md) · [Українська](README.uk.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Français](README.fr.md) · [Português](README.pt.md) · [Polski](README.pl.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [العربية](README.ar.md)

## 目的

実在しない証明書を作らず、無料の credentials を実用的に発見できるライブラリを構築します。具体的な名称は発行元の公式ページから取得し、taxonomy は対象分野を広げますが credential 名を生成しません。

## 規模

パイプラインは **5,000–10,000+ 件の観測レコード** と継続的な拡張を想定しています。規模は公式ページからの実名抽出と provenance の保存によって実現します。

## 対象分野

AI · Generative AI · LLM · AI Agents · RAG · Machine Learning · MLOps · Python · Java · C/C++ · C# · Rust · Go · Web · Mobile · APIs · Databases · Data Engineering · Cybersecurity · AppSec · SOC · DFIR · Cloud · DevOps · SRE · Kubernetes · Networking · 5G/6G · Telecommunications · IoT · Embedded · RISC-V · FPGA · ASIC · Electronics · PCB · EDA · RF · SDR · Antennas · Microwave · EMC/EMI · DSP · Radar · Control Systems · Robotics · ROS · PLC/SCADA · Industrial Automation · Mechatronics · CAD/CAM/CAE · BIM · CFD/FEA · Digital Twins · CNC · 3D Printing · Metrology · Semiconductors · Materials · Mathematics · Statistics · Physics · Quantum · GIS · Remote Sensing · Aerospace · Avionics · Automotive · Energy · Medical Devices · Biotechnology · Chemistry · Environment · Smart Cities · Game/XR · Open Source · Software Supply Chain · Observability · Testing/QA · Technical Writing など。

## アーキテクチャ

`providers/` — プロバイダー、国、公式 URL、言語・地域メタデータ。

`credentials/` — credential 名、抽出候補、registry ドキュメント。

`taxonomy/` — 管理された技術 taxonomy と progression レベル。

`evidence/` — provenance、抽出証拠、検証情報。

`status/` — freshness、統計、progression rules。

`data/` — 生成された datasets と exports。

`scripts/` — 決定論的な抽出、正規化、検証、freshness ツール。

`site/` — コンパクトな Web カタログと個人用 progress tracker。

`.github/workflows/` — 定期的な抽出、検証、freshness 自動化。

## レコードモデル

- `credential` — registry で確認された credential または badge。
- `credential-reference` — 実在する professional certification の参照記録。無料とは限りません。
- `credential-candidate` — 発行元公式ページで確認された正確な名称で、evidence 分類待ち。
- `source-watch` — プロバイダー/ドメイン監視記録。証明書として表示しません。
- `regional-source` — 地域ソース。
- `language-watch` — 言語対応監視。

## ステータス

✅ **Free** · ⚠️ **Conditional** · ⚪ **Unknown** · ❌ **Paid / reference**

`Free` は現在の公式ソースが必須の支払いなしの経路を提供することを意味します。`Conditional` は学生/教育者アクセス、voucher、scholarship、campaign、partner access、コース固有条件などを含みます。

会社名、製品名、credential 名、標準規格名、略語は翻訳せず原文を維持します。

## 個人学習システム

Web アプリは検索、フィルター、開始/完了、XP、ランク、進捗率、JSON export/import を提供します。進捗はブラウザー内にのみ保存されます。

Progression: **Explore → Beginner → Foundation → Intermediate → Advanced → Professional → Expert → Master**。

## 自動化

Extractor は JSON-LD、見出し、適切な same-origin links、利用可能な sitemap を使用します。各レコードには source URL、抽出方法、抽出日を保存します。Freshness はアクセス可能性を確認しますが、それだけで credential の有効性や無料性を保証しません。

最終基準確認: 2026-08-31.
