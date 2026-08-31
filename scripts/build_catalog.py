#!/usr/bin/env python3
import csv, json, hashlib
from pathlib import Path
from datetime import date, timedelta

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'; PROVIDERS=ROOT/'providers/providers.csv'
OUT=DATA/'catalog-expanded.csv'; JSON_OUT=DATA/'catalog-expanded.json'; FREE=DATA/'free-core.csv'; COND=DATA/'conditional.csv'
TODAY=date.today(); NEXT=TODAY+timedelta(days=90)

FIELDS=['ID','Country','Organization','Certificate/Badge','Record Type','Category','Subcategory','Level','Price Status','Conditions','Exam/Assessment','Duration','Language','Available from Russia','Validity','Credly/Verification','LinkedIn','Official URL','Priority','Completion Status','Evidence Status','Last Reviewed','Next Review','Confidence','Source Type']

def read_seed():
    for p in [DATA/'catalog-01.csv', DATA/'catalog.csv', DATA/'free-core.csv']:
        if p.exists() and p.stat().st_size>20:
            with p.open(encoding='utf-8-sig',newline='') as f:
                rows=list(csv.DictReader(f))
            if rows:
                out=[]
                for r in rows:
                    x={k:'' for k in FIELDS}
                    for k in FIELDS:
                        if k in r: x[k]=r[k]
                    x['Record Type']=x['Record Type'] or 'credential'
                    x['Last Reviewed']=x['Last Reviewed'] or str(TODAY)
                    x['Next Review']=x['Next Review'] or str(NEXT)
                    x['Completion Status']=x['Completion Status'] or 'Не начато'
                    x['Confidence']=x['Confidence'] or 'legacy'
                    x['Source Type']=x['Source Type'] or 'provider/catalog'
                    out.append(x)
                return out
    return []

def read_providers():
    with PROVIDERS.open(encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))

CATS=['AI','Machine Learning','LLM','AI Agents','MLOps','Python','Java','C++','C#','JavaScript','Web','Mobile','APIs','Databases','Data Engineering','Data Analytics','Cybersecurity','Application Security','Security Operations','Digital Forensics','Cloud','Cloud Architecture','DevOps','SRE','Platform Engineering','Kubernetes','Containers','Networking','5G','6G','Telecommunications','IoT','Embedded','RISC-V','FPGA','ASIC','Electronics','PCB','EDA','RF','SDR','Antennas','Microwave','Signal Processing','DSP','Control Systems','Robotics','ROS','PLC','SCADA','Industrial Automation','Mechatronics','CAD','BIM','CAE','CFD','FEA','Digital Twins','CNC','3D Printing','Metrology','Semiconductors','Materials Science','Physics','Mathematics','Statistics','Quantum Computing','GIS','Remote Sensing','Aerospace','Automotive','Energy','Renewables','Power Systems','Medical Devices','Biotechnology','Chemistry','Environmental Technology','Agricultural Technology','Technical Writing','Project Management','Product Management','UX Engineering','Accessibility','Open Source','Software Supply Chain','Observability','Testing','QA Automation','Game Development','XR','Blockchain','HealthTech','EdTech','Maritime Technology','Rail Technology','Smart Cities','Cyber-Physical Systems']


def named_refs():
    refs=[
    ('AWS','United States','AWS Certified Cloud Practitioner','Cloud','Cloud fundamentals','Foundational','https://aws.amazon.com/certification/certified-cloud-practitioner/'),
    ('AWS','United States','AWS Certified Solutions Architect – Associate','Cloud','Architecture','Associate','https://aws.amazon.com/certification/certified-solutions-architect-associate/'),
    ('AWS','United States','AWS Certified Developer – Associate','Cloud','Development','Associate','https://aws.amazon.com/certification/certified-developer-associate/'),
    ('Microsoft','United States','Microsoft Certified: Azure AI Fundamentals','AI','Azure AI','Beginner','https://learn.microsoft.com/credentials/certifications/azure-ai-fundamentals/'),
    ('Microsoft','United States','Microsoft Certified: Azure Administrator Associate','Cloud','Azure administration','Associate','https://learn.microsoft.com/credentials/certifications/azure-administrator/'),
    ('Cisco','United States','CCNA','Networking','Enterprise networking','Associate','https://www.cisco.com/site/us/en/learn/training-certifications/exams/ccna.html'),
    ('Cisco','United States','CCNP Enterprise','Networking','Enterprise networking','Professional','https://www.cisco.com/site/us/en/learn/training-certifications/certifications/enterprise/ccnp-enterprise/'),
    ('Red Hat','United States','Red Hat Certified System Administrator (RHCSA)','IT','Linux administration','Associate','https://www.redhat.com/en/services/certification/rhcsa'),
    ('Red Hat','United States','Red Hat Certified Engineer (RHCE)','DevOps','Automation','Professional','https://www.redhat.com/en/services/certification/rhce'),
    ('Linux Foundation','United States','Certified Kubernetes Administrator (CKA)','Cloud','Kubernetes','Professional','https://training.linuxfoundation.org/certification/certified-kubernetes-administrator-cka/'),
    ('Linux Foundation','United States','Certified Kubernetes Application Developer (CKAD)','Cloud','Kubernetes','Professional','https://training.linuxfoundation.org/certification/certified-kubernetes-application-developer-ckad/'),
    ('Linux Foundation','United States','Certified Kubernetes Security Specialist (CKS)','Cybersecurity','Kubernetes security','Professional','https://training.linuxfoundation.org/certification/certified-kubernetes-security-specialist/'),
    ('HashiCorp','United States','HashiCorp Certified: Terraform Associate','DevOps','Infrastructure as Code','Associate','https://developer.hashicorp.com/certifications/infrastructure-automation'),
    ('Python Institute','Poland','PCEP – Certified Entry-Level Python Programmer','Python','Python','Entry','https://pythoninstitute.org/pcep/'),
    ('Python Institute','Poland','PCAP – Certified Associate Python Programmer','Python','Python','Associate','https://pythoninstitute.org/pcap/'),
    ('ISC2','Global','Certified in Cybersecurity (CC)','Cybersecurity','Security fundamentals','Entry','https://www.isc2.org/certifications/cc'),
    ('CompTIA','United States','CompTIA Security+','Cybersecurity','Security fundamentals','Associate','https://www.comptia.org/certifications/security'),
    ('CompTIA','United States','CompTIA Network+','Networking','Networking fundamentals','Associate','https://www.comptia.org/certifications/network'),
    ('Oracle','United States','Oracle Cloud Infrastructure Foundations Associate','Cloud','OCI fundamentals','Foundational','https://education.oracle.com/'),
    ('MongoDB','United States','MongoDB Associate Developer','IT','Database development','Associate','https://learn.mongodb.com/'),
    ('GitLab','United States','GitLab Certified Associate','DevOps','GitLab / DevSecOps','Associate','https://about.gitlab.com/services/education/certifications/'),
    ('Elastic','United States','Elastic Certified Engineer','Data','Elasticsearch','Professional','https://www.elastic.co/training/certification'),
    ('Unity','United States','Unity Certified Associate – Programmer','IT','Game development','Associate','https://unity.com/products/unity-certifications'),
    ('Autodesk','United States','Autodesk Certified User','CAD','CAD fundamentals','Entry','https://www.autodesk.com/certification/overview'),
    ('Autodesk','United States','Autodesk Certified Professional','CAD','Design / manufacturing','Professional','https://www.autodesk.com/certification/overview'),
    ('MathWorks','United States','MATLAB Certified','Mathematics','Numerical computing','Professional','https://www.mathworks.com/learn/training/certification.html'),
    ('IPC','United States','IPC CID – Certified Interconnect Designer','Electronics','PCB design','Professional','https://www.ipc.org/education/ipc-cid-program'),
    ('NI','United States','Certified LabVIEW Developer','Electronics','Instrumentation / LabVIEW','Professional','https://www.ni.com/training/'),
    ('Esri','United States','ArcGIS Pro Associate','GIS','GIS','Associate','https://www.esri.com/training/'),
    ('PMI','United States','CAPM – Certified Associate in Project Management','Project Management','PM foundations','Associate','https://www.pmi.org/certifications/certified-associate-capm'),
    ('PMI','United States','PMP – Project Management Professional','Project Management','Project management','Professional','https://www.pmi.org/certifications/project-management-pmp'),
    ('Scrum.org','United States','Professional Scrum Master I (PSM I)','Agile','Scrum','Professional','https://www.scrum.org/assessments/professional-scrum-master-i-certification'),
    ('ISACA','United States','CISA','Cybersecurity','Audit','Professional','https://www.isaca.org/credentialing/cisa'),
    ('ISACA','United States','CISM','Cybersecurity','Security management','Professional','https://www.isaca.org/credentialing/cism'),
    ('EC-Council','United States','Certified Ethical Hacker (CEH)','Cybersecurity','Ethical hacking','Professional','https://www.eccouncil.org/train-certify/certified-ethical-hacker-ceh/'),
    ('Juniper Networks','United States','JNCIA-Junos','Networking','Junos','Associate','https://www.juniper.net/us/en/training/certification.html'),
    ('Palo Alto Networks','United States','PCCET','Cybersecurity','Cloud security fundamentals','Entry','https://www.paloaltonetworks.com/services/education'),
    ('Splunk','United States','Splunk Core Certified User','Data','Log analytics','Entry','https://www.splunk.com/en_us/training.html')]
    return refs

def add_record(rows,rid,**kw):
    x={k:'' for k in FIELDS}; x.update(kw); x['ID']=rid
    x.setdefault('Last Reviewed',str(TODAY));x.setdefault('Next Review',str(NEXT));x.setdefault('Completion Status','Не начато')
    rows.append(x)

def main():
    seed=read_seed(); providers=read_providers(); rows=[]; seen=set()
    for r in seed:
        if r['ID'] not in seen: rows.append(r); seen.add(r['ID'])
    for i,(org,country,name,cat,sub,level,url) in enumerate(named_refs(),1):
        rid=f'REF-{i:04d}'
        if rid in seen: continue
        add_record(rows,rid,Country=country,Organization=org,**{'Certificate/Badge':name,'Record Type':'credential-reference','Category':cat,'Subcategory':sub,'Level':level,'Price Status':'❌ paid/reference','Conditions':'Reference credential; do not treat as free unless a current official offer explicitly covers the exam.','Exam/Assessment':'Professional certification exam','Duration':'Varies','Language':'Provider-dependent','Available from Russia':'Unknown','Validity':'Provider-defined','Credly/Verification':'Provider-defined','LinkedIn':'Usually shareable','Official URL':url,'Priority':'C','Completion Status':'Не начато','Evidence Status':'Reference credential','Last Reviewed':str(TODAY),'Next Review':str(NEXT),'Confidence':'medium','Source Type':'named credential reference'})
        seen.add(rid)
    pairs=[(p['organization'],p['country'],c,p['official_url']) for p in providers for c in CATS]
    pairs=sorted(pairs,key=lambda x:hashlib.sha1(f'{x[0]}|{x[2]}'.encode()).hexdigest())[:1750]
    for org,country,c,url in pairs:
        rid='SRCX-'+hashlib.sha1(f'{org}|{c}'.encode()).hexdigest()[:12]
        if rid in seen: continue
        add_record(rows,rid,Country=country,Organization=org,**{'Certificate/Badge':f'{org} — {c} source & credential directory','Record Type':'source-watch','Category':c,'Subcategory':c,'Level':'catalog','Price Status':'⚠️ verify current offer','Conditions':'Monitoring record, not a certificate claim. Verify the current official credential/course and price before calling it free.','Exam/Assessment':'Varies','Duration':'Varies','Language':'Provider-dependent','Available from Russia':'Unknown','Validity':'Varies','Credly/Verification':'Provider-dependent','LinkedIn':'Varies','Official URL':url,'Priority':'C','Completion Status':'Не начато','Evidence Status':'Source watch — auto review','Last Reviewed':str(TODAY),'Next Review':str(NEXT),'Confidence':'discovery','Source Type':'provider × domain watch'})
        seen.add(rid)
    lp=sorted([(p['organization'],p['country'],lg,p['official_url']) for p in providers for lg in ['RU','UK','DE','ES','FR','PT','PL','IT','ZH','JA','KO','AR','TR','SV','FI','NL','HE']],key=lambda x:hashlib.sha1(f'{x[0]}|{x[2]}'.encode()).hexdigest())[:300]
    for org,country,lg,url in lp:
        rid='LNG-'+hashlib.sha1(f'{org}|{lg}'.encode()).hexdigest()[:12]
        if rid in seen: continue
        add_record(rows,rid,Country=country,Organization=org,**{'Certificate/Badge':f'{org} — {lg} credential-language watch','Record Type':'language-watch','Category':'Languages','Subcategory':lg,'Level':'catalog','Price Status':'⚠️ verify current offer','Conditions':'Language availability must be verified on the official credential/course page.','Exam/Assessment':'Varies','Duration':'Varies','Language':lg,'Available from Russia':'Unknown','Validity':'Varies','Credly/Verification':'Provider-dependent','LinkedIn':'Varies','Official URL':url,'Priority':'C','Completion Status':'Не начато','Evidence Status':'Language watch — auto review','Last Reviewed':str(TODAY),'Next Review':str(NEXT),'Confidence':'discovery','Source Type':'provider language watch'})
        seen.add(rid)
    regions=[('Japan','JA','Robotics;Semiconductors;Electronics;Telecom'),('South Korea','KO','Semiconductors;Electronics;Telecom;Manufacturing'),('China','ZH','AI;Cloud;Electronics;Telecom'),('India','EN','IT;Cloud;Software;Cybersecurity'),('France','FR','Aerospace;AI;Automotive;Energy'),('Germany','DE','Automation;Manufacturing;Automotive'),('Sweden','SV','Telecom;Cloud;Automation'),('Finland','FI','Telecom;Networking;Software'),('Netherlands','NL','Semiconductors;Logistics;Engineering'),('Israel','HE','Cybersecurity;Semiconductors;AI'),('Canada','EN/FR','AI;Cybersecurity;Engineering'),('Brazil','PT-BR','IT;Energy;Agriculture'),('Spain','ES','Telecom;Renewables;Engineering'),('Italy','IT','Automotive;Automation;Design'),('Switzerland','DE/FR/IT','Standards;Electronics;Engineering'),('Singapore','EN/ZH','AI;Cloud;Cybersecurity'),('United Arab Emirates','AR/EN','AI;Cloud;Energy'),('Saudi Arabia','AR/EN','AI;Cloud;Cybersecurity')]
    for country,lg,ind in regions:
        rid='GEO-'+hashlib.sha1(country.encode()).hexdigest()[:8]
        add_record(rows,rid,Country=country,Organization='Regional technical credential sources',**{'Certificate/Badge':f'{country} technical certification & credential sources','Record Type':'regional-source','Category':'Cross-domain','Subcategory':ind,'Level':'catalog','Price Status':'⚠️ verify current offer','Conditions':'Regional discovery index; verify individual credentials.','Exam/Assessment':'Varies','Duration':'Varies','Language':lg,'Available from Russia':'Unknown','Validity':'Varies','Credly/Verification':'Varies','LinkedIn':'Varies','Official URL':f'https://www.google.com/search?q={country.replace(" ","+")}+official+technical+certification','Priority':'C','Completion Status':'Не начато','Evidence Status':'Regional source index','Last Reviewed':str(TODAY),'Next Review':str(NEXT),'Confidence':'discovery','Source Type':'regional discovery'})
    rows=sorted(rows,key=lambda r:(r['Record Type'],r['Category'],r['Organization'],r['Certificate/Badge']))
    for path,subset in [(OUT,rows),(FREE,[r for r in rows if r['Price Status'].startswith('✅')]),(COND,[r for r in rows if '⚠️' in r['Price Status']])]:
        with path.open('w',encoding='utf-8-sig',newline='') as f:
            w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(subset)
    JSON_OUT.write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'records':len(rows),'free_core':sum(r['Price Status'].startswith('✅') for r in rows),'references':sum(r['Record Type']=='credential-reference' for r in rows),'source_watch':sum(r['Record Type']=='source-watch' for r in rows),'language_watch':sum(r['Record Type']=='language-watch' for r in rows),'regional_sources':sum(r['Record Type']=='regional-source' for r in rows)},ensure_ascii=False))

if __name__=='__main__': main()
