#!/usr/bin/env python3
"""Find which .inc files are still mostly English (untranslated)."""
import pathlib
import re
import sys
from collections import Counter

ENGLISH_MARKERS = re.compile(
    r'\b(the|and|you|your|with|that|this|have|will|from|they|were|some|good|like|here|come|come|now|right|going|over|when|going)\b',
    re.I,
)
CZECH_MARKERS = re.compile(
    r'\b(je|jsem|jsi|jsou|byl|byla|byti|nebo|prijd|tve|tvuj|tva|musis|mám|mas|pro|mezi|tady|kazdy|nej|ne|tvuj|tvoji|nejde|tvého|pojd|díky)\b',
    re.I,
)

def main():
    base = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'data')
    untranslated = []
    translated = []
    for f in base.rglob('*.inc'):
        text = f.read_text(encoding='utf-8', errors='ignore')
        strings = re.findall(r'\.string\s+"((?:[^"\\]|\\.)*)"', text)
        if not strings:
            continue
        body = ' '.join(strings)
        eng = len(ENGLISH_MARKERS.findall(body))
        cz = len(CZECH_MARKERS.findall(body))
        if eng > 5 and cz < 2:
            untranslated.append((f, eng, cz, len(body)))
        else:
            translated.append(f)

    print(f'Translated:   {len(translated)}')
    print(f'Untranslated: {len(untranslated)}')
    print()
    groups = Counter()
    for f, _, _, _ in untranslated:
        parts = f.parts
        if 'maps' in parts:
            idx = parts.index('maps')
            name = parts[idx+1] if idx+1 < len(parts) else 'maps'
            groups[name.split('_')[0]] += 1
        else:
            groups[f.parent.name] += 1
    print('Untranslated by region:')
    for region, n in sorted(groups.items(), key=lambda x: -x[1]):
        print(f'  {n:3d}  {region}')
    print()
    print('First 30 untranslated files:')
    for f, eng, cz, sz in sorted(untranslated, key=lambda x: -x[3])[:30]:
        rel = f.relative_to(base.parent if base.name == 'data' else '.')
        print(f'  {sz:5d}  {rel}')

if __name__ == '__main__':
    main()
