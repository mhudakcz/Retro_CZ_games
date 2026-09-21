#!/usr/bin/env python3
"""Inject translated Advance Wars 1 text back into the ROM.

AW1 has only ~33 KB of free space, so unlike the AW2 injector we cannot simply
append every string to the end of the ROM. Instead each contiguous text block
is repacked in place:

  * strings are rewritten back-to-back from the block start, 4-byte aligned,
    exactly the way the original ROM lays them out;
  * every pointer to a string that moved is rewritten;
  * a string that no longer fits inside its block is relocated into the free
    area at 0x3F7D74 and repointed there;
  * strings whose interior is targeted by some pointer are pinned to their
    original offset and act as block boundaries. If a translation does not fit
    a pinned slot, the English original is kept.

Run with no arguments to do a round-trip check: with no 'cz' filled the output
must be byte-identical to the input ROM.
"""
import sys, json, os, struct, collections

ROM_IN = sys.argv[1] if len(sys.argv) > 1 else 'baserom.gba'
ROM_OUT = sys.argv[2] if len(sys.argv) > 2 else 'roms/Advance_Wars_CZ.gba'
JS = 'translate/aw1_strings.json'

GBA_BASE = 0x08000000

# The stock 4 MB ROM has only ~33 KB of padding, which a Czech translation
# (roughly 10-15% longer than English) blows through. Expand the image to 8 MB
# - a stock GBA size, well inside the 32 MB cartridge window - and relocate
# overflowing strings there. EXPAND_TO = 0 keeps the original 4 MB layout.
EXPAND_TO = 0x800000
ORIG_FREE = (0x3F7D74, 0x3F7D74 + 33420)   # 33420 bytes of 0xFF padding

rom = bytearray(open(ROM_IN, 'rb').read())
ORIG_SIZE = len(rom)
if EXPAND_TO and len(rom) < EXPAND_TO:
    rom.extend(b'\xFF' * (EXPAND_TO - len(rom)))
N = len(rom)

# Free regions are consumed in order: the original padding first, then the
# expansion area.
FREE_REGIONS = [ORIG_FREE]
if EXPAND_TO and EXPAND_TO > ORIG_SIZE:
    FREE_REGIONS.append((ORIG_SIZE, EXPAND_TO))
entries = json.load(open(JS, encoding='utf-8'))

# ------------------------------------------------------------------ encoding
# v0.1 ships without diacritics (see repo README), so fold them to ASCII.
TRANSLIT = {}
for a, b in [('á', 'a'), ('é', 'e'), ('í', 'i'), ('ó', 'o'), ('ú', 'u'),
             ('ý', 'y'), ('č', 'c'), ('š', 's'), ('ž', 'z'), ('ř', 'r'),
             ('ě', 'e'), ('ť', 't'), ('ď', 'd'), ('ň', 'n'), ('ů', 'u'),
             ('Á', 'A'), ('É', 'E'), ('Í', 'I'), ('Ó', 'O'), ('Ú', 'U'),
             ('Ý', 'Y'), ('Č', 'C'), ('Š', 'S'), ('Ž', 'Z'), ('Ř', 'R'),
             ('Ě', 'E'), ('Ť', 'T'), ('Ď', 'D'), ('Ň', 'N'), ('Ů', 'U')]:
    TRANSLIT[a] = ord(b)

ESC = {'r': 0x0D, 'e': 0x0E, 'f': 0x0F, 'n': 0x0D}


def encode(s):
    out = bytearray()
    i = 0
    while i < len(s):
        c = s[i]
        if c == '\\' and i + 1 < len(s):
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


# ------------------------------------------------------------ pinned strings
# Any string whose interior is referenced by a pointer-looking word must not
# move. Recompute here so inject.py is self-contained.
ptr_targets = set()
for i in range(0, ORIG_SIZE - 3, 4):
    val = rom[i] | (rom[i + 1] << 8) | (rom[i + 2] << 16) | (rom[i + 3] << 24)
    if GBA_BASE <= val < GBA_BASE + ORIG_SIZE:
        ptr_targets.add(val - GBA_BASE)

for e in entries:
    e['pinned'] = any(o in ptr_targets
                      for o in range(e['str_off'] + 1, e['str_off'] + e['len'] + 1))
n_pinned = sum(1 for e in entries if e['pinned'])

# ------------------------------------------------------------------- blocks
entries.sort(key=lambda e: e['str_off'])
blocks = []
cur = [entries[0]]
for e in entries[1:]:
    prev = cur[-1]
    if e['str_off'] <= prev['str_off'] + prev['slot'] and not e['pinned'] \
            and not prev['pinned']:
        cur.append(e)
    else:
        blocks.append(cur)
        cur = [e]
blocks.append(cur)


def payload(e):
    """Bytes to write for this entry, with an English fallback."""
    cz = e.get('cz', '').strip()
    if cz:
        return encode(cz) + b'\x00', True
    return encode(e['en']) + b'\x00', False


# -------------------------------------------------------------------- write
n_cz = n_en = n_moved = n_relocated = n_shrunk_back = 0
repoint = {}                                  # str_off -> new offset
pinned_fallback = []      # pinned strings whose translation did not fit

free_idx = 0
free_pos = FREE_REGIONS[0][0]
free_used = 0


def alloc(size):
    """Reserve `size` bytes in the free regions, 4-byte aligned."""
    global free_idx, free_pos, free_used
    while free_idx < len(FREE_REGIONS):
        start, end = FREE_REGIONS[free_idx]
        if free_pos + size <= end:
            at = free_pos
            free_pos = (free_pos + size + 3) & ~3
            free_used += size
            return at
        free_idx += 1
        if free_idx < len(FREE_REGIONS):
            free_pos = FREE_REGIONS[free_idx][0]
    return None

for blk in blocks:
    block_start = blk[0]['str_off']
    block_end = blk[-1]['str_off'] + blk[-1]['slot']
    # Wipe the block so no tail of a longer original string survives.
    rom[block_start:block_end] = b'\x00' * (block_end - block_start)
    pos = block_start
    for e in blk:
        data, translated = payload(e)
        if e['pinned']:
            # Immovable: must fit its own slot, else keep English.
            if len(data) > e['slot']:
                data, translated = encode(e['en']) + b'\x00', False
                n_shrunk_back += 1
                pinned_fallback.append(e['str_off'])
            rom[e['str_off']:e['str_off'] + len(data)] = data
            pos = e['str_off'] + e['slot']
        else:
            # Prefer the original offset. The ROM pads strings irregularly, so
            # recomputing every offset would needlessly shift untouched text
            # (and break the round-trip check). Only slide a string forward
            # once something ahead of it has grown into its space.
            # Compare against pos, not the aligned position: a few strings sit
            # at unaligned offsets (e.g. the charset table at 0x2F0FDA) and
            # rounding up would push them out of their own block.
            if e['str_off'] >= pos and len(data) <= e['slot']:
                place = e['str_off']
            else:
                place = (pos + 3) & ~3
            if place + len(data) <= block_end:
                rom[place:place + len(data)] = data
                if place != e['str_off']:
                    repoint[e['str_off']] = place
                    n_moved += 1
                pos = place + len(data)
            else:
                # Block is full - relocate into the free area.
                at = alloc(len(data))
                if at is None:
                    print('ERROR: free space exhausted at 0x%06X' % e['str_off'])
                    sys.exit(1)
                rom[at:at + len(data)] = data
                repoint[e['str_off']] = at
                n_relocated += 1
                if os.environ.get('AW1_VERBOSE'):
                    print('  relocate 0x%06X -> 0x%06X (len %d) %r'
                          % (e['str_off'], at, len(data), e['en'][:40]))
        if translated:
            n_cz += 1
        else:
            n_en += 1

# ----------------------------------------------------------------- repoint
n_ptr = 0
for e in entries:
    if e['str_off'] in repoint:
        new = GBA_BASE + repoint[e['str_off']]
        for p in e['ptrs']:
            struct.pack_into('<I', rom, p, new)
            n_ptr += 1

# ------------------------------------------------------- header checksum
chk = 0
for i in range(0xA0, 0xBD):
    chk = (chk - rom[i]) & 0xFF
rom[0xBD] = (chk - 0x19) & 0xFF

print('Strings: %d in %d blocks (%d pinned)' % (len(entries), len(blocks), n_pinned))
print('Translated: %d   English fallback: %d' % (n_cz, n_en))
print('Moved within block: %d   relocated to free space: %d   pinned overflow: %d'
      % (n_moved, n_relocated, n_shrunk_back))
print('Pointers rewritten: %d' % n_ptr)
free_total = sum(end - start for start, end in FREE_REGIONS)
print('Free space used: %d of %d bytes (%.1f KB of %.1f KB)'
      % (free_used, free_total, free_used / 1024, free_total / 1024))
print('ROM size: %d bytes (%.1f MB)' % (N, N / 1024 / 1024))

os.makedirs(os.path.dirname(ROM_OUT) or '.', exist_ok=True)
open(ROM_OUT, 'wb').write(rom)
print('Wrote %s (%d bytes)' % (ROM_OUT, len(rom)))

# verify.py needs to know which strings intentionally kept their English text.
json.dump({'pinned_fallback': pinned_fallback},
          open('translate/inject_report.json', 'w', encoding='utf-8'), indent=1)

# Round-trip check when nothing is translated yet.
if n_cz == 0:
    orig = open(ROM_IN, 'rb').read()
    body = bytes(rom[:ORIG_SIZE])
    if body == orig:
        print('ROUND-TRIP OK: original %d bytes are byte-identical to the '
              'source ROM' % ORIG_SIZE)
    else:
        diff = [i for i in range(ORIG_SIZE) if body[i] != orig[i]]
        print('ROUND-TRIP FAILED: %d bytes differ, first at 0x%06X'
              % (len(diff), diff[0]))
        sys.exit(1)
