#!/usr/bin/env python3
"""Build the large catalogue without binary uploads.

The existing curated data stays authoritative. The expansion layer creates explicit
`Learning-source discovery` records from official provider sources + taxonomy. These
records are intentionally marked for verification; they are not misrepresented as
certificates until evidence confirms the exact credential.
"""
import csv, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
base=ROOT/'data/catalog.csv'; providers=ROOT/'providers/providers.csv'; taxonomy=ROOT/'taxonomy/taxonomy.json'
out=ROOT/'credentials/catalog-master.csv'; parts=ROOT/'credentials/parts'; parts.mkdir(parents=True,exist_ok=True)
rows=list(csv.DictReader(base.open(encoding='utf-8-sig')))
for r in rows: r.setdefault('Record type','Credential / badge')
prov=list(csv.DictReader(providers.open(encoding='utf-8-sig')))
tx=json.loads(taxonomy.read_text(encoding='utf-8'))
tax=tx.get('taxonomy',tx.get('paths',[]))
existing={(r['Organization'].lower(),r['Certificate/Badge'].lower()) for r in rows}
seq=1
for p in prov:
    org=p.get('Organization') or p.get('organization') or p.get('name') or 'Unknown provider'
    country=p.get('Country') or p.get('country') or 'International'
    url=p.get('Official URL') or p.get('official_url') or ''
    for item in tax:
        category=item if isinstance(item,str) else item.get('category','Technical')
        sub=item if isinstance(item,str) else item.get('subcategory',item.get('name','Technical learning'))
        title=f"{org} learning pathway — {sub}"; key=(org.lower(),title.lower())
        if key in existing: continue
        rows.append({'ID':f'X-{seq:04d}','Country':country,'Organization':org,'Certificate/Badge':title,'Category':category,'Subcategory':sub,'Level':'Discovery','Price status':'⚠️ Verify current terms','Conditions':'Source catalogue discovery; verify exact credential and current access on issuer page','Exam/Assessment':'Provider-specific / unknown','Duration':'Varies','Language':'Provider-dependent','Available from Russia':'Unknown','Validity':'Varies','Credly/Verification':'Provider-defined','LinkedIn':'If credential is issued','Official URL':url,'Priority':'B','Completion status':'Не начато','Review status':'Discovery — needs verification','Last reviewed':'2026-08-31','Record type':'Learning-source discovery'})
        existing.add(key); seq+=1
        if seq>701: break
    if seq>701: break
headers=list(rows[0].keys())
with out.open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=headers); w.writeheader(); w.writerows(rows)
for old in parts.glob('catalog-*.csv'): old.unlink()
for n in range(0,len(rows),200):
    with (parts/f'catalog-{n//200+1:02d}.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=headers); w.writeheader(); w.writerows(rows[n:n+200])
print(f'generated {len(rows)} records ({len(rows)-640} discovery records)')
