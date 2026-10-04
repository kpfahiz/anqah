"""Quick SEO / link audit for every page: run  python tools/audit_seo.py"""
import glob
import json
import os
import re
from urllib.parse import unquote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
pages = ['index.html', 'ar/index.html', '404.html'] + sorted(glob.glob('products/*.html')) + sorted(glob.glob('ar/products/*.html'))
alts = {}
for f in pages:
    f = f.replace(os.sep, '/')
    s = open(f, encoding='utf-8').read()
    base = os.path.dirname(f)
    issues = []
    h1 = len(re.findall(r'<h1[\s>]', s))
    if h1 != 1:
        issues.append(f'{h1} h1')
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            json.loads(m.group(1))
        except ValueError:
            issues.append('bad JSON-LD')
    for m in re.finditer(r'<img\b[^>]*>', s):
        if 'alt="' not in m.group(0):
            issues.append('img without alt')
    for m in re.finditer(r'(?:href|src)="([^"#][^"]*)"', s):
        u = m.group(1)
        if u.startswith(('http', 'mailto:', 'tel:', 'data:')):
            continue
        path = u.split('#')[0].split('?')[0]
        if not path:
            continue
        full = os.path.normpath(path.lstrip('/') if path.startswith('/') else os.path.join(base, unquote(path)))
        if os.path.isdir(full):
            full = os.path.join(full, 'index.html')
        if not os.path.exists(full):
            issues.append('broken: ' + u)
    if f.startswith('ar/') and 'dir="rtl"' not in s[:300]:
        issues.append('not rtl')
    if f != '404.html':
        canon = re.search(r'rel="canonical" href="([^"]+)"', s).group(1)
        alts[canon] = dict(re.findall(r'hreflang="([^"]+)" href="([^"]+)"', s))
    print(f'{f:34} h1={h1} ' + ('OK' if not issues else '; '.join(sorted(set(issues)))))

# every alternate a page lists must list that page back
bad = [(u, h, v) for u, a in alts.items() for h, v in a.items() if v in alts and u not in alts[v].values()]
missing = [v for a in alts.values() for v in a.values() if v not in alts]
print(f'hreflang: {len(alts)} pages | non-reciprocal: {bad or "none"} | targets without a page: {sorted(set(missing)) or "none"}')
