#!/usr/bin/env python3
"""List exact paths of untranslated .inc files."""
import pathlib, re

ENGLISH_MARKERS = re.compile(
    r'\b(the|and|you|your|with|that|this|have|will|from|they|were|some|good|like|here|come|now|right|going|over|when)\b',
    re.I,
)
CZECH_MARKERS = re.compile(
    r'\b(je|jsem|jsi|jsou|byl|byla|byti|nebo|prijd|tve|tvuj|tva|musis|mám|mas|pro|mezi|tady|kazdy|pojd|díky|tvoji)\b',
    re.I,
)

base = pathlib.Path('data')
for f in sorted(base.rglob('*.inc')):
    text = f.read_text(encoding='utf-8', errors='ignore')
    strings = re.findall(r'\.string\s+"((?:[^"\\]|\\.)*)"', text)
    if not strings:
        continue
    body = ' '.join(strings)
    eng = len(ENGLISH_MARKERS.findall(body))
    cz = len(CZECH_MARKERS.findall(body))
    if eng > 5 and cz < 2:
        print(str(f).replace('\\', '/'))
