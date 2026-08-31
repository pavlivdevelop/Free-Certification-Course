# Free Certification Course — العربية

فهرس قائم على المصادر الرسمية للشهادات و certifications و Digital Badges و Credentials القابلة للتحقق.

> **اللغات** · [Русский](README.ru.md) · [English](README.en.md) · [Українська](README.uk.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Français](README.fr.md) · [Português](README.pt.md) · [Polski](README.pl.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [العربية](README.ar.md)

## الهدف

بناء مكتبة عملية للـ credentials المجانية من دون اختلاق شهادات غير موجودة. تأتي الأسماء المحددة من صفحات الجهات المصدرة الرسمية؛ توسّع taxonomy نطاق التغطية لكنها لا تنشئ أسماء credentials.

## الحجم

تم تصميم الـ pipeline للتعامل مع **5,000–10,000+ سجل مرصود** مع قابلية التوسع المستمر. يعتمد التوسع على أسماء حقيقية مستخرجة من الصفحات الرسمية مع الحفاظ على provenance.

## التغطية

AI · Generative AI · LLM · AI Agents · RAG · Machine Learning · MLOps · Python · Java · C/C++ · C# · Rust · Go · Web · Mobile · APIs · Databases · Data Engineering · Cybersecurity · AppSec · SOC · DFIR · Cloud · DevOps · SRE · Kubernetes · Networking · 5G/6G · Telecommunications · IoT · Embedded · RISC-V · FPGA · ASIC · Electronics · PCB · EDA · RF · SDR · Antennas · Microwave · EMC/EMI · DSP · Radar · Control Systems · Robotics · ROS · PLC/SCADA · Industrial Automation · Mechatronics · CAD/CAM/CAE · BIM · CFD/FEA · Digital Twins · CNC · 3D Printing · Metrology · Semiconductors · Materials · Mathematics · Statistics · Physics · Quantum · GIS · Remote Sensing · Aerospace · Avionics · Automotive · Energy · Medical Devices · Biotechnology · Chemistry · Environment · Smart Cities · Game/XR · Open Source · Software Supply Chain · Observability · Testing/QA · Technical Writing وغيرها.

## البنية

`providers/` — الجهات المصدرة، الدول، عناوين URL الرسمية وبيانات اللغة والمنطقة.

`credentials/` — أسماء credentials، مرشحو الاستخراج ووثائق registry.

`taxonomy/` — تصنيف تقني مضبوط ومستويات progression.

`evidence/` — provenance وأدلة الاستخراج والتحقق.

`status/` — freshness والإحصاءات وقواعد progression.

`data/` — datasets وexports المُنشأة.

`scripts/` — الاستخراج الحتمي، التطبيع، التحقق وأدوات freshness.

`site/` — كتالوج ويب مختصر وpersonal progress tracker.

`.github/workflows/` — الاستخراج والvalidation وعمليات freshness المجدولة.

## نموذج السجلات

- `credential` — credential أو badge باسم مؤكد.
- `credential-reference` — professional certification حقيقية للتوثيق والسياق؛ لا يعني ذلك أنها مجانية.
- `credential-candidate` — اسم دقيق شوهد في صفحة رسمية، بانتظار تصنيف evidence.
- `source-watch` — سجل مراقبة للمصدر ولا يُعرض كشهادة.
- `regional-source` — مصدر إقليمي.
- `language-watch` — مراقبة توفر اللغة.

## نموذج الحالة

✅ **Free** · ⚠️ **Conditional** · ⚪ **Unknown** · ❌ **Paid / reference**

`Free` تعني أن المصدر الرسمي الحالي يوفّر مساراً من دون دفع إلزامي. `Conditional` تشمل وصول الطلاب/المعلمين، vouchers، scholarships، الحملات، partner access وقواعد البرنامج المحددة.

تبقى أسماء الشركات والمنتجات وcredentials والمعايير والاختصارات كما هي ولا تتم ترجمتها.

## نظام التعلم الشخصي

يوفر تطبيق الويب البحث والفلاتر وحالات البدء/الإنجاز وXP والرتب ونسبة التقدم وJSON export/import. يبقى التقدم محفوظاً محلياً في المتصفح ولا يدخل في dataset العام.

Progression: **Explore → Beginner → Foundation → Intermediate → Advanced → Professional → Expert → Master**.

## الأتمتة

يستخدم Extractor بيانات JSON-LD والعناوين وروابط same-origin المؤهلة وsitemaps المتاحة. يحتفظ كل سجل بـ source URL وطريقة الاستخراج وتاريخ الاستخراج. تتحقق Freshness من إمكانية الوصول، لكن إمكانية الوصول وحدها لا تثبت صلاحية credential أو مجانيتها.

آخر مراجعة أساسية: 2026-08-31.
