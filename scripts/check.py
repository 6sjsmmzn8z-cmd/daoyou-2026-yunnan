#!/usr/bin/env python3
"""Verify published links, PDFs, question data, learning records and reading controls."""
from pathlib import Path
from html.parser import HTMLParser
from collections import Counter
import json
import urllib.parse
import re

ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'docs'

class Links(HTMLParser):
 def __init__(self):
  super().__init__();self.links=[];self.anchors=[]
 def handle_starttag(self,tag,attrs):
  attributes=dict(attrs)
  for key,value in attrs:
   if key in {'href','src'} and value:self.links.append(value)
  if tag=='a':self.anchors.append(attributes)

errors=[];links=0
for path in SITE.rglob('*.html'):
 parser=Links();parser.feed(path.read_text())
 for url in parser.links:
  u=urllib.parse.urlsplit(url)
  if u.scheme or u.netloc or not u.path:continue
  target=(path.parent/urllib.parse.unquote(u.path)).resolve();links+=1
  if not target.is_relative_to(SITE.resolve()) or not target.is_file():errors.append(str(path.relative_to(SITE))+' -> '+url)
  if target.name=='viewer.html':
   query=urllib.parse.parse_qs(u.query);file=query.get('file',[''])[0]
   if not re.fullmatch(r'assets/[a-f0-9]{16}\.pdf',file) or not (SITE/file).is_file():errors.append('Missing viewer PDF: '+url)

catalogue=json.loads((SITE/'catalogue.json').read_text())
assert len(catalogue)==251
pdfs=json.loads((SITE/'pdfs.json').read_text())
for entry in pdfs:
 path=SITE/entry['file']
 with path.open('rb') as file:
  assert file.read(4)==b'%PDF',path
  file.seek(max(0,path.stat().st_size-4096));assert b'%%EOF' in file.read(),path

questions=json.loads((ROOT/'reports/原创预测训练100题.json').read_text())
assert len(questions)==100
assert len({item['id'] for item in questions})==100
assert len({item['stem'] for item in questions})==100
assert Counter(item['type'] for item in questions)=={'单选':60,'多选':40}
subjects={'政策与法律法规','导游业务','全国导游基础知识','地方导游基础知识'}
assert Counter(item['subject'] for item in questions)=={subject:25 for subject in subjects}
for subject in subjects:
 assert Counter(item['type'] for item in questions if item['subject']==subject)=={'单选':15,'多选':10}
for item in questions:
 assert item['difficulty']=='进阶' and item['knowledge_point']
 assert item['explanation'] and item['source']
 assert len(item['options'])==len(set(item['options']))
 assert len(item['answer'])==len(set(item['answer']))
 assert 4<=len(item['options'])<=6
 assert set(item['answer']).issubset(item['options'])
 assert len(item['answer'])==1 if item['type']=='单选' else 2<=len(item['answer'])<len(item['options'])
quiz=(SITE/'quiz.html').read_text()
embedded=re.search(r'<script type="application/json" id="quiz-data">(.*?)</script>',quiz,re.S)
assert embedded and json.loads(embedded.group(1))==questions,'Published quiz differs from source bank'
assert 'id="question-type"' in quiz and 'id="hide-correct"' in quiz

for name in ['index','law','business','national','local','agent','session-2026-11-15','progress']:
 assert (SITE/'study'/(name+'.html')).is_file(),name
progress=json.loads((ROOT/'study/progress.json').read_text())
assert json.loads((SITE/'study/progress.json').read_text())==progress,'Published learning record differs'
assert all(item['status'] in progress['status_definitions'] for item in progress['knowledge_points'])

continuous_pages=['articles/priorities.html','study/index.html','study/law.html','study/business.html','study/national.html','study/local.html','quiz.html','articles/yunnan.html','articles/courses.html','articles/questions.html','articles/answers.html','articles/quality.html','study/agent.html','study/session-2026-11-15.html','study/progress.html']
for route in continuous_pages:
 text=(SITE/route).read_text()
 navigation=re.search(r'<nav class="reading-nav" aria-label="连续阅读">(.*?)</nav>',text,re.S)
 assert navigation,f'Missing reading controls: {route}'
 parser=Links();parser.feed(navigation.group(0))
 assert {anchor.get('rel') for anchor in parser.anchors}=={'prev','next'},route

assert not list(SITE.rglob('*.zip')) and not list(SITE.rglob('*.rar'))
assert not errors,errors[:20]
print(f'OK: {len(catalogue)} sources, {len(pdfs)} readable PDFs, 100 advanced questions (60 single / 40 multiple), 8 study pages, {len(continuous_pages)} reading-control pages, {links} local links.')
