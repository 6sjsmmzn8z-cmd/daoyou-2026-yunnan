#!/usr/bin/env python3
"""Export the canonical practice bank; --book also rebuilds the DOCX/PDF booklet."""
from pathlib import Path
from collections import Counter
import argparse
import csv
import io
import json
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / 'reports'
REVISION = '2026-11-16'


def pandoc(text, *args):
    return subprocess.check_output(['pandoc', '--from=gfm', '--wrap=none', *args], input=text, text=True)


def build_exports():
    questions = json.loads((REPORTS / '原创预测训练100题.json').read_text())
    assert len(questions) == 100
    assert {q['id'] for q in questions} == set(range(101, 201))
    assert Counter(q['type'] for q in questions) == {'单选': 60, '多选': 40}
    assert sorted(Counter(q['subject'] for q in questions).values()) == [25] * 4
    assert len({q['stem'] for q in questions}) == 100
    for q in questions:
        assert len(set(q['options'])) == len(q['options'])
        assert len(set(q['answer'])) == len(q['answer'])
        assert q['answer'] and set(q['answer']).issubset(q['options'])
        if q['type'] == '单选':
            assert len(q['answer']) == 1
        else:
            assert 2 <= len(q['answer']) < len(q['options'])
        assert q['difficulty'] == '进阶' and q['knowledge_point']
        assert q['source'] and q['explanation']
    intro = (
        f'修订日期：{REVISION}。四科各25题，共60道单选、40道多选。'
        '本版替换低区分度旧训练，题号101—200，避免与旧作答记录混淆。\n\n'
        '本套为原创进阶练习，以条件、相近概念与易混对应辨析为主；'
        '未经真实样本难度校准，不代表官方真题或命题频率，题型比例不等同正式考试。'
        '多选选出所有正确项，不据此推定正式考试漏选计分规则。\n\n'
        '接手辅导先读根目录Agent必读与study/progress.json；旧题下线不清空历史作答证据，'
        '已答对的具体点不重复问。\n\n'
    )
    paper = ['# 100道原创进阶训练：试题\n\n', intro]
    answers = ['# 100道原创进阶训练：答案与逐题解析\n\n', intro]
    last_subject = None
    records = []
    for q in questions:
        if q['subject'] != last_subject:
            for chunks in (paper, answers):
                chunks.append(f"## {q['subject']}\n\n")
            last_subject = q['subject']
        paper.append(f"### {q['id']}．【{q['type']}】{q['stem']}\n\n")
        for index, option in enumerate(q['options']):
            paper.append(f"{chr(65 + index)}. {option}\n\n")
        letters = [chr(65 + q['options'].index(a)) for a in q['answer']]
        answers.append(f"### {q['id']}．{q['stem']}\n\n**正确答案：{'、'.join(letters)}**\n\n")
        answers.extend(f"- {letter}：{answer}\n" for letter, answer in zip(letters, q['answer']))
        answers.append(f"\n**解析：**{q['explanation']}\n\n**知识点：**{q['knowledge_point']}\n\n**依据：**{q['source']}\n\n")
        records.append({
            'id': q['id'], 'subject': q['subject'], 'type': q['type'], 'stem': q['stem'],
            'options': json.dumps(q['options'], ensure_ascii=False),
            'answer': json.dumps(q['answer'], ensure_ascii=False),
            'explanation': q['explanation'], 'source': q['source'],
            'difficulty': q['difficulty'], 'knowledge_point': q['knowledge_point'],
        })
    for name, chunks in [('03_原创预测训练100题_试题', paper), ('04_原创预测训练100题_答案解析', answers)]:
        text = ''.join(chunks).rstrip() + '\n'
        (REPORTS / f'{name}.md').write_text(text)
        (REPORTS / f'{name}.html').write_text(pandoc(text, '--to=html5', '--standalone', '--metadata', 'pagetitle=2026导考原创进阶训练'))
    output = io.StringIO(newline='')
    writer = csv.DictWriter(output, fieldnames=list(records[0]), lineterminator='\n')
    writer.writeheader()
    writer.writerows(records)
    (REPORTS / '原创预测训练100题.csv').write_text(output.getvalue(), encoding='utf-8-sig')
    print('Exported 100 canonical questions to CSV, Markdown and HTML.')


def build_book():
    import fitz
    sources = [ROOT / 'study/README.md', *sorted((ROOT / 'study').glob('0[1-4]-*.md'))]
    sources += [REPORTS / p for p in ['01_研究结论与考点预测.md', '02_云南中文面试重点与12景点提纲.md', '03_原创预测训练100题_试题.md', '04_原创预测训练100题_答案解析.md', '05_课程课件与教材使用指南.md']]
    title = '2026导考复习册：四科分类记忆与100道进阶训练'
    markdown = f'# {title}\n\n更新：{REVISION}。原创复习资料，非官方试卷。\n\n'
    markdown += '\n\n---\n\n'.join(p.read_text() for p in sources)
    with tempfile.TemporaryDirectory() as work:
        source = Path(work) / 'book.md'
        source.write_text(markdown)
        subprocess.run(['pandoc', '--from=gfm', str(source), '-o', str(ROOT / 'study.docx'), '--metadata', f'title={title}'], check=True)
    body = pandoc(markdown, '--to=html5')
    css = 'body{font-family:sans-serif;font-size:9.5pt;line-height:1.5}h1{font-size:19pt}h2{font-size:15pt}h3{font-size:12pt}table{border-collapse:collapse;width:100%;font-size:8pt}th,td{border:0.5pt solid #999;padding:4pt;vertical-align:top}a{color:#205d4d}'
    story = fitz.Story(html=body, user_css=css)
    output = io.BytesIO()
    writer = fitz.DocumentWriter(output)
    paper = fitz.paper_rect('a4')
    area = paper + (35, 38, -35, -38)
    more, pages = True, 0
    while more:
        device = writer.begin_page(paper)
        more, _ = story.place(area)
        story.draw(device)
        writer.end_page()
        pages += 1
        if pages > 400:
            raise RuntimeError('Book pagination did not converge.')
    writer.close()
    pdf = fitz.open(stream=output.getvalue(), filetype='pdf')
    pdf.set_metadata({'title': title, 'subject': '四科分类记忆与原创进阶训练', 'author': '考试资料整理'})
    pdf.save(ROOT / 'study.pdf', garbage=4, deflate=True)
    print(f'Rebuilt study.docx and study.pdf ({len(pdf)} pages).')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--book', action='store_true', help='also rebuild DOCX/PDF with Pandoc and PyMuPDF')
    args = parser.parse_args()
    build_exports()
    if args.book:
        build_book()
