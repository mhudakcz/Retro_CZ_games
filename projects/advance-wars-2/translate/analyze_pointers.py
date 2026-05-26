#!/usr/bin/env python3
"""Analyze AW2 text: are strings null-terminated? Find pointers (0x08xxxxxx)."""
import sys, struct

rom = open(sys.argv[1] if len(sys.argv) > 1 else 'disassembly/baserom.gba', 'rb').read()

# Check a known dialogue string at 0x5D9328
off = 0x5D9328
print(f'Bytes around 0x{off:06X}:')
print('  before:', rom[off-4:off].hex())
chunk = rom[off:off+60]
print('  text  :', repr(chunk.decode('ascii', 'replace')))
# Find the terminator
end = rom.index(0, off)
print(f'  string 0x{off:06X}..0x{end:06X} len={end-off}, terminator=0x{rom[end]:02X}')

# Build a set of all 4-byte little-endian pointers that point into ROM (0x08000000..0x09FFFFFF)
print('\nSearching for pointer to 0x{:06X} (= GBA addr 0x{:08X})...'.format(off, 0x08000000+off))
target = struct.pack('<I', 0x08000000 + off)
idx = 0
found = []
while True:
    p = rom.find(target, idx)
    if p < 0:
        break
    found.append(p)
    idx = p + 1
print(f'  pointer bytes {target.hex()} found at: {[hex(x) for x in found]}')

# Look at the pointer table region — dump a few pointers around the first hit
if found:
    pt = found[0]
    base = pt - (pt % 4)
    print(f'\nPointer table around 0x{base:06X}:')
    for i in range(base-16, base+40, 4):
        val = struct.unpack('<I', rom[i:i+4])[0]
        marker = ' <==' if i == pt else ''
        tgt = ''
        if 0x08000000 <= val < 0x0A000000:
            o = val - 0x08000000
            if o < len(rom):
                s = rom[o:o+30].split(b'\0')[0].decode('ascii', 'replace')
                tgt = f'  -> 0x{o:06X}: {s!r}'
        print(f'  0x{i:06X}: {val:08X}{tgt}{marker}')
