#!/usr/bin/env python3
"""Build conservative credential -> pathway-node candidate mappings.

These mappings are navigation/recommendation candidates only. They do not claim
that a credential teaches a node, and they never change credential verification
or free-status fields.
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data" / "catalog-expanded.json"
PATHWAYS = ROOT / "taxonomy" / "pathways.json"
CSV_OUT = ROOT / "status" / "CREDENTIAL-PATHWAY-CANDIDATES.csv"
JSON_OUT = ROOT / "data" / "pathway-candidates-lite.json"

# Conservative aliases. Scores are intentionally low-confidence discovery signals.
ALIASES = {
    "ai-literacy": ["ai literacy", "artificial intelligence", "generative ai", "genai"],
    "python": ["python", "pythonic"],
    "statistics": ["statistics", "statistical"],
    "linear-algebra": ["linear algebra"],
    "ml": ["machine learning", "ml ", " ml", "supervised learning", "unsupervised learning"],
    "deep-learning": ["deep learning", "neural network", "neural networks"],
    "llm": ["llm", "large language model", "large language models"],
    "rag": ["retrieval augmented", "retrieval-augmented", "rag"],
    "agents": ["ai agent", "ai agents", "agentic", "autonomous agent"],
    "mlops": ["mlops", "machine learning operations"],
    "ai-evaluation": ["ai evaluation", "llm evaluation", "model evaluation"],
    "it-foundations": ["it fundamentals", "it foundation", "information technology"],
    "networking-basics": ["networking", "computer network", "network fundamentals"],
    "tcp-ip": ["tcp/ip", "tcp-ip", "ipv4", "ipv6"],
    "routing-switching": ["routing", "switching", "ccna"],
    "wifi": ["wi-fi", "wifi", "wireless networking"],
    "network-automation": ["network automation", "netconf", "restconf"],
    "sdn": ["software defined networking", "sdn"],
    "telecom": ["telecommunications", "telecom", "mobile communications"],
    "5g-6g": ["5g", "6g"],
    "linux": ["linux", "red hat", "rhel"],
    "security-fundamentals": ["cybersecurity", "cyber security", "security fundamentals", "information security"],
    "iam": ["identity and access", "iam", "identity management"],
    "appsec": ["application security", "appsec", "secure software"],
    "soc": ["soc", "security operations", "siem"],
    "dfir": ["digital forensics", "incident response", "dfir"],
    "cloud-security": ["cloud security"],
    "zero-trust": ["zero trust", "zero-trust"],
    "programming-basics": ["programming fundamentals", "programming basics", "software development"],
    "git": ["git", "github", "gitlab"],
    "testing": ["software testing", "testing", "qa", "quality assurance"],
    "sql": ["sql", "database", "relational database"],
    "apis": ["api", "apis", "rest api", "graphql"],
    "web-development": ["web development", "frontend", "backend", "full stack"],
    "containers": ["docker", "container", "containers"],
    "ci-cd": ["ci/cd", "continuous integration", "continuous delivery", "continuous deployment"],
    "cloud-fundamentals": ["cloud", "aws", "azure", "google cloud", "gcp"],
    "iac": ["terraform", "infrastructure as code", "iac"],
    "kubernetes": ["kubernetes", "k8s"],
    "observability": ["observability", "opentelemetry", "monitoring"],
    "sre": ["site reliability", "sre"],
    "electronics-basics": ["electronics", "electrical engineering", "electronic engineering"],
    "digital-electronics": ["digital electronics", "logic design", "digital logic"],
    "c-programming": ["c programming", "c language", "c/c++"],
    "microcontrollers": ["microcontroller", "microcontrollers", "mcu"],
    "embedded-c": ["embedded c", "embedded systems", "embedded software"],
    "stm32-esp32": ["stm32", "esp32", "esp-idf"],
    "rtos": ["rtos", "freeRTOS", "real-time operating system"],
    "embedded-linux": ["embedded linux", "yocto", "buildroot"],
    "pcb-eda": ["pcb", "printed circuit board", "eda", "altium", "kicad"],
    "fpga": ["fpga", "verilog", "vhdl"],
    "risc-v": ["risc-v", "risc v"],
    "signals-systems": ["signals and systems", "signals & systems"],
    "dsp": ["digital signal processing", " dsp ", "signal processing"],
    "rf-basics": ["radio frequency", "rf engineering", "rf basics"],
    "antennas": ["antenna", "antennas"],
    "microwave": ["microwave", "microwave engineering"],
    "sdr": ["software defined radio", "sdr"],
    "emc-emi": ["emc", "emi", "electromagnetic compatibility"],
    "radar": ["radar", "radar systems"],
    "control-systems": ["control systems", "control engineering", "automatic control"],
    "robotics-basics": ["robotics", "robot"],
    "ros2": ["ros2", "ros 2", "robot operating system"],
    "plc": ["plc", "programmable logic controller"],
    "scada": ["scada", "supervisory control"],
    "industrial-robotics": ["industrial robotics", "industrial robot"],
    "uav": ["uav", "drone", "unmanned aerial"],
    "technical-drawing": ["technical drawing", "engineering drawing"],
    "cad-basics": ["cad", "computer aided design"],
    "3d-modeling": ["3d modeling", "3d modelling", "solidworks", "fusion 360"],
    "materials": ["materials science", "materials engineering"],
    "fea": ["finite element", "fea", "ansys mechanical"],
    "cfd": ["computational fluid", "cfd"],
    "cam": ["cam", "computer aided manufacturing"],
    "cnc": ["cnc", "computer numerical control"],
    "3d-printing": ["3d printing", "additive manufacturing"],
    "metrology": ["metrology", "measurement science"],
    "digital-twins": ["digital twin", "digital twins"],
    "math-basics": ["mathematics", "math fundamentals", "quantitative"],
    "algebra": ["algebra"],
    "calculus": ["calculus"],
    "probability": ["probability"],
    "numerical-methods": ["numerical methods", "numerical analysis"],
    "classical-physics": ["classical physics", "physics"],
    "electromagnetism": ["electromagnetism", "electromagnetic theory"],
    "quantum": ["quantum", "quantum computing", "quantum information"],
}


def norm(value: object) -> str:
    text = str(value or "").lower().replace("–", "-").replace("—", "-")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    rows = load_json(CATALOG)
    pathways = load_json(PATHWAYS)
    if not isinstance(rows, list):
        raise SystemExit("catalog-expanded.json must be an array")

    valid_nodes = set(pathways.get("node_levels", {}))
    node_to_tracks: dict[str, list[str]] = {n: [] for n in valid_nodes}
    for track in pathways.get("tracks", []):
        for node in track.get("nodes", []):
            node_to_tracks.setdefault(node, []).append(track.get("id", ""))

    compiled = {
        node: [(alias, re.compile(r"(?<![a-z0-9])" + re.escape(alias) + r"(?![a-z0-9])")) for alias in aliases]
        for node, aliases in ALIASES.items() if node in valid_nodes
    }

    out: list[dict[str, object]] = []
    for row in rows:
        record_type = norm(row.get("Record Type"))
        if record_type not in {"credential", "credential-candidate", "credential-reference"}:
            continue
        text = " | ".join(norm(row.get(k)) for k in ("Certificate/Badge", "Category", "Subcategory", "Organization"))
        hits: list[tuple[int, str, list[str]]] = []
        for node, patterns in compiled.items():
            reasons = [alias for alias, pattern in patterns if pattern.search(text)]
            if reasons:
                # Exact credential title/category hits are stronger than organization-only hits.
                title = norm(row.get("Certificate/Badge"))
                category_text = " ".join(norm(row.get(k)) for k in ("Category", "Subcategory"))
                title_hits = sum(1 for alias in reasons if re.search(r"(?<![a-z0-9])" + re.escape(alias) + r"(?![a-z0-9])", title))
                cat_hits = sum(1 for alias in reasons if re.search(r"(?<![a-z0-9])" + re.escape(alias) + r"(?![a-z0-9])", category_text))
                score = min(100, 35 + title_hits * 25 + cat_hits * 15 + min(10, len(reasons) * 5))
                hits.append((score, node, reasons))

        for score, node, reasons in sorted(hits, reverse=True)[:4]:
            out.append({
                "credential_id": str(row.get("ID", "")),
                "credential_name": row.get("Certificate/Badge", ""),
                "pathway_node": node,
                "pathway_level": pathways["node_levels"].get(node, ""),
                "pathway_tracks": node_to_tracks.get(node, []),
                "match_score": score,
                "match_reasons": reasons,
                "mapping_status": "candidate",
                "evidence_status": row.get("Evidence Status", ""),
                "record_type": row.get("Record Type", ""),
                "official_url": row.get("Official URL", ""),
            })

    fieldnames = [
        "credential_id", "credential_name", "pathway_node", "pathway_level", "pathway_tracks",
        "match_score", "match_reasons", "mapping_status", "evidence_status", "record_type", "official_url",
    ]
    CSV_OUT.parent.mkdir(parents=True, exist_ok=True)
    with CSV_OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in out:
            row = dict(item)
            row["pathway_tracks"] = ";".join(item["pathway_tracks"])
            row["match_reasons"] = ";".join(item["match_reasons"])
            writer.writerow(row)

    lite = [
        {
            "credential_id": item["credential_id"],
            "pathway_node": item["pathway_node"],
            "pathway_level": item["pathway_level"],
            "pathway_tracks": item["pathway_tracks"],
            "match_score": item["match_score"],
            "mapping_status": "candidate",
            "evidence_status": item["evidence_status"],
        }
        for item in out
    ]
    JSON_OUT.write_text(json.dumps(lite, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"pathway_candidate_mappings={len(out)}")
    print(f"pathway_candidate_credentials={len({x['credential_id'] for x in out})}")
    print(f"pathway_candidate_nodes={len({x['pathway_node'] for x in out})}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
