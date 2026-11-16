#!/usr/bin/env python3
"""Build a Chinese, browser-readable study library for GitHub Pages."""
from pathlib import Path
from html.parser import HTMLParser
import json,html,re,hashlib,shutil,subprocess,urllib.parse,os,sys
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs';OUT.mkdir(exist_ok=True)
for d in ['assets','articles','archives','sources','study']: (OUT/d).mkdir(exist_ok=True)
practice_builder=ROOT/'scripts/build_practice.py'
if practice_builder.is_file():subprocess.run([sys.executable,str(practice_builder)],check=True)
previous_pdfs=json.loads((OUT/'pdfs.json').read_text()) if (OUT/'pdfs.json').exists() else []
learning=json.loads((ROOT/'study/progress.json').read_text())
H=html.escape

def link(path): return urllib.parse.quote(str(path),safe='/')

READING_PATH=[('articles/priorities.html','考试与复习重点'),('study/index.html','四科分类记忆'),('study/law.html','政策与法律法规'),('study/business.html','导游业务'),('study/national.html','全国导游基础知识'),('study/local.html','地方导游基础知识'),('quiz.html','100道进阶训练'),('articles/yunnan.html','云南中文面试'),('articles/courses.html','课程与教材指南')]
EXTRA_READING={
 'articles/questions.html':(('quiz.html','进阶训练'),('articles/answers.html','答案与逐题解析')),
 'articles/answers.html':(('articles/questions.html','完整题目'),('quiz.html','返回在线作答')),
 'articles/quality.html':(('quiz.html','进阶训练'),('study/index.html','四科分类记忆')),
 'study/agent.html':(('study/index.html','四科分类记忆'),('study/session-2026-11-15.html','当日答题记录')),
 'study/session-2026-11-15.html':(('study/agent.html','Agent先读'),('study/progress.html','结构化进度')),
 'study/progress.html':(('study/session-2026-11-15.html','当日答题记录'),('study/index.html','返回四科分类记忆')),
}
def reading_nav(route):
 if not route:return ''
 routes=[r for r,_ in READING_PATH]
 if route in routes:
  index=routes.index(route)
  previous=READING_PATH[index-1] if index else ('index.html','阅读首页')
  following=READING_PATH[index+1] if index+1<len(READING_PATH) else ('study/index.html','返回四科分类记忆')
 elif route in EXTRA_READING:previous,following=EXTRA_READING[route]
 else:return ''
 items=[]
 for label,relation,target in [('上一篇','prev',previous),('下一篇','next',following)]:
  href=urllib.parse.quote(os.path.relpath(OUT/target[0],(OUT/route).parent),safe='/')
  items.append('<a rel="'+relation+'" href="'+href+'"><small>'+label+'</small><strong>'+html.escape(target[1])+' '+('→' if relation=='next' else '←')+'</strong></a>')
 return '<nav class="reading-nav" aria-label="连续阅读">'+''.join(items)+'</nav>'

def page(title,content,depth=0,active='',route=''):
 content+=reading_nav(route)
 pre='../'*depth
 nav=''.join(f'<a href="{pre}{href}"'+(' aria-current="page"' if label==active else '')+f'>{label}</a>' for label,href in [('阅读首页','index.html'),('四科记忆','study/index.html'),('进阶训练','quiz.html'),('学习记录','study/agent.html'),('云南面试','articles/yunnan.html'),('全部资料','index.html#library')])
 return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><meta name="description" content="2026全国导游资格考试资料库：云南昆明中文类，官方大纲、复习重点、历年回忆题、100道原创进阶练习、四科分类记忆和12景点面试提纲。"><title>{H(title)} · 2026导考资料库</title><link rel="stylesheet" href="{pre}style.css"></head><body><a class="skip" href="#main">跳到正文</a><header class="site-header"><div class="header-inner"><a class="brand" href="{pre}index.html"><span class="brand-mark" aria-hidden="true">导</span><span>2026 导考资料库<small>云南昆明 · 中文类</small></span></a><nav aria-label="主导航">{nav}</nav></div></header><main id="main">{content}</main><footer><p>资料收集截点：2026年11月14日 · 分类记忆、进阶题与阅读导航更新：2026年11月16日</p><p>预测为复习优先级，不保证命中。回忆题与旧版资料请对照2026官方大纲。<a href="{pre}about.html">来源与使用说明</a></p></footer></body></html>'''

css='''*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:100px}body{margin:0;color:#203632;background:#f7f7f1;font:16px/1.75 -apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif}a{color:#15665b;text-underline-offset:4px}button,input,select{font:inherit}a,button,input,select{touch-action:manipulation}button,a,input,select{outline-offset:4px}button:focus-visible,a:focus-visible,input:focus-visible,select:focus-visible{outline:3px solid #b26428}.skip{position:absolute;top:-100px}.skip:focus{top:6px;z-index:20;background:white;padding:8px}.site-header{background:#fffef9;border-bottom:1px solid #d9e0d7;position:sticky;top:0;z-index:10}.header-inner{max-width:1200px;margin:auto;padding:15px 28px;display:flex;align-items:center;justify-content:space-between;gap:24px}.brand{display:flex;gap:12px;align-items:center;font-weight:750;color:#203b32;text-decoration:none;white-space:nowrap}.brand small{display:block;font-size:12px;font-weight:400;color:#68796e;line-height:1.5}.brand-mark{display:grid;place-items:center;background:#205d4d;color:#fff;width:43px;height:43px;font-size:23px;border-radius:11px}nav{display:flex;gap:24px}nav a{text-decoration:none;font-size:14px;color:#53685c;padding:4px 0}nav a[aria-current]{color:#154c3c;border-bottom:2px solid #154c3c}main{max-width:1200px;margin:0 auto;padding:0 28px 64px}.hero{padding:62px 0 34px;display:grid;grid-template-columns:1.6fr 1fr;gap:50px;align-items:center}.eyebrow{color:#386a58;font-size:13px;letter-spacing:.12em;font-weight:650;margin:0 0 12px}h1,h2,h3{line-height:1.4;color:#1b3f33}h1{font-size:clamp(30px,4vw,48px);font-weight:760;letter-spacing:-.025em;margin:0 0 18px}h2{font-size:26px;margin:0 0 12px}h3{font-size:18px;margin:0 0 10px}.lead{max-width:640px;font-size:17px;color:#617365;margin:0 0 24px}.actions{display:flex;gap:10px;flex-wrap:wrap;align-items:center}.button,button.primary{display:inline-block;background:#205d4d;color:white;border:1px solid #205d4d;border-radius:7px;padding:10px 17px;font-weight:600;text-decoration:none;cursor:pointer}.button.secondary{background:transparent;color:#205d4d;border-color:#bccdc0}.note-card{border:1px solid #d0dbcd;border-radius:14px;padding:25px;background:#eef2e7}.note-card .date{font-size:28px;font-weight:750;color:#244f3e}.note-card p{margin:7px 0;color:#536a59}.note-card small{display:block;line-height:1.8;color:#5d7262}.metrics{display:flex;gap:28px;border-top:1px solid #d6ded3;padding-top:22px;margin:14px 0 34px;flex-wrap:wrap}.metrics strong{display:block;font-size:28px;color:#214d3d}.metrics span{font-size:13px;color:#69806c}.section{margin:30px 0 48px}.section-heading{display:flex;align-items:end;justify-content:space-between;gap:16px;margin-bottom:20px}.section-heading p{margin:0;color:#68796d;font-size:14px}.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.step{background:#fffefb;border:1px solid #dbe3d6;border-radius:12px;padding:24px;display:flex;flex-direction:column}.step .number{font-size:12px;font-weight:700;color:#8f6536;letter-spacing:.1em;margin-bottom:16px}.step p{font-size:14px;color:#67776a;flex:1;margin:0 0 18px}.step a{font-size:14px;font-weight:650}.hint{border-left:3px solid #a87c3d;background:#f2eee2;padding:14px 18px;color:#665b45;font-size:14px;border-radius:0 7px 7px 0}.search-panel{background:#edf1e7;border:1px solid #d6dfd0;border-radius:12px;padding:20px;margin-bottom:22px}.search-row{display:grid;grid-template-columns:1.8fr 1fr 1fr;gap:14px}.field label{display:block;font-size:13px;color:#4a6551;margin-bottom:5px}.field input,.field select{width:100%;padding:11px 12px;background:white;border:1px solid #c8d4c2;border-radius:6px;color:#2f4738;min-height:46px}.result-info{font-size:13px;color:#526951;margin:13px 0 0}.resource-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}.resource{min-width:0;display:flex;flex-direction:column;gap:11px;background:#fffefb;border:1px solid #dde4d8;border-radius:11px;padding:21px}.resource[hidden]{display:none}.resource h3{font-size:16px;overflow-wrap:anywhere;margin:0;flex:1}.resource .meta{font-size:12px;color:#63765f}.resource .resource-actions{display:flex;gap:14px;flex-wrap:wrap;font-size:13px}.resource .state{font-size:12px;color:#8b6435}.tag{display:inline-block;font-size:11px;border-radius:4px;background:#edf2e7;color:#57704c;padding:2px 7px;width:fit-content}.empty{padding:36px;text-align:center;color:#697a65}.article{max-width:850px;margin:0 auto;padding-top:36px}.article .crumb,.crumb{font-size:13px;margin:0 0 23px;color:#74816d}.article h1{font-size:32px}.article h2{font-size:24px;margin-top:36px}.article h3{margin-top:24px}.article p,.article li{overflow-wrap:anywhere}.article table{width:100%;border-collapse:collapse;font-size:14px;background:#fffefb;display:block;overflow-x:auto}.article td,.article th{border:1px solid #d6dfd0;padding:10px;min-width:90px;text-align:left;vertical-align:top}.article th{background:#eaf0e2}.article code{background:#e8eee0;border-radius:4px;padding:2px 5px}.article pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#eef1e7;padding:16px;border-radius:8px;font-size:13px}.article blockquote{margin:20px 0;padding:8px 20px;border-left:3px solid #9cb28e}.article ul,.article ol{padding-left:24px}.article details{border:1px solid #d6dfd0;padding:14px;border-radius:8px;background:#fffefb}.article summary{cursor:pointer}.child-file{border-bottom:1px solid #dce3d7;padding:15px 0}.child-file:last-child{border:0}.child-file a{display:block;font-weight:600}.viewer{padding-top:30px}.viewer h1{font-size:26px;overflow-wrap:anywhere}.pdf-frame{width:100%;height:75vh;border:1px solid #cfdbca;border-radius:8px;background:white;margin-top:20px}.quiz-header{padding-top:35px}.quiz-header h1{font-size:34px}.quiz-tools{display:flex;justify-content:space-between;gap:18px;align-items:end;margin:24px 0;flex-wrap:wrap}.quiz-tools select{padding:9px 12px;border:1px solid #becdb6;border-radius:6px;background:white;max-width:100%}.quiz-progress{font-size:14px;color:#4d6854}.question{padding:24px;background:#fffefb;border:1px solid #d9e2d2;border-radius:10px;margin-bottom:16px}.question legend{font-weight:650;line-height:1.8;padding:0}.question fieldset{border:0;padding:0;margin:0;min-width:0}.question .qmeta{font-size:12px;color:#708065;margin-bottom:10px}.option{display:flex;align-items:flex-start;gap:10px;border:1px solid #e0e6da;border-radius:6px;padding:11px 12px;margin:9px 0;cursor:pointer}.option:has(input:checked){background:#eaf2e2;border-color:#91af80}.option input{margin-top:7px;flex:0 0 auto;accent-color:#205d4d}.question button{padding:8px 14px;background:#205d4d;border:0;border-radius:6px;color:white;cursor:pointer;margin-top:8px}.question button:disabled{background:#a8b3a1;cursor:not-allowed}.feedback{margin-top:14px;background:#eef3e8;border-left:3px solid #658d51;padding:12px 15px;font-size:14px}.feedback.wrong{background:#f7eee5;border-color:#a97442}.feedback[hidden]{display:none}footer{border-top:1px solid #d9e0d2;max-width:1144px;margin:0 auto;padding:28px 0;color:#788570;font-size:12px}footer p{margin:5px 0}body:has(.viewer) main{max-width:1350px}@media(max-width:850px){.hero{gap:25px;grid-template-columns:1fr;padding-top:34px}.note-card{padding:20px}.note-card .date{font-size:24px}.resource-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.steps{grid-template-columns:1fr}.step{padding:20px}.step .number{margin-bottom:10px}.header-inner{gap:12px;padding:12px 20px;flex-wrap:wrap}nav{gap:20px;width:100%;justify-content:space-between}main{padding:0 20px 40px}.search-row{grid-template-columns:1fr 1fr}.search-row .field:first-child{grid-column:1/-1}.section-heading{align-items:start;flex-direction:column}.metrics{gap:25px}.article h1{font-size:27px}.article h2{font-size:22px}footer{margin:0 20px}.article{padding-top:25px}}@media(max-width:530px){.resource-grid{grid-template-columns:1fr}.search-row{grid-template-columns:1fr}.search-row .field:first-child{grid-column:auto}.metrics{gap:24px}.metrics strong{font-size:25px}.hero h1{font-size:33px}.hero{padding-top:30px}.lead{font-size:16px}.question{padding:18px}.quiz-header h1{font-size:29px}nav a{font-size:13px}.pdf-frame{height:65vh}}'''
css+='''nav{flex-wrap:wrap;column-gap:18px;row-gap:4px}.learning-summary{display:flex;flex-wrap:wrap;gap:12px;margin:20px 0}.learning-summary p{margin:0;background:#eef2e7;border:1px solid #d0dbcd;border-radius:8px;padding:12px 16px}.learning-summary strong{font-size:23px;color:#205d4d}.quiz-filters{display:flex;flex-wrap:wrap;gap:14px;align-items:end}.quiz-check{display:flex;align-items:center;gap:8px;font-size:14px;padding:10px 0}.quiz-check input{accent-color:#205d4d;width:18px;height:18px}.quiz-summary{font-size:14px;color:#526951}.feedback p{margin:8px 0;overflow-wrap:anywhere}.option span{min-width:0;overflow-wrap:anywhere}.question legend{overflow-wrap:anywhere}.feedback .selection-error{font-weight:600;color:#875724}.article .study-nav{font-size:14px;display:flex;flex-wrap:wrap;gap:10px;margin-bottom:20px}.article .study-nav a{border:1px solid #cbd7c3;border-radius:6px;padding:5px 10px;text-decoration:none}.reference-text{white-space:pre-wrap;font-size:13px}.reading-nav{display:grid;grid-template-columns:1fr 1fr;gap:16px;max-width:850px;margin:45px auto 0;border-top:1px solid #cedbc7;padding-top:22px}.reading-nav a{display:flex;flex-direction:column;gap:5px;padding:16px 18px;background:#eef2e7;border:1px solid #cbd7c3;border-radius:9px;text-decoration:none;min-height:86px}.reading-nav a[rel=next]{text-align:right}.reading-nav small{font-size:12px;color:#617563}.reading-nav strong{font-size:16px;overflow-wrap:anywhere}.question[hidden]{display:none}@media(max-width:850px){html{scroll-padding-top:145px}}@media(max-width:530px){nav{justify-content:flex-start;gap:5px 14px}.quiz-tools{align-items:stretch}.quiz-filters{width:100%}.quiz-filters .field{flex:1;min-width:130px}.quiz-tools select{width:100%}.learning-summary p{flex:1;min-width:120px}.reading-nav{gap:10px}.reading-nav a{padding:13px 11px}.reading-nav strong{font-size:14px}}'''
(OUT/'style.css').write_text(css)
(OUT/'.nojekyll').write_text('')
(OUT/'robots.txt').write_text('User-agent: *\nAllow: /\n')
rows=json.loads((ROOT/'manifest.json').read_text());groups={g['id']:g for g in json.loads((ROOT/'expanded_materials.json').read_text())}
assets={};PDFS=[]
def pdf_asset(p,title):
 digest=hashlib.sha256(p.read_bytes()).hexdigest();name=assets.get(digest)
 if name is None:
  name='assets/'+digest[:16]+'.pdf';shutil.copyfile(p,OUT/name);assets[digest]=name;PDFS.append({'file':name,'title':title})
 return name

def viewer_url(file,title,pre=''):return pre+'viewer.html?'+urllib.parse.urlencode({'file':file,'title':title})
# Publish Markdown as real site pages and keep repository-relative links inside docs.
reports=[('01_研究结论与考点预测.md','priorities.html','考试与复习重点'),('02_云南中文面试重点与12景点提纲.md','yunnan.html','云南中文面试'),('03_原创预测训练100题_试题.md','questions.html','进阶训练题目'),('04_原创预测训练100题_答案解析.md','answers.html','答案与逐题解析'),('05_课程课件与教材使用指南.md','courses.html','课程与教材指南')]
if (ROOT/'reports/06_训练题质量修订说明.md').is_file():reports.append(('06_训练题质量修订说明.md','quality.html','题库质量修订说明'))
study_pages={
 ROOT/'study/README.md':('index.html','四科分类记忆'),
 ROOT/'study/01-政策与法律法规重点.md':('law.html','政策与法律法规分类记忆'),
 ROOT/'study/02-导游业务重点.md':('business.html','导游业务分类记忆'),
 ROOT/'study/03-全国导游基础知识分类记忆表.md':('national.html','全国导基分类记忆'),
 ROOT/'study/04-地方导游基础知识分类记忆表.md':('local.html','地方导基分类记忆'),
 ROOT/'study/2026-11-15_答题记录.md':('session-2026-11-15.html','2026-11-15答题记录'),
 ROOT/'AGENT必读_学习记忆与续练规则.md':('agent.html','AI／Agent先读：学习记忆与跳过清单'),
}
study_routes={source.resolve():OUT/'study'/dest for source,(dest,_) in study_pages.items()}
study_routes[(ROOT/'study/progress.json').resolve()]=OUT/'study/progress.html'
report_routes={(ROOT/'reports'/source).resolve():OUT/'articles'/dest for source,dest,_ in reports}
reference_pages={}
def relative_site_path(target,current):return link(os.path.relpath(target,current.parent))
def publish_reference(source):
 source=source.resolve()
 if source not in reference_pages:
  dest=OUT/'study'/('reference-'+hashlib.sha256(str(source.relative_to(ROOT)).encode()).hexdigest()[:12]+'.html')
  reference_pages[source]=dest
  body='<article class="article"><p class="crumb"><a href="index.html">四科分类记忆</a> / 核对原文</p><h1>'+H(source.name)+'</h1><p class="hint">这是仓库保存的原文或检索文本。OCR可能有错字，背诵与引用需对照官方原件。</p><pre class="reference-text">'+H('\n'.join(line.rstrip() for line in source.read_text(errors='replace').splitlines()))+'</pre></article>'
  dest.write_text(page(source.name,body,1,active='四科记忆'))
 return reference_pages[source]
def rewrite_links(body,source,current):
 def replace(match):
  href=html.unescape(match.group(1));u=urllib.parse.urlsplit(href)
  if u.scheme or u.netloc or not u.path:return match.group(0)
  target=(source.parent/urllib.parse.unquote(u.path)).resolve()
  if target in study_routes:dest=relative_site_path(study_routes[target],current)
  elif target in report_routes:dest=relative_site_path(report_routes[target],current)
  elif target.suffix.lower()=='.pdf' and target.is_file():dest=viewer_url(pdf_asset(target,target.stem),target.stem,'../')
  elif target.suffix.lower() in {'.txt','.json','.md'} and target.is_file():dest=relative_site_path(publish_reference(target),current)
  else:raise ValueError(f'Unmapped local link in {source.name}: {href}')
  if u.fragment:dest+='#'+u.fragment
  return 'href="'+H(dest,quote=True)+'"'
 return re.sub(r'href="([^"]+)"',replace,body)
def markdown_body(source,current):
 body=subprocess.check_output(['pandoc','--from=gfm','--to=html5','--wrap=none',str(source)],text=True)
 return rewrite_links(body,source,current)
for source,dest,title in reports:
 current=OUT/'articles'/dest
 body=markdown_body(ROOT/'reports'/source,current)
 content='<article class="article"><p class="crumb"><a href="../index.html">阅读首页</a> / '+title+'</p>'+body+'</article>'
 current.write_text(page(title,content,1,active='云南面试' if dest=='yunnan.html' else '',route='articles/'+dest))
study_nav='<div class="study-nav"><a href="index.html">四科入口</a><a href="law.html">法规</a><a href="business.html">业务</a><a href="national.html">全国导基</a><a href="local.html">地方导基</a><a href="agent.html">Agent先读</a><a href="session-2026-11-15.html">答题记录</a></div>'
counts={status:sum(point['status']==status for point in learning['knowledge_points']) for status in learning['status_definitions']}
for source,(dest,title) in study_pages.items():
 current=OUT/'study'/dest
 summary=''
 if dest in {'index.html','agent.html'}:
  summary='<div class="learning-summary"><p><strong>'+str(counts['passed_skip'])+'</strong> 项具体答题已通过</p><p><strong>'+str(counts['weak_retest'])+'</strong> 项已讲解、待复测</p></div><p class="hint">这是当前学习者的个体记录，不是全科掌握评估。排除一个错项不等于能够主动说出正确归类；未练内容保持“尚未验证”。</p>'
 content='<article class="article"><p class="crumb"><a href="../index.html">阅读首页</a> / '+H(title)+'</p>'+study_nav+summary+markdown_body(source,current)+'</article>'
 current.write_text(page(title,content,1,active='学习记录' if dest in {'agent.html','session-2026-11-15.html'} else '四科记忆',route='study/'+dest))
(OUT/'study/progress.json').write_text(json.dumps(learning,ensure_ascii=False,indent=2)+'\n')
progress_body='<article class="article"><p class="crumb"><a href="agent.html">Agent先读</a> / 结构化进度</p><h1>结构化学习进度</h1><p>其他 Agent 可读取此记录，区分已通过、待复测与尚未验证。<a href="progress.json">打开 JSON 原文</a></p><pre class="reference-text">'+H(json.dumps(learning,ensure_ascii=False,indent=2))+'</pre></article>'
(OUT/'study/progress.html').write_text(page('结构化学习进度',progress_body,1,active='学习记录',route='study/progress.html'))
book=pdf_asset(ROOT/'study.pdf','分类记忆与进阶训练复习册')
# Format conversion groups: expanded reference bundles or readable Office-file exports.
for sid,g in groups.items():
 items=[]
 for f in g['files']:
  asset=pdf_asset(ROOT/f['path'],f['title']);items.append({'title':f['title'],'file':asset})
 title=g['title']
 if sid=='S005':title='苏州考区2026现场考试事项（外省参考）'
 if sid=='S249':title='《导游业务》出版社公开样章'
 body='<article class="article"><p class="crumb"><a href="../index.html#library">全部资料</a> / 文件内容</p><h1>'+H(title)+'</h1>'
 if items:
  body+='<p>以下资料已展开或转换成可在线阅读的 PDF。转换后的排版可能与原件略有差异，涉及条款请核对原始来源。</p>'
  for f in items:body+='<div class="child-file"><a href="'+H(viewer_url(f['file'],f['title'],'../'),quote=True)+'">'+H(f['title'])+'</a><small>PDF · 浏览器直接阅读</small></div>'
 else:body+='<div class="hint">出版社提供的内层课件包受密码保护，当前没有取得可直接阅读的课件正文。请按出版社原站的资源获取流程办理，本库未尝试解密。</div>'
 body+='<p><a href="'+H(g['url'],quote=True)+'" target="_blank" rel="noopener noreferrer">查看发布方原始页面</a></p></article>'
 (OUT/'archives'/(sid+'.html')).write_text(page(title,body,1))

class TextOnly(HTMLParser):
 def __init__(self):super().__init__();self.skip=0;self.parts=[]
 def handle_starttag(self,t,a):
  if t in ['script','style','noscript','svg']:self.skip+=1
  elif not self.skip and t in ['p','div','br','li','h1','h2','h3','tr']:self.parts.append('\n')
 def handle_endtag(self,t):
  if t in ['script','style','noscript','svg'] and self.skip:self.skip-=1
 def handle_data(self,d):
  if not self.skip:self.parts.append(d)

catalogue=[]
for row in rows:
 title=row.get('title') or row['url'];status=row['status'];dest=None;state='网页资料';kind='网页'
 p=ROOT/row.get('path','')
 if row['id'] in groups:
  dest='archives/'+row['id']+'.html';kind='展开资料';state='可在线阅读' if groups[row['id']]['files'] else '获取受限';action='查看资料内容' if groups[row['id']]['files'] else '查看获取说明'
  title=groups[row['id']]['title']
  if row['id']=='S005':title='苏州考区2026现场考试事项（外省参考）'
 elif status=='downloaded' and p.suffix.lower()=='.pdf':
  asset=pdf_asset(p,title);dest=viewer_url(asset,title);state='PDF 原件';kind='PDF';action='在线阅读'
 elif status=='downloaded' and p.suffix.lower()=='.html':
  parser=TextOnly();parser.feed(p.read_text(errors='replace'));text=''.join(parser.parts);text=re.sub(r'\n\s*\n+','\n\n',text).strip();text='\n'.join(line.rstrip() for line in text.splitlines())
  body='<article class="article"><p class="crumb"><a href="../index.html#library">全部资料</a> / 网页来源</p><h1>'+H(title)+'</h1><p>该项为网页介绍或资料入口。课程视频、完整题库及付费内容的访问条件以发布方为准。</p><p><a class="button" href="'+H(row['url'],quote=True)+'" target="_blank" rel="noopener noreferrer">访问原始网站</a></p><details><summary>查看保存的网页文字</summary><pre>'+H(text)+'</pre></details></article>'
  (OUT/'sources'/(row['id']+'.html')).write_text(page(title,body,1));dest='sources/'+row['id']+'.html';action='查看网页与入口'
 else:state='未取回原文件';action='访问原始来源';dest=row['url']
 cat=row['category'];
 if '非本次' in cat:cat='其他等级考试（补充档案）'
 if '真题' in cat:cat='历年回忆题与真题入口'
 if '考点笔记' in cat:cat='考点笔记与时政'
 data={'id':row['id'],'title':title,'category':cat,'year':row.get('year_hint',''),'state':state,'kind':kind,'href':dest,'action':action,'url':row['url'],'trust':row['trust']}
 catalogue.append(data)
(OUT/'catalogue.json').write_text(json.dumps(catalogue,ensure_ascii=False,indent=2))
(OUT/'pdfs.json').write_text(json.dumps(PDFS,ensure_ascii=False,indent=2))
# Remove only obsolete copies of our own generated booklet, preserving source PDFs.
current_pdf_files={entry['file'] for entry in PDFS}
for old in previous_pdfs:
 if old['title'] in {'研究与预测复习册','分类记忆与进阶训练复习册'} and old['file'] not in current_pdf_files:
  obsolete=OUT/old['file']
  if re.fullmatch(r'assets/[a-f0-9]{16}\.pdf',old['file']) and obsolete.is_file():obsolete.unlink()
cats=sorted({x['category'] for x in catalogue});cards=[]
for c in catalogue:
 external=c['href'].startswith('https:');attrs=' target="_blank" rel="noopener noreferrer"' if external else ''
 search=' '.join([c['title'],c['category'],c['year'],c['id'],c['state']]).lower()
 cards.append('<article class="resource" data-search="'+H(search,quote=True)+'" data-category="'+H(c['category'],quote=True)+'" data-kind="'+c['kind']+'"><span class="tag">'+H(c['category'])+'</span><h3>'+H(c['title'])+'</h3><div class="meta">'+H(c['year'])+' · '+H(c['trust'].split(' ')[0])+'类来源 · '+c['id']+'</div><span class="state">'+H(c['state'])+'</span><div class="resource-actions"><a href="'+H(c['href'],quote=True)+'"'+attrs+'>'+c['action']+'</a><a href="'+H(c['url'],quote=True)+'" target="_blank" rel="noopener noreferrer">原始来源 ↗</a></div></article>')
body=f'''<section class="hero"><div><p class="eyebrow">全国笔试 + 云南中文面试</p><h1>资料都在这里，<br>按顺序开始复习。</h1><p class="lead">先按四科分类表记忆，再用进阶题辨析易混点，最后逐个练习云南面试景点。大纲、回忆题和考点笔记，随时在目录里查找。</p><div class="actions"><a class="button" href="study/index.html">打开四科分类记忆</a><a class="button secondary" href="study/agent.html">Agent先读：学习记录</a><a class="button secondary" href="{H(viewer_url(book,'分类记忆与进阶训练复习册'),quote=True)}">阅读完整复习册</a></div></div><aside class="note-card"><p class="eyebrow">考前提醒</p><div class="date">11月21日 · 全国笔试</div><p>准考证自11月16日9:00起下载。</p><small>科三、科四在合卷中各占50%。<br>云南中文面试：12个指定景点，注意团型与讲解顺序。具体安排以官方通知、准考证为准。</small></aside></section><div class="metrics"><div><strong>{len(catalogue)}</strong><span>条可追溯资料来源</span></div><div><strong>{len(PDFS)}</strong><span>份可浏览的 PDF</span></div><div><strong>100</strong><span>道原创进阶练习</span></div><div><strong>12</strong><span>个云南面试景点</span></div></div><section class="section" aria-labelledby="order-title"><div class="section-heading"><div><p class="eyebrow">建议阅读顺序</p><h2 id="order-title">先看哪份，再学什么</h2></div><p>不必一次读完所有资料，先完成这三步。</p></div><div class="steps"><article class="step"><div class="number">第一步 · 明确重点</div><h3>按四科分类表建立记忆</h3><p>茶类、古籍作者、法规条件、业务流程和全国地区按表记忆；先补个人记录中的具体缺口。</p><a href="study/index.html">阅读四科分类表 →</a></article><article class="step"><div class="number">第二步 · 查缺补漏</div><h3>做100道原创进阶题</h3><p>按科目和题型筛选，辨析相近概念；提交后分别看漏选、误选与依据，隐藏本页已答对题。</p><a href="quiz.html">开始在线训练 →</a></article><article class="step"><div class="number">第三步 · 开口练习</div><h3>准备云南中文面试</h3><p>12景点按对应团型练讲解，再练导游服务规范、应变能力与云南综合知识问答。</p><a href="articles/yunnan.html">查看景点与问答 →</a></article></div></section><section id="library" class="section" aria-labelledby="library-title"><div class="section-heading"><div><p class="eyebrow">按需查阅</p><h2 id="library-title">全部资料目录</h2></div><a href="articles/courses.html">课程与教材怎么选 →</a></div><p class="hint">官方大纲确定范围；历年回忆题和旧版笔记仅作辅助。网页入口不等于离线课程，受限课件已单独标明。</p><div class="search-panel"><div class="search-row"><div class="field"><label for="search">搜索资料</label><input type="search" id="search" placeholder="例如：云南、大纲、2025真题、时政" autocomplete="off"></div><div class="field"><label for="category">资料分类</label><select id="category"><option value="">全部分类</option>{''.join('<option>'+H(c)+'</option>' for c in cats)}</select></div><div class="field"><label for="kind">阅读形式</label><select id="kind"><option value="">全部形式</option><option>PDF</option><option>展开资料</option><option>网页</option></select></div></div><p class="result-info" id="result-count" aria-live="polite">共 {len(catalogue)} 条资料</p></div><div class="resource-grid">{''.join(cards)}</div><p id="empty" class="empty" hidden>没有找到匹配资料，请换一个关键词或清除筛选。</p></section><script src="library.js" defer></script>'''
(OUT/'index.html').write_text(page('阅读首页',body,active='阅读首页'))
(OUT/'library.js').write_text('''const search=document.getElementById('search'),category=document.getElementById('category'),kind=document.getElementById('kind'),cards=[...document.querySelectorAll('.resource')];function filter(){let n=0;const q=search.value.trim().toLowerCase();cards.forEach(c=>{const show=(!q||c.dataset.search.includes(q))&&(!category.value||c.dataset.category===category.value)&&(!kind.value||c.dataset.kind===kind.value);c.hidden=!show;if(show)n++});document.getElementById('result-count').textContent=`显示 ${n} / ${cards.length} 条资料`;document.getElementById('empty').hidden=n!==0}search.addEventListener('input',filter);category.addEventListener('change',filter);kind.addEventListener('change',filter);filter();''')
# PDF viewer uses native browser viewing, with a direct-PDF link for iOS and embedded-view limitations.
body='<section class="viewer"><p class="crumb"><a href="index.html#library">全部资料</a> / PDF 阅读</p><h1 id="doc-title">正在打开资料</h1><p class="lead">如果内嵌阅读只显示第一页或无法翻页，请直接打开完整 PDF。</p><div class="actions"><a id="direct" class="button" hidden>在浏览器中打开完整 PDF</a><a class="button secondary" href="index.html#library">返回资料目录</a></div><p id="viewer-error" role="alert" hidden>未找到该资料，请从目录重新选择。</p><iframe id="pdf-frame" class="pdf-frame" title="PDF资料阅读区域" hidden></iframe></section><script src="viewer.js" defer></script>'
(OUT/'viewer.html').write_text(page('PDF 阅读',body))
(OUT/'viewer.js').write_text('''const p=new URLSearchParams(location.search),file=p.get('file')||'',title=p.get('title')||'PDF资料';document.getElementById('doc-title').textContent=title;document.title=title+' · 2026导考资料库';if(/^assets\\/[a-f0-9]{16}\\.pdf$/.test(file)){const a=document.getElementById('direct');a.href=file;a.hidden=false;const f=document.getElementById('pdf-frame');f.src=file;f.hidden=false}else{document.getElementById('viewer-error').hidden=false}''')
questions=json.loads((ROOT/'reports/原创预测训练100题.json').read_text());quiz_json=json.dumps(questions,ensure_ascii=False).replace('</','<\\/')
body='''<section class="quiz-header"><p class="eyebrow">全国笔试 · 原创进阶训练</p><h1>100道进阶题，辨清条件与易混点。</h1><p class="lead">每科25题，共60道单选、40道多选。用合理近似的干扰项检验知识，提交后查看漏选、误选和逐题解析。这是原创练习，题型比例不等同正式试卷，不预测考试分数。</p><div class="actions"><a href="study/index.html">先看四科分类记忆</a><a href="articles/questions.html">阅读完整题目</a><a href="articles/answers.html">查看全部答案</a><a href="articles/quality.html">本次修订说明</a></div><p class="hint">此页只记录当前页面会话的作答，刷新后重置，不会自动修改个人学习记忆。<a href="study/agent.html">已答对的具体考点与待补点请先看学习记录。</a></p><div class="quiz-tools"><div class="quiz-filters"><div class="field"><label for="subject">选择科目</label><select id="subject"><option value="">全部四科</option>'''+''.join('<option>'+H(subject)+'</option>' for subject in dict.fromkeys(q['subject'] for q in questions))+'''</select></div><div class="field"><label for="question-type">题型</label><select id="question-type"><option value="">全部题型</option><option>单选</option><option>多选</option></select></div><label class="quiz-check"><input type="checkbox" id="hide-correct">隐藏本页已答对题</label></div><p class="quiz-progress" id="progress" aria-live="polite">本页已答 0 / 100，答对 0 题</p></div><p id="visible-count" class="quiz-summary" aria-live="polite"></p><div id="questions"></div><p id="quiz-empty" class="empty" hidden>当前筛选下没有待显示题目。可调整科目、题型或取消隐藏已答对题。</p><noscript><p class="hint">在线作答需要开启 JavaScript，也可通过上方链接阅读题目与答案。</p></noscript></section><script type="application/json" id="quiz-data">'''+quiz_json+'<'+'''/script><script src="quiz.js" defer></script>'''
(OUT/'quiz.html').write_text(page('进阶训练',body,active='进阶训练',route='quiz.html'))
(OUT/'quiz.js').write_text('''const data=JSON.parse(document.getElementById('quiz-data').textContent);
const results=new Map(),root=document.getElementById('questions'),labels='ABCDEF';
const subject=document.getElementById('subject'),questionType=document.getElementById('question-type'),hideCorrect=document.getElementById('hide-correct');
function filterQuestions(){let count=0;for(const card of root.children){const show=(!subject.value||card.dataset.subject===subject.value)&&(!questionType.value||card.dataset.type===questionType.value)&&(!hideCorrect.checked||results.get(Number(card.dataset.id))!==true);card.hidden=!show;if(show)count++;}document.getElementById('visible-count').textContent=`当前显示 ${count} / ${data.length} 题`;document.getElementById('quiz-empty').hidden=count!==0;}
function answerLabel(q,text){return labels[q.options.indexOf(text)]+'. '+text;}
for(const q of data){
 const card=document.createElement('article');card.className='question';card.dataset.subject=q.subject;card.dataset.type=q.type;card.dataset.id=String(q.id);
 const meta=document.createElement('div');meta.className='qmeta';meta.textContent=String(q.id)+' · '+q.subject+' · '+q.type+' · '+q.difficulty;card.append(meta);
 const fs=document.createElement('fieldset'),legend=document.createElement('legend');legend.textContent=q.stem;fs.append(legend);
 q.options.forEach((option,index)=>{const label=document.createElement('label');label.className='option';const input=document.createElement('input');input.type=q.type==='多选'?'checkbox':'radio';input.name='question-'+q.id;input.value=String(index);const span=document.createElement('span');span.textContent=labels[index]+'. '+option;label.append(input,span);fs.append(label);});
 const button=document.createElement('button');button.type='button';button.textContent='确认作答，查看解析';button.disabled=true;
 const feedback=document.createElement('div');feedback.className='feedback';feedback.hidden=true;feedback.setAttribute('aria-live','polite');
 fs.addEventListener('change',()=>{button.disabled=!fs.querySelector('input:checked');feedback.hidden=true;});
 button.addEventListener('click',()=>{
  const chosen=[...fs.querySelectorAll('input:checked')].map(input=>q.options[Number(input.value)]);
  const missed=q.answer.filter(answer=>!chosen.includes(answer)),wrong=chosen.filter(answer=>!q.answer.includes(answer));
  const good=missed.length===0&&wrong.length===0;results.set(q.id,good);feedback.className='feedback'+(good?'':' wrong');feedback.replaceChildren();
  const title=document.createElement('strong');title.textContent=good?'回答正确':'这题需要再巩固';feedback.append(title);
  if(!good){const differences=document.createElement('p');differences.className='selection-error';differences.textContent='漏选：'+(missed.map(text=>answerLabel(q,text)).join('；')||'无')+'。误选：'+(wrong.map(text=>answerLabel(q,text)).join('；')||'无')+'。';feedback.append(differences);}
  for(const text of ['正确答案：'+q.answer.map(answer=>answerLabel(q,answer)).join('；'),'解析：'+q.explanation,'知识点：'+q.knowledge_point,'依据：'+q.source]){const paragraph=document.createElement('p');paragraph.textContent=text;feedback.append(paragraph);}
  feedback.hidden=false;button.textContent='重新核对答案';document.getElementById('progress').textContent=`本页已答 ${results.size} / ${data.length}，答对 ${[...results.values()].filter(Boolean).length} 题`;filterQuestions();
 });
 card.append(fs,button,feedback);root.append(card);
}
for(const control of [subject,questionType,hideCorrect])control.addEventListener('change',filterQuestions);filterQuestions();''')
about='''<article class="article"><p class="crumb"><a href="index.html">阅读首页</a> / 使用说明</p><h1>这份资料库怎么用</h1><h2>按顺序学习，按需查资料</h2><ol><li>先读“考试与复习重点”，确认2026考试范围、变化与时间安排。</li><li>先读四科分类记忆，再做原创进阶题，结合漏选、误选和解析补缺口。</li><li>准备云南12景点，按团型和顺序录音练习，再练24道面试问答。</li><li>需要补充时，用目录搜索官方原件、回忆题、模拟题和课程入口。</li></ol><h2>哪些内容已经可以直接看</h2><p>PDF原件可在线阅读；两份公开ZIP中的复习材料已展开；可读取的Office文件与出版社样章已转换为PDF。部分出版社内层课件受密码保护，保留获取说明和原站入口，未解密。</p><p>网页条目提供原站入口与纯文字存档，课程视频和付费内容的条件以发布方为准。旧题与旧笔记不能替代2026大纲。OCR仅辅助检索，背诵与引用请核对扫描原件。</p><h2>资料来源与局限</h2><p>来源包括政府网站、出版社、高校课程、国际机构与培训平台。官方文件用于确认考试范围，第三方回忆题存在错录、缺项与过时信息。本站原创预测是复习优先级，未提供可靠命中概率，也不保证通过考试。</p><p>原资料权利与使用条件属于原发布方，本站不对第三方文件重新授予开源许可。资料截点为2026年11月14日，之后的考试通知请及时查看官方发布。</p><p><a href="index.html#library">查看完整资料目录与原始来源</a> · <a href="https://github.com/6sjsmmzn8z-cmd/daoyou-2026-yunnan" target="_blank" rel="noopener noreferrer">查看GitHub仓库</a></p></article>'''
(OUT/'about.html').write_text(page('来源与使用说明',about))
(OUT/'site_stats.json').write_text(json.dumps({'sources':len(catalogue),'readable_pdfs':len(PDFS),'questions':len(questions),'expanded_files':sum(len(g['files']) for g in groups.values())},ensure_ascii=False,indent=2))
print('BUILT',len(catalogue),'sources;',len(PDFS),'readable PDFs;',len(questions),'advanced questions; study pages and continuous reading navigation')
