#!/usr/bin/env python3
"""Source-first extraction of concrete course/certificate/badge names from issuer sites.

Only names observed on issuer-owned HTML are emitted. No taxonomy combinations are
converted into fake credentials. Every row keeps provenance and remains a candidate
until evidence verifies credential type and current free status.
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
MAX_TOTAL=12000; MAX_PAGES_PROVIDER=35; TIMEOUT=18
UA='Free-Certification-Course/2026 (+https://github.com/pavlivdevelop/Free-Certification-Course)'
MARKERS=re.compile(r'\b(certificate|certification|credential|badge|microcredential|professional certificate|skill badge|digital credential|learning path|course|training|academy|exam)\b',re.I)
PATH_HINTS=re.compile(r'/(course|courses|learn|learning|training|academy|education|certif|credential|badge|exam|skills?|certification)(/|$|[?#])',re.I)
SKIP=re.compile(r'^(learn more|more|read more|sign in|login|register|home|menu|search|view all|contact|privacy|terms|cookies)$',re.I)
S=requests.Session(); S.headers.update({'User-Agent':UA})

def providers():
    out=[]; seen=set()
    for path in PROVIDER_FILES:
        if not path.exists(): continue
        with path.open(encoding='utf-8-sig',newline='') as f:
            for r in csv.DictReader(f):
                org=r.get('Organization') or r.get('organization') or r.get('name')
                url=r.get('Official URL') or r.get('official_url')
                if not org or not url: continue
                k=(org.strip().lower(),url.strip())
                if k not in seen:
                    seen.add(k); out.append((org.strip(),r.get('Country') or r.get('country') or 'International',url.strip()))
    return out

def clean(s):
    s=re.sub(r'\s+',' ',(s or '')).strip(' \t\r\n|•·-')
    if not 4<=len(s)<=180 or SKIP.match(s): return None
    return s

def fetch(url):
    try:
        r=S.get(url,timeout=TIMEOUT,allow_redirects=True)
        if r.ok and 'text/html' in r.headers.get('content-type','') and len(r.text)<5_000_000:
            return r.url,r.text
    except requests.RequestException: pass
    return None,None

def discover(root_url,html,limit):
    soup=BeautifulSoup(html,'html.parser'); host=urlparse(root_url).netloc; out=[]; seen=set()
    def add(u):
        u=u.split('#')[0]
        if not u.startswith(('http://','https://')) or urlparse(u).netloc!=host or u in seen: return
        if any(x in u.lower() for x in ('/privacy','/terms','/login','/signin','/search','/cart','/account')): return
        if PATH_HINTS.search(u): seen.add(u); out.append(u)
    for a in soup.select('a[href]'): add(urljoin(root_url,a.get('href','')))
    for loc in soup.select('loc'): add(loc.get_text(' ',strip=True))
    return out[:limit]

def extract_page(url,html):
    soup=BeautifulSoup(html,'html.parser'); page=clean(soup.title.get_text(' ',strip=True) if soup.title else ''); found=[]
    for sc in soup.select('script[type="application/ld+json"]'):
        try: obj=json.loads(sc.string or sc.get_text())
        except Exception: continue
        stack=[]
        if isinstance(obj,dict) and isinstance(obj.get('@graph'),list): stack.extend(obj['@graph'])
        elif isinstance(obj,list): stack.extend(obj)
        else: stack.append(obj)
        for x in stack:
            if not isinstance(x,dict): continue
            typ=' '.join(x.get('@type',[]) if isinstance(x.get('@type'),list) else [str(x.get('@type',''))])
            if re.search(r'Course|Credential|Certification|LearningResource|EducationalOccupationalCredential',typ,re.I):
                t=clean(x.get('name') or x.get('headline'))
                if t: found.append((t,urljoin(url,x.get('url') or url),'jsonld',page,typ))
    for tag in soup.select('h1,h2,h3,h4,h5,h6'):
        t=clean(tag.get_text(' ',strip=True))
        if t and MARKERS.search(t): found.append((t,url,'heading',page,''))
    host=urlparse(url).netloc
    for a in soup.select('a[href]'):
        t=clean(a.get_text(' ',strip=True)); href=urljoin(url,a.get('href',''))
        if not t or urlparse(href).netloc!=host: continue
        if MARKERS.search(t+' '+href): found.append((t,href,'anchor',page,''))
    out=[]; seen=set()
    for x in found:
        k=(x[0].lower(),x[1])
        if k not in seen: seen.add(k); out.append(x)
    return out

def crawl(org,country,seed):
    first,html=fetch(seed)
    if not html: return []
    queue=[first]; seen={first}
    for u in discover(first,html,MAX_PAGES_PROVIDER*3):
        if u not in seen: queue.append(u)
    sm=join_sitemap= f"{urlparse(first).scheme}://{urlparse(first).netloc}/sitemap.xml"
    _,smhtml=fetch(sm)
    if smhtml:
        for u in discover(sm,smhtml,MAX_PAGES_PROVIDER*2):
            if u not in seen: queue.append(u)
    results=[]
    for u in queue[:MAX_PAGES_PROVIDER]:
        if u==first: body=html; final=first
        else: final,body=fetch(u)
        if not body: continue
        try: results.extend(extract_page(final,body))
        except Exception: pass
    return results

def main():
    prov=providers(); records=[]; evidence=[]; seen=set(); today=datetime.now(timezone.utc).date().isoformat()
    with ThreadPoolExecutor(max_workers=10) as ex:
        fs={ex.submit(crawl,o,c,u):(o,c,u) for o,c,u in prov}
        for f in as_completed(fs):
            org,country,seed=fs[f]
            try: items=f.result()
            except Exception: continue
            for title,link,method,page,typ in items:
                rid=hashlib.sha1((org+'|'+title+'|'+link).encode()).hexdigest()[:14].upper()
                if rid in seen: continue
                seen.add(rid)
                records.append({'ID':'CAND-'+rid,'Record Type':'credential-candidate','Country':country,'Organization':org,'Certificate/Badge':title,'Category':'Unclassified','Subcategory':'Unclassified','Level':'Discovery','Price Status':'⚪ unknown','Conditions':'Observed on issuer-owned page; verify exact credential type and current price before promotion','Exam/Assessment':'Provider-specific / unknown','Duration':'Varies','Language':'Provider-dependent','Available from Russia':'Unknown','Validity':'Varies','Credly/Verification':'Provider-defined','LinkedIn':'Varies','Official URL':link,'Priority':'B','Completion Status':'Не начато','Evidence Status':'official-page-extraction','Last Reviewed':today,'Source Page':page,'Extraction Method':method,'Schema Type':typ,'Confidence':'candidate'})
                evidence.append({'record_id':'CAND-'+rid,'provider':org,'official_url':link,'source_page':seed,'method':method,'observed_name':title,'observed_at':today})
                if len(records)>=MAX_TOTAL: break
            if len(records)>=MAX_TOTAL: break
    records.sort(key=lambda r:(r['Organization'].lower(),r['Certificate/Badge'].lower()))
    OUT.parent.mkdir(parents=True,exist_ok=True); EVID.parent.mkdir(parents=True,exist_ok=True)
    with OUT.open('w',encoding='utf-8') as f:
        for r in records: f.write(json.dumps(r,ensure_ascii=False)+'\n')
    with EVID.open('w',encoding='utf-8') as f:
        for r in evidence: f.write(json.dumps(r,ensure_ascii=False)+'\n')
    print(f'extracted_candidates={len(records)} providers={len(prov)}')
    return 0 if len(records)>=5000 else 2
if __name__=='__main__': raise SystemExit(main())
