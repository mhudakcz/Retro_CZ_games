#!/usr/bin/env python3
"""Check whether AW1 text blocks can be safely repacked.

The ROM has only ~33 KB of free space, far too little to relocate every
translated string the way the AW2 injector does. The alternative is to repack
each contiguous text block in place. That is only safe if, for every block:

  1. no pointer targets the *interior* of a string (code that skips a prefix
     would break when the string moves), and
  2. the block contains no text bytes that we failed to extract (data reached
     by pointer arithmetic rather than by an absolute pointer).

This script reports both, plus the byte budget of every block.
"""
import json, sys, collections

ROM = sys.argv[1] if len(sys.argv) > 1 else 'baserom.gba'
JS = sys.argv[2] if len(sys.argv) > 2 else 'translate/aw1_strings.json'
GBA_BASE = 0x08000000

rom = open(ROM, 'rb').read()
N = len(rom)
entries = json.load(open(JS, encoding='utf-8'))

# ------------------------------------------------------------------ blocks
blocks = []
cur = [entries[0]]
for e in entries[1:]:
    prev = cur[-1]
    if e['str_off'] <= prev['str_off'] + prev['slot']:
        cur.append(e)
    else:
        blocks.append(cur)
        cur = [e]
blocks.append(cur)

print('Text blocks: %d' % len(blocks))
total_span = 0
for b in blocks:
    start = b[0]['str_off']
    end = b[-1]['str_off'] + b[-1]['slot']
    span = end - start
    used = sum(e['len'] + 1 for e in b)
    total_span += span
    if len(b) >= 5:
        print('  0x%06X..0x%06X  %5d strings  span %6d  text %6d  slack %5d'
              % (start, end, len(b), span, used, span - used))
print('Total span: %d bytes (%.1f KB)' % (total_span, total_span / 1024))

# ------------------------------------------------ 1) interior pointer check
all_ptr_targets = set()
for i in range(0, N - 3, 4):
    val = rom[i] | (rom[i + 1] << 8) | (rom[i + 2] << 16) | (rom[i + 3] << 24)
    if GBA_BASE <= val < GBA_BASE + N:
        all_ptr_targets.add(val - GBA_BASE)

interior = []
for e in entries:
    for o in range(e['str_off'] + 1, e['str_off'] + e['len'] + 1):
        if o in all_ptr_targets:
            interior.append((e['str_off'], o, e['en'][:40]))
print('\n1) Pointers into the middle of a string: %d' % len(interior))
for s, o, t in interior[:15]:
    print('   string 0x%06X + %d  %r' % (s, o - s, t))

# -------------------------------------------- 2) unextracted text in blocks
covered = set()
for e in entries:
    for o in range(e['str_off'], e['str_off'] + e['slot']):
        covered.add(o)

CTRL = (0x0D, 0x0E, 0x0F)
gaps = collections.Counter()
gap_samples = []
for b in blocks:
    start = b[0]['str_off']
    end = b[-1]['str_off'] + b[-1]['slot']
    o = start
    while o < end:
        if o not in covered and (0x20 <= rom[o] < 0x7F or rom[o] in CTRL):
            j = o
            while j < end and j not in covered and rom[j] != 0:
                j += 1
            if j - o >= 3:
                gaps[start] += 1
                if len(gap_samples) < 15:
                    gap_samples.append((o, rom[o:j].decode('ascii', 'replace')))
            o = j
        else:
            o += 1
print('\n2) Uncovered text runs (>=3 bytes) inside blocks: %d' % sum(gaps.values()))
for o, s in gap_samples:
    print('   0x%06X: %r' % (o, s[:50]))
