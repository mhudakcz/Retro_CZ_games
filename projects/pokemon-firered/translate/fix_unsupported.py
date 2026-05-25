#!/usr/bin/env python3
"""Auto-fix unsupported Czech diacritics in all .inc files.

Maps Czech chars that aren't in FireRed charmap to ASCII equivalents.
Run after agents finish to catch any diacritics that slipped through.
"""
import pathlib
import sys

# Czech diacritics that are NOT in FireRed charmap → transliterate
MAPPING = {
    'ý': 'y', 'Ý': 'Y',
    'č': 'c', 'Č': 'C',
    'š': 's', 'Š': 'S',
    'ž': 'z', 'Ž': 'Z',
    'ř': 'r', 'Ř': 'R',
    'ě': 'e', 'Ě': 'E',
    'ť': 't', 'Ť': 'T',
    'ď': 'd', 'Ď': 'D',
    'ň': 'n', 'Ň': 'N',
    'ů': 'u', 'Ů': 'U',
    # Em-dash → en-dash (en-dash is in charmap as '-')
    '—': '-',
    '–': '-',
    # Curly quotes that aren't in charmap (avoid issues)
    '„': '"',  # Czech opening
    '"': '"',  # German closing — wait, these may be in charmap; safer no-op
    # Non-breaking space → regular space
    ' ': ' ',
}

def fix_file(path: pathlib.Path) -> int:
    text = path.read_text(encoding='utf-8')
    orig = text
    changes = 0
    for src, dst in MAPPING.items():
        if src in text:
            n = text.count(src)
            text = text.replace(src, dst)
            changes += n
    if text != orig:
        path.write_text(text, encoding='utf-8')
    return changes

if __name__ == '__main__':
    base = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'data')
    total_changes = 0
    files_changed = 0
    for ext in ('*.inc', '*.s', '*.asm'):
        for f in base.rglob(ext):
            n = fix_file(f)
            if n:
                files_changed += 1
                total_changes += n
                print(f'  fixed {n:3d} chars in {f}')
    print(f'\nTotal: {files_changed} files, {total_changes} character replacements')
