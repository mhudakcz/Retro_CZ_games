#!/usr/bin/env python3
"""Extract Advance Wars 1 (AWRE, USA Rev 1) text -> JSON.

AW1 stores text as null-terminated ASCII, 4-byte aligned, referenced by
4-byte LE GBA pointers (0x08000000 + offset). Unlike AW2 there is almost no
free space in this ROM (only ~33 KB at 0x3F7D74), so the injector works
primarily in place; see inject.py.

Control codes: 0x0D = newline in box, 0x0E = scene/pause marker,
0x0F = end-of-box / prompt.
"""
import sys, json, os, collections

ROM = sys.argv[1] if len(sys.argv) > 1 else 'baserom.gba'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'translate/aw1_strings.json'
GBA_BASE = 0x08000000

rom = open(ROM, 'rb').read()
N = len(rom)

CTRL = (0x0D, 0x0E, 0x0F)


def is_text_byte(b):
    return 0x20 <= b < 0x7F or b in CTRL


# ---------------------------------------------------------------- pointer map
# Every 4-byte aligned word that looks like a ROM pointer.
ptrs_by_off = collections.defaultdict(list)
for i in range(0, N - 3, 4):
    val = rom[i] | (rom[i + 1] << 8) | (rom[i + 2] << 16) | (rom[i + 3] << 24)
    if GBA_BASE <= val < GBA_BASE + N:
        ptrs_by_off[val - GBA_BASE].append(i)
print('Aligned ROM-pointer words: %d to %d distinct offsets'
      % (sum(len(v) for v in ptrs_by_off.values()), len(ptrs_by_off)))


# ---------------------------------------------------------------- string scan
def read_string(off):
    """Return (raw_bytes, end_off) if a valid text string starts at off."""
    j = off
    while j < N and is_text_byte(rom[j]):
        j += 1
    if j >= N or rom[j] != 0x00:
        return None                      # not null-terminated -> not a string
    return rom[off:j], j


def slot_size(off, end):
    """Bytes available in place: string + its null + trailing 0x00 padding."""
    j = end
    while j < N and rom[j] == 0x00:
        j += 1
    return j - off


ESCAPES = {0x0D: 'r', 0x0E: 'e', 0x0F: 'f'}


def decode(raw):
    out = []
    for b in raw:
        if b in ESCAPES:
            out.append('\\' + ESCAPES[b])
        elif 0x20 <= b < 0x7F:
            out.append(chr(b))
        else:
            out.append('\\x%02X' % b)
    return ''.join(out)


def meaningful(raw):
    """At least a couple of letters - filters out control/punctuation blobs."""
    letters = sum(1 for b in raw if 0x41 <= b <= 0x5A or 0x61 <= b <= 0x7A)
    return letters >= 2


def is_string_start(off):
    """A pointer target is a string start unless it lands inside another one.

    Strings normally follow a terminator, but some sit directly behind a data
    table (0x2807B8 'Welcome to Design Maps mode!' is preceded by 0x04), so
    requiring a preceding null would miss them. A preceding *text* byte, on
    the other hand, means the pointer aims into the middle of a longer string
    - a suffix pointer, which must not become an entry of its own.
    """
    if off == 0:
        return True
    prev = rom[off - 1]
    return prev == 0x00 or not is_text_byte(prev)


entries = []
for off in sorted(ptrs_by_off):
    if not is_string_start(off):
        continue
    r = read_string(off)
    if not r:
        continue
    raw, end = r
    if len(raw) < 2 or not meaningful(raw):
        continue
    entries.append({
        'str_off': off,
        'len': len(raw),
        'slot': slot_size(off, end),
        'ptrs': ptrs_by_off[off],
        'en': decode(raw),
        'cz': '',
    })

# Real text lives in dense clusters; a lone "string" in the middle of the code
# segment is a coincidental pointer-looking word (e.g. ' pG' = thumb `bx lr`).
# Drop 64 KB buckets holding fewer than 5 hits.
bucket_count = collections.Counter(e['str_off'] >> 16 for e in entries)
dropped = [e for e in entries if bucket_count[e['str_off'] >> 16] < 5]
entries = [e for e in entries if bucket_count[e['str_off'] >> 16] >= 5]
for e in entries:
    e['region'] = '0x%02X0000' % (e['str_off'] >> 16)
print('Dropped %d false positives in sparse regions: %s'
      % (len(dropped), [d['en'][:12] for d in dropped]))

entries.sort(key=lambda e: e['str_off'])
total = sum(e['len'] for e in entries)
print('Strings referenced by pointers: %d' % len(entries))
print('Total text bytes: %d (%.1f KB)' % (total, total / 1024))
print('Total slot bytes: %.1f KB' % (sum(e['slot'] for e in entries) / 1024))
if entries:
    print('Region: 0x%06X - 0x%06X' % (entries[0]['str_off'], entries[-1]['str_off']))

os.makedirs(os.path.dirname(OUT) or '.', exist_ok=True)
json.dump(entries, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('Wrote %s' % OUT)

print('\nSample:')
for e in entries[:10]:
    print('  0x%06X [%3d/%3d] x%d %r'
          % (e['str_off'], e['len'], e['slot'], len(e['ptrs']), e['en'][:60]))
