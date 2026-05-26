#!/usr/bin/env python3
"""Split aw2_strings.json into N chunks for parallel translation."""
import json, sys, math, os

n_chunks = int(sys.argv[1]) if len(sys.argv) > 1 else 10
entries = json.load(open('translate/aw2_strings.json', encoding='utf-8'))

# Assign a stable index to each entry so we can merge back
for idx, e in enumerate(entries):
    e['idx'] = idx

per = math.ceil(len(entries) / n_chunks)
os.makedirs('translate/chunks', exist_ok=True)
for c in range(n_chunks):
    chunk = entries[c*per:(c+1)*per]
    if not chunk:
        continue
    path = f'translate/chunks/chunk_{c:02d}.json'
    json.dump(chunk, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'{path}: {len(chunk)} strings')
print(f'\nTotal {len(entries)} strings in {n_chunks} chunks (~{per} each)')
