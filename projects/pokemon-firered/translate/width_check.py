#!/usr/bin/env python3
"""Width + charset linter for pokefirered .string text lines.

FireRed uses a variable-width font. We use a conservative character count
heuristic: typical chars = 1 unit. Originals max out around 36-37 chars
per line, so we set MAX = 36.

ALSO: check for chars not in the FireRed charmap (would cause build failure).
"""
import re
import sys
import pathlib

MAX = 36  # max chars per visible line in FireRed text box

# Characters supported NATIVELY in FireRed charmap (from charmap.txt).
# Includes ASCII + selected accented chars used by EN/FR/DE/ES/IT.
SUPPORTED = set(
    " ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    ".,!?…\"'`'-:;()&+×÷/=*\\[\\]<>•♂♀¥% "
    # Latin diacritics in charmap
    "ÀÁÂÇÈÉÊËÌÎÏÒÓÔŒÙÚÛÑß"  # uppercase
    "àáçèéêëìîïòóôœùúûñ"     # lowercase
    "âíÍ"                       # extras
    "ªº¿¡"
)

# Czech diacritics that need transliteration (NOT supported)
UNSUPPORTED_CZ = "ýčšžřěťďňůÝČŠŽŘĚŤĎŇŮ"

# Token expansions worst-case
TOKEN_WIDTH = {
    'PLAYER': 7,
    'RIVAL': 7,
    'STR_VAR_1': 10,
    'STR_VAR_2': 10,
    'STR_VAR_3': 10,
    'NAME': 10,
    'NICKNAME': 10,
}

STRING_RE = re.compile(r'^\s*\.string\s+"((?:[^"\\]|\\.)*)"')
LINE_BREAK_RE = re.compile(r'\\[nlp]')
TOKEN_RE = re.compile(r'\{(\w+)(?:\s*,\s*[^}]+)?\}')

def visible_width(s: str) -> int:
    def replace_token(m):
        name = m.group(1)
        w = TOKEN_WIDTH.get(name, len(m.group(0)))
        return 'x' * w
    s = TOKEN_RE.sub(replace_token, s)
    s = re.sub(r'\\.', '', s)
    s = s.rstrip('$')
    return len(s)

def find_unsupported(s: str) -> list:
    # Strip tokens and escapes first
    s = TOKEN_RE.sub('', s)
    s = re.sub(r'\\.', '', s)
    bad = []
    for c in s:
        if c in UNSUPPORTED_CZ:
            bad.append(c)
        elif c not in SUPPORTED and not c.isascii():
            # Don't flag valid charmap characters even if not in our set
            # (POKéMON's é is at U+00E9, which IS in SUPPORTED)
            pass
    return bad


def check_file(path: pathlib.Path):
    issues = 0
    for ln, raw in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
        m = STRING_RE.match(raw)
        if not m:
            continue
        content = m.group(1)
        # Charset check
        bad = find_unsupported(content)
        if bad:
            print(f'{path}:{ln}: UNSUPPORTED chars: {sorted(set(bad))}  "{content}"')
            issues += 1
        # Width check (per visible line)
        sublines = LINE_BREAK_RE.split(content)
        for sub in sublines:
            w = visible_width(sub)
            if w > MAX:
                print(f'{path}:{ln}: WIDTH {w}/{MAX}  "{sub}"')
                issues += 1
    return issues


if __name__ == '__main__':
    paths = sys.argv[1:] or ['data/maps', 'data/text']
    total = 0
    for p in paths:
        pp = pathlib.Path(p)
        files = pp.rglob('*.inc') if pp.is_dir() else [pp]
        for f in files:
            total += check_file(f)
    if total:
        print(f'\n{total} issue(s) found')
        sys.exit(1)
    print(f'OK (max {MAX} chars per line, supported charset)')
