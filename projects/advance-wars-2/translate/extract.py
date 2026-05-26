#!/usr/bin/env python3
"""Extract AW2 text from known pointer tables → JSON.

Text tables live in the 0x61xxxx region. Each is a run of 4-byte LE GBA
pointers (0x08000000 + offset) to null-terminated ASCII strings.
Control codes: \\r (0x0D)=newline, 0x0E/0x0F = pause/prompt markers.
"""
import sys, struct, json

rom = open(sys.argv[1] if len(sys.argv) > 1 else 'disassembly/baserom.gba', 'rb').read()
N = len(rom)

# Known good text tables (start_offset, count) from map_table.py — 0x61xxxx region
TABLES = [
    (0x610A38, 2310),  # main campaign script
    (0x6131B4, 51),    # game modes (Fog of War...)
    (0x61328C, 21),
    (0x612EE4, 179),   # UI (Out...)
    (0x6132E4, 416),   # Field Training / tutorial
    (0x613B48, 21),    # tutorial movement
    (0x613BBC, 147),   # tutorial hints
]

def read_cstr(off):
    end = rom.index(0, off)
    return rom[off:end], end

def decode(raw):
    # Represent control codes readably for translators
    out = []
    for b in raw:
        if b == 0x0D:
            out.append('\\r')      # newline within a box
        elif b == 0x0E:
            out.append('\\e')      # marker (often scene/cmd)
        elif b == 0x0F:
            out.append('\\f')      # prompt / end-of-box
        elif 0x20 <= b < 0x7F:
            out.append(chr(b))
        else:
            out.append(f'\\x{b:02X}')
    return ''.join(out)

entries = []
seen_offsets = set()
for tbl_start, count in TABLES:
    for i in range(count):
        ptr_loc = tbl_start + i*4
        val = struct.unpack('<I', rom[ptr_loc:ptr_loc+4])[0]
        if not (0x08000000 <= val < 0x08000000 + N):
            continue
        str_off = val - 0x08000000
        raw, end = read_cstr(str_off)
        entries.append({
            'table': f'0x{tbl_start:06X}',
            'ptr_loc': ptr_loc,
            'str_off': str_off,
            'len': len(raw),
            'en': decode(raw),
            'cz': '',  # to be filled by translation
        })
        seen_offsets.add(str_off)

print(f'Extracted {len(entries)} strings from {len(TABLES)} tables')
total_bytes = sum(e['len'] for e in entries)
print(f'Total text bytes: {total_bytes} ({total_bytes/1024:.1f} KB)')

# Dedup note: some pointers may reference same string
uniq = len(seen_offsets)
print(f'Unique string offsets: {uniq}')

with open('translate/aw2_strings.json', 'w', encoding='utf-8') as f:
    json.dump(entries, f, ensure_ascii=False, indent=1)
print('Wrote translate/aw2_strings.json')

# Sample
print('\nSample (campaign):')
for e in entries[:8]:
    print(f"  [{e['len']:3d}] {e['en'][:70]!r}")
