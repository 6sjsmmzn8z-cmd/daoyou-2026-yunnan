#!/usr/bin/env python3
"""Check local HTML links, published PDFs and source catalogue coverage."""
from pathlib import Path
from html.parser import HTMLParser
import json,urllib.parse,re
ROOT=Path(__file__).resolve().parents[1];SITE=ROOT/'docs'
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,tag,attrs):
  for key,value in attrs:
   if key in {'href','src'} and value:self.links.append(value)
errors=[];links=0
for path in SITE.rglob('*.html'):
 parser=Links();parser.feed(path.read_text())
 for url in parser.links:
  u=urllib.parse.urlsplit(url)
  if u.scheme or u.netloc or not u.path:continue
  target=(path.parent/urllib.parse.unquote(u.path)).resolve();links+=1
  if not target.is_relative_to(SITE.resolve()) or not target.is_file():errors.append(str(path.relative_to(SITE))+' -> '+url)
  if target.name=='viewer.html':
   q=urllib.parse.parse_qs(u.query);f=q.get('file',[''])[0]
   if not re.fullmatch(r'assets/[a-f0-9]{16}\.pdf',f) or not (SITE/f).is_file():errors.append('Missing viewer PDF: '+url)
cat=json.loads((SITE/'catalogue.json').read_text());assert len(cat)==251
pdfs=json.loads((SITE/'pdfs.json').read_text())
for entry in pdfs:
 p=SITE/entry['file']
 with p.open('rb') as f:
  assert f.read(4)==b'%PDF',p
  f.seek(max(0,p.stat().st_size-4096));assert b'%%EOF' in f.read(),p
q=json.loads((ROOT/'reports/原创预测训练100题.json').read_text());assert len(q)==100
assert len({x['stem'] for x in q})==100
assert all(x['answer'] and all(a in x['options'] for a in x['answer']) for x in q)
assert not list(SITE.rglob('*.zip')) and not list(SITE.rglob('*.rar'))
assert not errors,errors[:20]
print(f'OK: {len(cat)} catalogue entries, {len(pdfs)} readable PDFs, 100 questions, {links} local links; no compressed downloads in site.')
