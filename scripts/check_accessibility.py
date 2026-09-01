#!/usr/bin/env python3
"""Static accessibility heuristics for OpenCertAtlas pages."""
from pathlib import Path
import re,sys
ROOT=Path(__file__).resolve().parents[1]; PAGES=[ROOT/'site'/n for n in ('index.html','progress.html','recommend.html','pathways.html')]
def fail(m): raise SystemExit('A11Y ERROR: '+m)
def main():
    for p in PAGES:
        s=p.read_text(encoding='utf-8').lower(); name=p.name
        if not re.search(r'<html[^>]+lang="[a-z]{2,3}(?:-[a-z]{2})?"',s): fail(f'{name}: missing valid html lang')
        if '<meta name="viewport"' not in s: fail(f'{name}: missing viewport meta')
        if '<title>' not in s or not re.search(r'<title>\s*[^<]+',s): fail(f'{name}: missing non-empty title')
        if '<meta name="description"' not in s and name=='index.html': fail(f'{name}: missing description')
        for tag in re.findall(r'<(?:input|select|button)\b[^>]*>',s):
            if tag.startswith('<input') and 'type="hidden"' in tag: continue
            if tag.startswith('<select') and 'aria-label=' not in tag and 'id=' not in tag: fail(f'{name}: select without id/aria-label')
        if 'onclick=' in s and 'button' not in s: fail(f'{name}: click handlers must remain attached to semantic controls')
    print('accessibility_smoke=passed'); return 0
if __name__=='__main__': sys.exit(main())
