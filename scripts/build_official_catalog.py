#!/usr/bin/env python3
"""Build the canonical OpenCertAtlas dataset from curated seeds + observed issuer data.

Discovery is never treated as verification. Curated seed metadata is preserved;
extracted observations remain candidates until evidence promotion. In particular,
the public free-core is deliberately stricter than an observed free-price signal:
only explicitly promoted ``verified-free`` credentials enter it.
"""
from pathlib import Path
import csv, json, hashlib
from datetime import date

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"; CRED = ROOT / "credentials"; STATUS = ROOT / "status"
TODAY = str(date.today())
OUT = DATA / "catalog-expanded.csv"; OJSON = DATA / "catalog-expanded.json"
FREE = DATA / "free-core.csv"; COND = DATA / "conditional.csv"
CAND = CRED / "extracted-candidates.jsonl"
FIELDS = ["ID","Country","Organization","Certificate/Badge","Record Type","Category","Subcategory","Level","Price Status","Conditions","Exam/Assessment","Duration","Language","Available from Russia","Validity","Credly/Verification","LinkedIn","Official URL","Priority","Completion Status","Evidence Status","Last Reviewed","Source Page","Extraction Method","Confidence"]
MAP = {
"AI":["artificial intelligence","generative ai","genai","llm","language model","agentforce","ai agent","machine learning","deep learning","computer vision","nlp","prompt","rag"],
"Cybersecurity":["cybersecurity","security","soc","siem","pentest","penetration","forensic","zero trust","iam","identity","appsec"],
"Cloud":["cloud","aws","azure","google cloud","oci","serverless"],
"DevOps":["devops","ci/cd","gitops","terraform","ansible","kubernetes","docker","sre","platform"],
"Networking":["network","routing","switching","ipv4","ipv6","dns","wi-fi","5g","6g","telecom","fiber","voip"],
"Python":["python"],"Data":["data","sql","database","analytics","tableau","power bi","mongodb","postgres"],
"Electronics":["electronics","pcb","eda","fpga","asic","semiconductor","analog","power electronics","spice"],
"RF":["rf","radio","sdr","antenna","microwave","millimeter","emc","emi","radar","lidar"],
"Embedded":["embedded","stm32","esp32","arduino","rtos","risc-v","arm","microcontroller","iot","physical computing"],
"Robotics":["robot","ros","plc","scada","industrial automation","mechatronics","uav","drone"],
"CAD":["cad","cam","cae","bim","fea","cfd","digital twin","cnc","3d printing","metrology","plm"],
"Mathematics":["mathematics","math","calculus","linear algebra","statistics","probability","numerical"],
"Physics":["physics","quantum","geophysics","astronomy"],"Chemistry":["chemistry"],"Biotechnology":["biotechnology","bioinformatics"],
"GIS":["gis","geospatial","remote sensing","surveying"],"Aerospace":["aerospace","avionics","space systems","satellite"],
"Automotive":["automotive","adas","electric vehicle","ev"],"Energy":["energy","power systems","smart grid","renewable","battery"],
"Medical Devices":["medical device","biomedical","healthtech"],"Environment":["environment","climate","sustainability"],
"Project/Product":["project management","product management","agile","scrum"],"UX/Design":["ux","accessibility","design thinking"],
"Testing/QA":["testing","quality assurance","qa automation","performance testing"],"Open Source":["open source","linux","apache","eclipse"],
"Game/XR":["game development","unity","unreal"," xr "," vr "],"Blockchain":["blockchain","web3","smart contract"],"Technical Writing":["technical writing","documentation"]}
VERIFIED_FREE_EVIDENCE = {"verified-free", "issuer-verified-free", "manual-verified-free"}

def readp(p):
    with p.open(encoding="utf-8-sig", newline="") as f: return list(csv.DictReader(f))

def norm(r):
    # Accept historical seed spelling/case while emitting one canonical schema.
    lower = {str(k).strip().casefold(): v for k,v in r.items()}
    def g(*keys, d=""):
        for k in keys:
            v = r.get(k)
            if v not in (None, ""): return str(v).strip()
            v = lower.get(k.casefold())
            if v not in (None, ""): return str(v).strip()
        return d
    title = g("Certificate/Badge","credential_name",d="Unnamed")
    org = g("Organization","organization",d="Unknown")
    url = g("Official URL","official_url")
    text = " ".join([title,org,g("Subcategory"),g("Conditions"),g("Category")]).lower()
    cat = g("Category") or max(((sum(v in text for v in terms),k) for k,terms in MAP.items()),default=(0,"Other Technical"))[1]
    rid = g("ID") or "ROW-" + hashlib.sha1((org+"|"+title+"|"+url).encode()).hexdigest()[:12].upper()
    return {"ID":rid,"Country":g("Country","country",d="International"),"Organization":org,"Certificate/Badge":title,"Record Type":g("Record Type","record_type",d="credential"),"Category":cat,"Subcategory":g("Subcategory",d=cat),"Level":g("Level",d="Discovery"),"Price Status":g("Price Status","Price status","price_status",d="⚪ Unknown"),"Conditions":g("Conditions",d="Verify official page"),"Exam/Assessment":g("Exam/Assessment","Exam/assessment",d="Provider-specific"),"Duration":g("Duration",d="Varies"),"Language":g("Language",d="Provider-dependent"),"Available from Russia":g("Available from Russia",d="Unknown"),"Validity":g("Validity",d="Varies"),"Credly/Verification":g("Credly/Verification",d="Provider-defined"),"LinkedIn":g("LinkedIn",d="Varies"),"Official URL":url,"Priority":g("Priority",d="B"),"Completion Status":g("Completion Status","Completion status",d="Не начато"),"Evidence Status":g("Evidence Status","Review status","Review Status","evidence_status",d="official-page-extraction"),"Last Reviewed":g("Last Reviewed","Last reviewed","last_reviewed",d=TODAY),"Source Page":g("Source Page","source_page",d=url),"Extraction Method":g("Extraction Method","extraction_method",d="curated"),"Confidence":g("Confidence",d="candidate")}

def is_verified_free(r):
    return (
        r["Record Type"] == "credential"
        and r["Evidence Status"].strip().casefold() in VERIFIED_FREE_EVIDENCE
        and r["Price Status"].startswith("✅")
        and bool(r["Source Page"].strip())
        and bool(r["Last Reviewed"].strip())
    )

def main():
    rows=[]; seed_files=[]
    for p in sorted(DATA.glob("catalog-*.csv")):
        if p.name in {"catalog-expanded.csv","catalog.csv"}: continue
        seed_files.append(p)
    # catalog.csv is accepted only when it contains real seed rows, not a tiny placeholder.
    if (DATA/"catalog.csv").exists() and (DATA/"catalog.csv").stat().st_size > 20:
        seed_files.append(DATA/"catalog.csv")
    for p in seed_files:
        rows += [norm(x) for x in readp(p) if x.get("Certificate/Badge") or x.get("credential_name")]
    if CAND.exists():
        with CAND.open(encoding="utf-8") as f:
            for line in f:
                if line.strip(): rows.append(norm(json.loads(line)))
    unique={}
    for r in rows:
        key=(r["Organization"].casefold(),r["Certificate/Badge"].casefold(),r["Official URL"])
        old=unique.get(key)
        if old is None or (old["Record Type"]=="credential-candidate" and r["Record Type"]!="credential-candidate"):
            unique[key]=r
    rows=sorted(unique.values(),key=lambda r:(r["Category"],r["Organization"].casefold(),r["Certificate/Badge"].casefold()))
    DATA.mkdir(exist_ok=True); STATUS.mkdir(exist_ok=True)
    free=[r for r in rows if is_verified_free(r)]
    conditional=[r for r in rows if r["Price Status"].startswith("⚠️")]
    for p,subset in ((OUT,rows),(FREE,free),(COND,conditional)):
        with p.open("w",encoding="utf-8-sig",newline="") as f:
            w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader(); w.writerows(subset)
    OJSON.write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding="utf-8")
    (STATUS/"CATALOG-STATS.md").write_text(f"# Catalog statistics\n\n- records: {len(rows)}\n- free signals: {sum(r['Price Status'].startswith('✅') for r in rows)}\n- verified free-core: {len(free)}\n- conditional: {len(conditional)}\n- candidates: {sum(r['Record Type']=='credential-candidate' for r in rows)}\n- built: {TODAY}\n",encoding="utf-8")
    print(f"records={len(rows)} free_signals={sum(r['Price Status'].startswith('✅') for r in rows)} verified_free_core={len(free)} conditional={len(conditional)}")
    return 0 if len(rows)>=5000 else 2
if __name__=="__main__": raise SystemExit(main())