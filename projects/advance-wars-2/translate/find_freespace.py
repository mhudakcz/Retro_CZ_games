#!/usr/bin/env python3
"""Find free space (long runs of 0x00 or 0xFF) in AW2 ROM for relocated text."""
import sys

rom = open(sys.argv[1] if len(sys.argv) > 1 else 'disassembly/baserom.gba', 'rb').read()
N = len(rom)
print(f'ROM size: {N} bytes (0x{N:X})')

# Find runs of identical padding byte >= 256
def find_pad(byte, min_len=1024):
    runs = []
    i = 0
    while i < N:
        if rom[i] == byte:
            j = i
            while j < N and rom[j] == byte:
                j += 1
            if j - i >= min_len:
                runs.append((i, j - i))
            i = j
        else:
            i += 1
    return runs

for b in (0x00, 0xFF):
    runs = find_pad(b, 4096)
    total = sum(l for _, l in runs)
    print(f'\nByte 0x{b:02X}: {len(runs)} runs >=4KB, total {total} bytes ({total/1024:.0f} KB)')
    for off, length in sorted(runs, key=lambda x: -x[1])[:8]:
        print(f'  0x{off:06X}: {length} bytes ({length/1024:.0f} KB)')
