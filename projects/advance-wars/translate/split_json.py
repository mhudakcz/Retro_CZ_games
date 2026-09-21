#!/usr/bin/env python3
"""Split aw1_strings.json into chunks for parallel translation.

Strings stay in ROM order so a chunk holds whole scenes rather than a random
scatter of lines. Entries that must not be translated (the in-ROM charset
table) are dropped from the chunks and keep their English text at inject time.
"""
import json, sys, math, os

n_chunks = int(sys.argv[1]) if len(sys.argv) > 1 else 14
entries = json.load(open('translate/aw1_strings.json', encoding='utf-8'))

for idx, e in enumerate(entries):
    e['idx'] = idx


def translatable(e):
    en = e['en']
    if 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' in en:      # charset table, not dialogue
        return False
    return True


work = [e for e in entries if translatable(e)]
print('%d strings, %d translatable' % (len(entries), len(work)))

per = math.ceil(len(work) / n_chunks)
os.makedirs('translate/chunks', exist_ok=True)
for c in range(n_chunks):
    chunk = work[c * per:(c + 1) * per]
    if not chunk:
        continue
    path = 'translate/chunks/chunk_%02d.json' % c
    slim = [{'idx': e['idx'], 'en': e['en'], 'cz': ''} for e in chunk]
    json.dump(slim, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('%s: %d strings, %d bytes of text'
          % (path, len(chunk), sum(len(e['en']) for e in chunk)))
