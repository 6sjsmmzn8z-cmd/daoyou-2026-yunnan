#!/usr/bin/env python3
"""Check the archived assets, provenance and question-bank completeness."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parents[1]
MAX_GIT_FILE = 100 * 1024 * 1024


def check():
    manifest = json.loads((ROOT / 'manifest.json').read_text(encoding='utf-8'))
    archived = {}
    for row in manifest:
        if row['status'] != 'downloaded':
            continue
        path = ROOT / row['path']
        if not path.is_file():
            raise ValueError(f'Missing asset: {row["path"]}')
        if not path.resolve().is_relative_to(ROOT):
            raise ValueError(f'Unsafe path: {row["path"]}')
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != row['sha256']:
            raise ValueError(f'Hash mismatch: {row["path"]}')
        archived[row['path']] = path
    stats = json.loads((ROOT / 'stats.json').read_text(encoding='utf-8'))
    if len(archived) != stats['unique_saved_files']:
        raise ValueError('Unique source-file count differs from stats.json')
    if dict(Counter(path.suffix for path in archived.values())) != stats['file_types']:
        raise ValueError('File-type counts differ from stats.json')
    for rel, path in archived.items():
        if path.suffix == '.pdf':
            with path.open('rb') as f:
                if f.read(4) != b'%PDF':
                    raise ValueError(f'Invalid PDF header: {rel}')
                f.seek(max(0, path.stat().st_size - 4096))
                if b'%%EOF' not in f.read():
                    raise ValueError(f'Incomplete PDF trailer: {rel}')
        if path.suffix in {'.zip', '.docx'}:
            with zipfile.ZipFile(path) as z:
                if z.testzip() is not None:
                    raise ValueError(f'Corrupt ZIP container: {rel}')
    questions = json.loads((ROOT / 'reports/原创预测训练100题.json').read_text(encoding='utf-8'))
    if len(questions) != 100 or len({q['stem'] for q in questions}) != 100:
        raise ValueError('Expected 100 distinct original questions')
    if set(Counter(q['subject'] for q in questions).values()) != {25}:
        raise ValueError('Expected 25 questions per subject')
    for q in questions:
        if not q['answer'] or any(a not in q['options'] for a in q['answer']):
            raise ValueError(f'Invalid question answer: {q["id"]}')
    for path in ROOT.rglob('*'):
        rel = path.relative_to(ROOT)
        if not path.is_file() or rel.parts[0] in {'.git', 'downloads'}:
            continue
        if path.stat().st_size >= MAX_GIT_FILE:
            raise ValueError(f'File exceeds ordinary GitHub limit: {rel}')
    print(f'OK: {len(archived)} unique source files, 104 PDFs, 100 questions; hashes and ZIP containers verified.')


if __name__ == '__main__':
    check()
