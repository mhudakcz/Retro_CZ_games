#!/usr/bin/env python3
"""Split USA.json's 80 groups into ~N chunks for parallel translation.

Output: chunks/chunk_NN.json containing a list of [group_idx, string_idx, en, cz=""].
We flatten so each entry is independently translatable.
"""
import json, math, os, sys

n_chunks = int(sys.argv[1]) if len(sys.argv) > 1 else 8

d = json.load(open('translations/USA.json', encoding='utf-8'))
entries = []
for gi, g in enumerate(d):
    for si, s in enumerate(g):
        if isinstance(s, str) and s.strip():
            entries.append({'gi': gi, 'si': si, 'en': s, 'cz': ''})

per = math.ceil(len(entries) / n_chunks)
os.makedirs('translate/chunks', exist_ok=True)
for c in range(n_chunks):
    chunk = entries[c*per:(c+1)*per]
    if not chunk:
        continue
    path = f'translate/chunks/chunk_{c:02d}.json'
    json.dump(chunk, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'{path}: {len(chunk)} strings')

print(f'\nTotal {len(entries)} entries in {n_chunks} chunks (~{per} each)')
