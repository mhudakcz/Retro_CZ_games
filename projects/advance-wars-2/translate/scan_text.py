#!/usr/bin/env python3
"""Scan AW2 ROM text region."""
import sys

rom = open(sys.argv[1] if len(sys.argv) > 1 else 'disassembly/baserom.gba', 'rb').read()
start = int(sys.argv[2], 16) if len(sys.argv) > 2 else 0x090000
end = int(sys.argv[3], 16) if len(sys.argv) > 3 else 0x092000

def ascii_runs(lo, hi, min_len=4):
    runs = []
    i = lo
    while i < hi:
        j = i
        while j < hi and (0x20 <= rom[j] < 0x7F or rom[j] in (0x0A, 0x0D)):
            j += 1
        if j - i >= min_len:
            runs.append((i, rom[i:j].decode('ascii', 'replace')))
        i = max(j + 1, i + 1)
    return runs

for o, s in ascii_runs(start, end, 4):
    print(f'0x{o:06X}: {s!r}')
