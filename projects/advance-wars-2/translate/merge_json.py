#!/usr/bin/env python3
"""Merge translated chunks back into aw2_strings.json (by idx)."""
import json, glob

base = json.load(open('translate/aw2_strings.json', encoding='utf-8'))
# base has no idx; add it
for idx, e in enumerate(base):
    e['idx'] = idx

cz_by_idx = {}
for path in sorted(glob.glob('translate/chunks/chunk_*.json')):
    chunk = json.load(open(path, encoding='utf-8'))
    for e in chunk:
        if e.get('cz', '').strip():
            cz_by_idx[e['idx']] = e['cz']

filled = 0
for e in base:
    if e['idx'] in cz_by_idx:
        e['cz'] = cz_by_idx[e['idx']]
        filled += 1
    e.pop('idx', None)

json.dump(base, open('translate/aw2_strings.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'Merged {filled} translated strings into aw2_strings.json')
