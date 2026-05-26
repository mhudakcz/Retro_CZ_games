#!/usr/bin/env python3
"""Report how many chunks have cz filled."""
import json, glob
done = 0
total_chunks = 0
for path in sorted(glob.glob('translate/chunks/chunk_*.json')):
    total_chunks += 1
    chunk = json.load(open(path, encoding='utf-8'))
    filled = sum(1 for e in chunk if e.get('cz', '').strip())
    pct = filled * 100 // max(len(chunk), 1)
    status = 'DONE' if pct >= 40 else 'wait'
    if pct >= 40:
        done += 1
    print(f'{path}: {filled}/{len(chunk)} ({pct}%) {status}')
print(f'CHUNKS_DONE={done}/{total_chunks}')
