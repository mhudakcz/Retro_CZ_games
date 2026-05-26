#!/usr/bin/env python3
"""Map the full extent of AW2 text pointer table(s)."""
import sys, struct

rom = open(sys.argv[1] if len(sys.argv) > 1 else 'disassembly/baserom.gba', 'rb').read()
N = len(rom)

def is_text_ptr(val):
    if not (0x08000000 <= val < 0x08000000 + N):
        return False
    o = val - 0x08000000
    # Points to printable ASCII or control code?
    b = rom[o]
    return 0x0A <= b < 0x7F or b in (0x0D, 0x0E, 0x0F)

# Find contiguous runs of text pointers (each 4 bytes aligned)
runs = []
i = 0
cur_start = None
cur_count = 0
while i + 4 <= N:
    val = struct.unpack('<I', rom[i:i+4])[0]
    if is_text_ptr(val):
        if cur_start is None:
            cur_start = i
            cur_count = 0
        cur_count += 1
        i += 4
    else:
        if cur_start is not None and cur_count >= 8:
            runs.append((cur_start, cur_count))
        cur_start = None
        cur_count = 0
        i += 4

print(f'Pointer-table runs (>=8 consecutive text pointers): {len(runs)}')
total = 0
big = [r for r in runs if r[1] >= 20]
print(f'Large tables (>=20 pointers): {len(big)}')
for start, count in sorted(big, key=lambda x: -x[1])[:25]:
    total += count
    # sample first string
    val = struct.unpack('<I', rom[start:start+4])[0]
    o = val - 0x08000000
    s = rom[o:o+40].split(b'\0')[0].decode('ascii', 'replace')
    print(f'  0x{start:06X}: {count:4d} ptrs  first-> {s!r}')

allcount = sum(c for _, c in runs)
print(f'\nTotal pointers across all runs: {allcount}')
