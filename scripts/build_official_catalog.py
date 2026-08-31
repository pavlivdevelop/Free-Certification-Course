#!/usr/bin/env python3
"""Merge curated seed data with names extracted from official issuer pages.
Never invent credential names from taxonomy combinations.
"""
from pathlib import Path
import csv,json,hashlib,re
from datetime import date

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'; CRED=ROOT/'credentials'; STATUS=ROOT/'status'
TODAY=str(date.today()); OUT=DATA/'catalog-expanded.csv'; OJSON=DATA/'catalog-expanded.json'; FREE=DATA/'free-core.csv'; COND=DATA/'conditional.csv'; CAND=CRED/'extracted-candidates.jsonl'
FIELDS=['ID','Country','Organization','Certificate/Badge','Record Type','Category','Subcategory','Level','Price Status','Conditions','Exam/Assessment','Duration','Language','Available from Russia','Validity','Credly/Verification','LinkedIn','Official URL','Priority','Completion Status','Evidence Status','Last Reviewed','Source Page','Extraction Method','Confidence']
MAP={
'AI':['artificial intelligence','generative ai','genai','llm','language model','agentforce','ai agent','machine learning','deep learning','computer vision','nlp','prompt','rag'],
'Cybersecurity':['cybersecurity','security','soc','siem','pentest','penetration','forensic','zero trust','iam','identity','appsec'],
'Cloud':['cloud','aws','azure','google cloud','oci','serverless'],
'DevOps':['devops','ci/cd','gitops','terraform','ansible','kubernetes','docker','sre','platform'],
'Networking':['network','routing','switching','ipv4','ipv6','dns','wi-fi','5g','6g','telecom','fiber','voip'],
'Python':['python'],'Data':['data','sql','database','analytics','tableau','power bi','mongodb','postgres'],
'Electronics':['electronics','pcb','eda','fpga','asic','semiconductor','analog','power electronics','spice'],
'RF':['rf','radio','sdr','antenna','microwave','millimeter','emc','emi','radar','lidar'],
'Embedded':['embedded','stm32','esp32','arduino','rtos','risc-v','arm','microcontroller','iot','physical computing'],
'Robotics':['robot','ros','plc','scada','industrial automation','mechatronics','uav','drone'],
'CAD':['cad','cam','cae','bim','fea','cfd','digital twin','cnc','3d printing','metrology','plm'],
'Mathematics':['mathematics','math','calculus','linear algebra','statistics','probability','numerical'],
'Physics':['physics','quantum','geophysics','astronomy'], 'Chemistry':['chemistry'],'Biotechnology':['biotechnology','bioinformatics'],
'GIS':['gis','geospatial','remote sensing','surveying'],'Aerospace':['aerospace','avionics','space systems','satellite'],
'Automotive':['automotive','adas','electric vehicle','ev'],'Energy':['energy','power systems','smart grid','renewable','battery'],
'Medical Devices':['medical device','biomedical','healthtech'],'Environment':['environment','climate','sustainability'],
'Project/Product':['project management','product management','agile','scrum'],'UX/Design':['ux','accessibility','design thinking'],
'Testing/QA':['testing','quality assurance','qa automation','performance testing'],'Open Source':['open source','linux','apache','eclipse'],
'Game/XR':['game development','unity','unreal',' xr ',' vr '],'Blockchain':['blockchain','web3','smart contract'],
'Technical Writing':['technical writing','documentation']}
def readp(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def norm(r):
    def g(*k,d=''):
        for x in k:
            if x in r and r[x]:return str(r[x]).strip()
        return d
    title=g('Certificate/Badge','credential_name',d='Unnamed'); org=g('Organization','organization',d='Unknown'); text=(title+' '+org+' '+g('Subcategory')+' '+g('Conditions')+' '+g('Category')).lower(); cat=g('Category')
    if not cat or cat=='Unclassified': cat=max(((sum(v in text for v in ks),k) for k,ks in MAP.items()),default=(0,'Other Technical'))[1]
    rid=g('ID') or 'ROW-'+hashlib.sha1((org+'|'+title+'|'+g('Official URL','official_url')).encode()).hexdigest()[:12].upper()
    return {'ID':rid,'Country':g('Country','country',d='International'),'Organization':org,'Certificate/Badge':title,'Record Type':g('Record Type','record_type',d='credential'),'Category':cat,'Subcategory':g('Subcategory',d=cat),'Level':g('Level',d='Discovery'),'Price Status':g('Price Status','price_status',d='⚪ unknown'),'Conditions':g('Conditions',d='Verify official page'),'Exam/Assessment':g('Exam/Assessment','Exam/assessment',d='Provider-specific'),'Duration':g('Duration',d='Varies'),'Language':g('Language',d='Provider-dependent'),'Available from Russia':g('Available from Russia',d='Unknown'),'Validity':g('Validity',d='Varies'),'Credly/Verification':g('Credly/Verification',d='Provider-defined'),'LinkedIn':g('LinkedIn',d='Varies'),'Official URL':g('Official URL','official_url'),'Priority':g('Priority',d='B'),'Completion Status':g('Completion Status',d='Не начато'),'Evidence Status':g('Evidence Status','evidence_status',d='official-page-extraction'),'Last Reviewed':g('Last Reviewed','last_reviewed',d=TODAY),'Source Page':g('Source Page','source_page'),'Extraction Method':g('Extraction Method','extraction_method',d='curated'),'Confidence':g('Confidence',d='candidate')}
def main():
    rows=[]
    # Only curated/seed CSVs are valid inputs. Generated outputs such as
    # catalog-expanded.csv must never be re-ingested on the next run.
    seed_files=[]
    for p in sorted(DATA.glob('catalog-*.csv')):
        if p.name in {'catalog-expanded.csv','catalog.csv'}:
            continue
        seed_files.append(p)
    if (DATA/'catalog.csv').exists() and (DATA/'catalog.csv').stat().st_size>20:
        seed_files.append(DATA/'catalog.csv')
    for p in seed_files: rows += [norm(x) for x in readp(p) if x.get('Certificate/Badge') or x.get('credential_name')]
    if CAND.exists():
        with CAND.open(encoding='utf-8') as f:
            for line in f:
                if line.strip():rows.append(norm(json.loads(line)))
    u={}
    for r in rows:u.setdefault((r['Organization'].lower(),r['Certificate/Badge'].lower(),r['Official URL']),r)
    rows=sorted(u.values(),key=lambda r:(r['Category'],r['Organization'].lower(),r['Certificate/Badge'].lower()))
    DATA.mkdir(exist_ok=True); STATUS.mkdir(exist_ok=True)
    for p,subset in [(OUT,rows),(FREE,[r for r in rows if r['Price Status'].startswith('✅')]),(COND,[r for r in rows if '⚠️' in r['Price Status']])]:
        with p.open('w',encoding='utf-8-sig',newline='') as f:
            w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(subset)
    OJSON.write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    (STATUS/'CATALOG-STATS.md').write_text(f'# Catalog statistics\n\n- records: {len(rows)}\n- free-core: {sum(r["Price Status"].startswith("✅") for r in rows)}\n- candidates: {sum(r["Record Type"]=="credential-candidate" for r in rows)}\n- built: {TODAY}\n',encoding='utf-8')
    print('records=',len(rows))
    return 0 if len(rows)>=5000 else 2
if __name__=='__main__':raise SystemExit(main())
