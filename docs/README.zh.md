# Free Certification Course — 中文

基于官方来源的证书、认证、Digital Badges 和可验证 Credentials 目录。

> **语言** · [Русский](README.ru.md) · [English](README.en.md) · [Українська](README.uk.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Français](README.fr.md) · [Português](README.pt.md) · [Polski](README.pl.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [العربية](README.ar.md)

## 目标

建立一个实用的免费 Credential 发现库，不制造虚假的证书。具体名称来自发行方官方页面；taxonomy 扩展覆盖范围，但不会生成不存在的 Credential 名称。

## 规模

构建流水线面向 **5,000–10,000+ 条观测记录**，并可继续扩展。规模来自官方页面中的真实名称以及保存的来源信息，而不是简单组合“供应商 × 主题”。

## 覆盖范围

AI · Generative AI · LLM · AI Agents · RAG · Machine Learning · MLOps · Python · Java · C/C++ · C# · Rust · Go · Web · Mobile · APIs · Databases · Data Engineering · Cybersecurity · AppSec · SOC · DFIR · Cloud · DevOps · SRE · Kubernetes · Networking · 5G/6G · Telecommunications · IoT · Embedded · RISC-V · FPGA · ASIC · Electronics · PCB · EDA · RF · SDR · Antennas · Microwave · EMC/EMI · DSP · Radar · Control Systems · Robotics · ROS · PLC/SCADA · Industrial Automation · Mechatronics · CAD/CAM/CAE · BIM · CFD/FEA · Digital Twins · CNC · 3D Printing · Metrology · Semiconductors · Materials · Mathematics · Statistics · Physics · Quantum · GIS · Remote Sensing · Aerospace · Avionics · Automotive · Energy · Medical Devices · Biotechnology · Chemistry · Environment · Smart Cities · Game/XR · Open Source · Software Supply Chain · Observability · Testing/QA · Technical Writing 等。

## 架构

`providers/` — 供应商、国家、官方 URL、语言与区域信息。

`credentials/` — 已命名 Credentials、提取候选和 Registry 文档。

`taxonomy/` — 受控技术分类和学习进阶等级。

`evidence/` — 来源、提取证据和验证信息。

`status/` — freshness、统计数据和 progression rules。

`data/` — 自动生成的数据集和导出文件。

`scripts/` — 确定性提取、标准化、验证和 freshness 工具。

`site/` — 精简网页目录和个人学习进度追踪器。

`.github/workflows/` — 定时提取、验证和 freshness 自动化。

## 记录模型

- `credential` — 已确认名称的 Credential 或 Badge。
- `credential-reference` — 合法的 professional certification 参考记录；不表示免费。
- `credential-candidate` — 在官方页面发现的确切名称，等待 evidence 分类。
- `source-watch` — 供应商/领域监控记录，绝不显示为证书。
- `regional-source` — 区域发现来源。
- `language-watch` — 语言可用性监控。

## 状态模型

✅ **Free** · ⚠️ **Conditional** · ⚪ **Unknown** · ❌ **Paid / reference**

`Free` 表示当前官方来源支持无需强制付费的路径。`Conditional` 包括学生/教师资格、voucher、scholarship、campaign、partner access 和课程特定规则。

公司名称、产品名称、Credential 名称、标准和缩写保持原样，不翻译。

## 个人学习系统

Web 应用支持搜索、筛选、开始/完成控制、XP、等级、进度百分比以及 JSON export/import。进度只保存在用户浏览器中，不写入公开数据集。

Progression: **Explore → Beginner → Foundation → Intermediate → Advanced → Professional → Expert → Master**。

## 自动化

Extractor 使用 JSON-LD、标题、same-origin links 和 sitemap。每条记录都会保存 source URL、提取方法与日期。Freshness 只检查来源可达性；可达性本身不能证明 Credential 仍然有效或免费。

最后基线检查：2026-08-31。
