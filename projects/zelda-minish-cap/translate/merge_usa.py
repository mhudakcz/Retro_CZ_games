#!/usr/bin/env python3
"""Merge translated chunks back into translations/USA.json."""
import json, glob

usa = json.load(open('translations/USA.json', encoding='utf-8'))

cz_by_pos = {}
for path in sorted(glob.glob('translate/chunks/chunk_*.json')):
    chunk = json.load(open(path, encoding='utf-8'))
    for e in chunk:
        if e.get('cz', '').strip():
            cz_by_pos[(e['gi'], e['si'])] = e['cz']

filled = 0
for gi, g in enumerate(usa):
    for si, s in enumerate(g):
        if (gi, si) in cz_by_pos:
            g[si] = cz_by_pos[(gi, si)]
            filled += 1

json.dump(usa, open('translations/USA.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
print(f'Merged {filled} translated strings into translations/USA.json')
