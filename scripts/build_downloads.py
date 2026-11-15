#!/usr/bin/env python3
"""Build downloadable archives using only standard Python modules."""
from pathlib import Path
import json
import zipfile
from check import check

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'downloads'


def write_zip(destination, files, prefix):
    with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED, compresslevel=5) as z:
        for path in sorted(set(files)):
            z.write(path, str(Path(prefix) / path.relative_to(ROOT)))
    with zipfile.ZipFile(destination) as z:
        if z.testzip() is not None:
            raise ValueError(f'ZIP checksum verification failed: {destination}')
    print(f'{destination.name}: {destination.stat().st_size:,} bytes')


def main():
    check()
    OUT.mkdir(exist_ok=True)
    all_files = [p for p in ROOT.rglob('*') if p.is_file()
                 and p.relative_to(ROOT).parts[0] not in {'.git', 'downloads'}
                 and '__pycache__' not in p.parts and p.name != '.DS_Store']
    write_zip(OUT / 'guide-all.zip', all_files, 'daoyou-2026-yunnan')
    core = [ROOT / 'README.md', ROOT / 'RIGHTS.md', ROOT / 'study.pdf', ROOT / 'study.docx',
            ROOT / '资源总表.csv', ROOT / 'manifest.json']
    core.extend(p for p in (ROOT / 'reports').iterdir() if p.is_file())
    words = ['2026全国导游资格考试笔试大纲_官方', '2026云南省', '2026研学旅游合同',
             '旅游强国建设十五五', 'GB_T15971', '2025导游资格', '2024年全国导游格',
             '2026导游资格时事', '导游资格面试-导游', '清华出版社']
    for row in json.loads((ROOT / 'manifest.json').read_text(encoding='utf-8')):
        if row['status'] == 'downloaded' and Path(row['path']).suffix in {'.pdf', '.doc', '.rar', '.zip'}:
            if any(word in row.get('title', '') for word in words):
                core.append(ROOT / row['path'])
    write_zip(OUT / 'guide-core.zip', core, 'daoyou-core')
    (OUT / 'checksums.json').write_text(json.dumps(
        {'guide-all.zip': (OUT / 'guide-all.zip').stat().st_size,
         'guide-core.zip': (OUT / 'guide-core.zip').stat().st_size}, indent=2) + '\n')


if __name__ == '__main__':
    main()
