#!/usr/bin/env python3
"""Merge translated chunks back into aw1_strings.json (matched on idx)."""
import json, glob, re

BS = chr(92)
base = json.load(open('translate/aw1_strings.json', encoding='utf-8'))
for idx, e in enumerate(base):
    e['idx'] = idx

cz_by_idx = {}
for path in sorted(glob.glob('translate/chunks/chunk_*.json')):
    for e in json.load(open(path, encoding='utf-8')):
        if e.get('cz', '').strip():
            cz_by_idx[e['idx']] = e['cz']

# Sanity check: the control codes must survive translation untouched.
pat = re.compile(re.escape(BS) + r'(?:r|e|f|x[0-9A-Fa-f]{2})')
filled = mismatched = 0
for e in base:
    cz = cz_by_idx.get(e['idx'])
    if not cz:
        continue
    if pat.findall(e['en']) != pat.findall(cz):
        mismatched += 1
        if mismatched <= 10:
            print('  control-code mismatch at idx %d:' % e['idx'])
            print('    en: %r' % e['en'][:70])
            print('    cz: %r' % cz[:70])
        continue                       # keep English rather than risk a crash
    e['cz'] = cz
    filled += 1

for e in base:
    e.pop('idx', None)

json.dump(base, open('translate/aw1_strings.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print('Merged %d translated strings (%d rejected for control-code mismatch)'
      % (filled, mismatched))
print('Coverage: %d/%d (%.1f%%)'
      % (filled, len(base), 100.0 * filled / len(base)))
