#!/usr/bin/env python3
"""Extract concrete learning/credential names from issuer-owned pages.

Only names observed on official pages are emitted. Records remain candidates until
free-status and credential type are supported by evidence. Taxonomy is never used
as a source of invented credential names.
"""
from __future__ import annotations
import csv, hashlib, json, re, sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
PROVIDER_FILES=[ROOT/'providers/providers.csv', ROOT/'providers/providers-additional.csv']
OUT=ROOT/'credentials/extracted-candidates.jsonl'
EVID=ROOT/'evidence/extraction-evidence.jsonl'
MAX_TOTAL=12000; TIMEOUT=20
UA='Free-Certification-Course/2026 (+https://github.com/pavlivdevelop/Free-Certification-Course)'
MARKERS=re.compile(r'\b(certificate|certification|credential|badge|microcredential|professional certificate|skill badge|digital credential|learning path|course|training|academy|exam)\b',re.I)
SKIP=re.compile(r'^(learn more|more|read more|sign in|login|register|home|menu|search|view all|contact|privacy|terms)$',re.I)

def providers():
    out=[]; seen=set()
    for p in PROVIDER_FILES:
        if not p.exists(): continue
        with p.open(encoding='utf-8-sig',newline='') as f:
            for r in csv.DictReader(f):
                org=r.get('Organization') or r.get('organization') or r.get('name')
                url=r.get('Official URL') or r.get('official_url')
                if not org or not url: continue
                k=(org.strip().lower(),url.strip())
                if k not in seen: seen.add(k); out.append((org.strip(),r.get('Country') or r.get('country') or 'International',url.strip()))
    return out

def clean(s):
    s=re.sub(r'\s+',' ',(s or '')).strip(' \t\r\n|•·-')
    if not 4<=len(s)<=180 or SKIP.match(s): return None
    return s

def fetch(url):
    try:
        r=requests.get(url,headers={'User-Agent':UA},timeout=TIMEOUT,allow_redirects=True)
        if r.ok and 'text/html' in r.headers.get('content-type','') and len(r.text)<4_000_000:
            return r.url,r.text,r.status_code
    except requests.RequestException: pass
    return url,None,None

def extract(org,country,url,html):
    soup=BeautifulSoup(html,'html.parser'); page=clean(soup.title.get_text(' ',strip=True) if soup.title else '')
    found=[]
    # Structured data: most precise source when an issuer publishes Course/Credential schema.
    for s in soup.select('script[type="application/ld+json"]'):
        try: obj=json.loads(s.string or s.get_text())
        except Exception: continue
        stack=[]
        if isinstance(obj,dict) and isinstance(obj.get('@graph'),list): stack.extend(obj['@graph'])
        elif isinstance(obj,list): stack.extend(obj)
        else: stack.append(obj)
        for x in stack:
            if not isinstance(x,dict): continue
            typ=' '.join(x.get('@type',[]) if isinstance(x.get('@type'),list) else [str(x.get('@type',''))])
            if not re.search(r'Course|Credential|Certification|LearningResource|EducationalOccupationalCredential',typ,re.I): continue
            t=clean(x.get('name') or x.get('headline'))
            if t and MARKERS.search(t+' '+typ): found.append((t,urljoin(url,x.get('url') or url),'jsonld',page,typ))
    # Headings
    for tag in soup.select('h1,h2,h3,h4,h5,h6'):
        t=clean(tag.get_text(' ',strip=True))
        if t and MARKERS.search(t): found.append((t,url,'heading',page,''))
    # Same-origin links that point to training/credential pages or use credential wording.
    host=urlparse(url).netloc
    for a in soup.select('a[href]'):
        t=clean(a.get_text(' ',strip=True)); href=urljoin(url,a.get('href',''))
        if not t or not href.startswith(('http://','https://')): continue
        if urlparse(href).netloc!=host: continue
        if MARKERS.search(t+' '+href): found.append((t,href,'anchor',page,''))
    seen=set(); out=[]
    for x in found:
        k=(x[0].lower(),x[1])
        if k not in seen: seen.add(k); out.append(x)
    return out

def main():
    prov=providers(); records=[]; evidence=[]; seen=set()
    with ThreadPoolExecutor(max_workers=16) as ex:
        fs={ex.submit(fetch,u):(o,c,u) for o,c,u in prov}
        for f in as_completed(fs):
            org,country,u=fs[f]
            try: final,html,status=f.result()
            except Exception: continue
            if not html: continue
            for title,link,method,page,typ in extract(org,country,final,html):
                rid=hashlib.sha1((org+'|'+title+'|'+link).encode()).hexdigest()[:14].upper()
                if rid in seen: continue
                seen.add(rid); observed=datetime.now(timezone.utc).date().isoformat()
                rec={'ID':'CAND-'+rid,'Record Type':'credential-candidate','Country':country,'Organization':org,'Certificate/Badge':title,'Category':'Unclassified','Subcategory':'Unclassified','Level':'Discovery','Price Status':'⚪ unknown','Conditions':'Extracted from issuer-owned page; verify current credential and price before promoting','Exam/Assessment':'Provider-specific / unknown','Duration':'Varies','Language':'Provider-dependent','Available from Russia':'Unknown','Validity':'Varies','Credly/Verification':'Provider-defined','LinkedIn':'Varies','Official URL':link,'Priority':'B','Completion Status':'Не начато','Evidence Status':'official-page-extraction','Last Reviewed':observed,'Source Page':final,'Extraction Method':method,'Page Title':page,'Schema Type':typ,'Confidence':'candidate'}
                records.append(rec); evidence.append({'record_id':rec['ID'],'official_url':link,'source_page':final,'method':method,'observed_name':title,'observed_at':observed,'provider':org})
                if len(records)>=MAX_TOTAL: break
            if len(records)>=MAX_TOTAL: break
    records.sort(key=lambda r:(r['Organization'].lower(),r['Certificate/Badge'].lower()))
    OUT.parent.mkdir(parents=True,exist_ok=True); EVID.parent.mkdir(parents=True,exist_ok=True)
    with OUT.open('w',encoding='utf-8') as f:
        for r in records: f.write(json.dumps(r,ensure_ascii=False)+'\n')
    with EVID.open('w',encoding='utf-8') as f:
        for r in evidence: f.write(json.dumps(r,ensure_ascii=False)+'\n')
    print(f'extracted_candidates={len(records)} providers={len(prov)}')
if __name__=='__main__': main()
