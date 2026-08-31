# Free Certification Course — Français

Catalogue basé sur les sources officielles de certificats, certifications, Digital Badges et Credentials vérifiables.

> **Langues** · [Русский](README.ru.md) · [English](README.en.md) · [Українська](README.uk.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Français](README.fr.md) · [Português](README.pt.md) · [Polski](README.pl.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [العربية](README.ar.md)

## Objectif

Construire une bibliothèque pratique de credentials gratuits sans inventer de certificats. Les noms concrets proviennent des pages officielles des émetteurs. La taxonomie élargit la couverture sans créer de noms de credentials.

## Échelle

Le pipeline vise **5 000–10 000+ enregistrements observés** et une croissance continue, avec provenance conservée.

## Couverture

AI · Generative AI · LLM · AI Agents · RAG · Machine Learning · MLOps · Python · Java · C/C++ · C# · Rust · Go · Web · Mobile · APIs · Databases · Data Engineering · Cybersecurity · AppSec · SOC · DFIR · Cloud · DevOps · SRE · Kubernetes · Networking · 5G/6G · Telecommunications · IoT · Embedded · RISC-V · FPGA · ASIC · Electronics · PCB · EDA · RF · SDR · Antennas · Microwave · EMC/EMI · DSP · Radar · Control Systems · Robotics · ROS · PLC/SCADA · Industrial Automation · Mechatronics · CAD/CAM/CAE · BIM · CFD/FEA · Digital Twins · CNC · 3D Printing · Metrology · Semiconductors · Materials · Mathematics · Statistics · Physics · Quantum · GIS · Remote Sensing · Aerospace · Avionics · Automotive · Energy · Medical Devices · Biotechnology · Chemistry · Environment · Smart Cities · Game/XR · Open Source · Software Supply Chain · Observability · Testing/QA · Technical Writing et plus.

## Architecture

`providers/` — fournisseurs, pays, URLs officielles et métadonnées de langue/région.

`credentials/` — credentials nommés, candidats extraits et documentation du registre.

`taxonomy/` — taxonomie technique contrôlée et niveaux de progression.

`evidence/` — provenance, preuves d’extraction et vérification.

`status/` — fraîcheur, statistiques et règles de progression.

`data/` — datasets et exports générés.

`scripts/` — extraction déterministe, normalisation, validation et outils de fraîcheur.

`site/` — catalogue web compact et tracker personnel.

`.github/workflows/` — extraction, validation et contrôles de fraîcheur planifiés.

## Modèle de statut

✅ **Free** · ⚠️ **Conditional** · ⚪ **Unknown** · ❌ **Paid / reference**

`Free` signifie qu’une voie sans paiement obligatoire est indiquée par la source officielle actuelle. `Conditional` couvre accès étudiant/enseignant, voucher, scholarship, campagne, partenaire ou règle propre au cours.

Les noms de sociétés, produits, credentials, standards et abréviations restent inchangés.

## Système d’apprentissage

L’application permet la recherche, les filtres, le suivi de début/fin, les XP, les rangs, le pourcentage de progression et JSON export/import. La progression reste locale au navigateur.

Progression: **Explore → Beginner → Foundation → Intermediate → Advanced → Professional → Expert → Master**.

## Automatisation

L’extracteur utilise JSON-LD, les titres, les liens same-origin qualifiés et les sitemaps disponibles. Chaque enregistrement conserve son URL source, sa méthode d’extraction et sa date. La fraîcheur vérifie l’accessibilité, mais celle-ci ne prouve ni la validité ni la gratuité.

Dernière vérification de base : 31-08-2026.
