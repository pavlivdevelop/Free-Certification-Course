#!/usr/bin/env python3
"""Check source reachability and review age. It never infers price from HTTP text."""
import csv, datetime as dt, json, urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CATALOG=ROOT/'data/catalog-expanded.csv'
TODAY=dt.date.today(); MAX_AGE=120

def probe(url):
    req=urllib.request.Request(url,headers={'User-Agent':'Free-Certification-Course/1.0'})
    try:
        with urllib.request.urlopen(req,timeout=20) as r:
            return r.status, r.geturl(), ''
    except Exception as e:
        return None, url, str(e)

if not CATALOG.exists():
    raise SystemExit('data/catalog-expanded.csv is missing; run scripts/build_catalog.py first')
rows=list(csv.DictReader(CATALOG.open(encoding='utf-8-sig',newline='')))
items=[]
for r in rows:
    try: last=dt.date.fromisoformat(r['Last Reviewed'])
    except Exception: last=dt.date.min
    age=(TODAY-last).days
    code,final_url,error=probe(r.get('Official URL','')) if r.get('Official URL','').startswith(('http://','https://')) else (None,'','')
    items.append({**r,'review_due':age>MAX_AGE,'review_age_days':age,'http_status':code,'final_url':final_url,'http_error':error})
report={'generated':str(TODAY),'max_review_age_days':MAX_AGE,'total':len(items),'review_due':sum(i['review_due'] for i in items),'http_failures':sum(i['http_status'] is None and i['Official URL'] for i in items),'items':items}
out=ROOT/'status/freshness-report.json'; out.parent.mkdir(exist_ok=True); out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(f"checked={len(items)} review_due={report['review_due']} http_failures={report['http_failures']}")
