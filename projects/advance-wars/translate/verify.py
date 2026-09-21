#!/usr/bin/env python3
"""End-to-end check of a built ROM.

Walks every pointer recorded during extraction, reads the string it now points
at in the patched ROM, and compares it against what the injector was supposed
to write. Catches repointing mistakes that the round-trip test cannot see,
because the round-trip moves nothing.

    py -3 translate/verify.py roms/Advance_Wars_CZ_v0.1.gba
"""
import sys, json

ROM = sys.argv[1] if len(sys.argv) > 1 else 'roms/Advance_Wars_CZ_v0.1.gba'
GBA_BASE = 0x08000000

rom = open(ROM, 'rb').read()
N = len(rom)
entries = json.load(open('translate/aw1_strings.json', encoding='utf-8'))

TRANSLIT = {}
for a, b in [('á', 'a'), ('é', 'e'), ('í', 'i'), ('ó', 'o'), ('ú', 'u'),
             ('ý', 'y'), ('č', 'c'), ('š', 's'), ('ž', 'z'), ('ř', 'r'),
             ('ě', 'e'), ('ť', 't'), ('ď', 'd'), ('ň', 'n'), ('ů', 'u'),
             ('Á', 'A'), ('É', 'E'), ('Í', 'I'), ('Ó', 'O'), ('Ú', 'U'),
             ('Ý', 'Y'), ('Č', 'C'), ('Š', 'S'), ('Ž', 'Z'), ('Ř', 'R'),
             ('Ě', 'E'), ('Ť', 'T'), ('Ď', 'D'), ('Ň', 'N'), ('Ů', 'U')]:
    TRANSLIT[a] = ord(b)

ESC = {'r': 0x0D, 'e': 0x0E, 'f': 0x0F, 'n': 0x0D}
BS = chr(92)


def encode(s):
    out = bytearray()
    i = 0
    while i < len(s):
        c = s[i]
        if c == BS and i + 1 < len(s):
            n = s[i + 1]
            if n in ESC:
                out.append(ESC[n])
                i += 2
                continue
            if n == 'x' and i + 3 < len(s):
                out.append(int(s[i + 2:i + 4], 16))
                i += 4
                continue
        o = ord(c)
        out.append(o if o < 0x80 else TRANSLIT.get(c, ord('?')))
        i += 1
    return bytes(out)


checked = bad = 0
examples = []
for e in entries:
    cz = e.get('cz', '').strip()
    want = encode(cz if cz else e['en'])
    for p in e['ptrs']:
        if p + 4 > N:
            continue
        val = rom[p] | (rom[p + 1] << 8) | (rom[p + 2] << 16) | (rom[p + 3] << 24)
        if not (GBA_BASE <= val < GBA_BASE + N):
            continue
        off = val - GBA_BASE
        end = rom.find(b'\x00', off)
        got = rom[off:end]
        checked += 1
        if got != want:
            bad += 1
            if len(examples) < 10:
                examples.append((e['str_off'], p, want[:50], got[:50]))

print('Pointers checked: %d' % checked)
print('Mismatches: %d' % bad)
for str_off, p, want, got in examples:
    print('  string 0x%06X via ptr 0x%06X' % (str_off, p))
    print('    want: %r' % want)
    print('    got : %r' % got)

n_cz = sum(1 for e in entries if e.get('cz', '').strip())
print('\nTranslated strings in ROM: %d / %d (%.1f%%)'
      % (n_cz, len(entries), 100.0 * n_cz / len(entries)))
sys.exit(1 if bad else 0)
