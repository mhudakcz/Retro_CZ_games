#!/usr/bin/env python3
"""Find AW2 campaign dialogue — long English sentences."""
import sys, re

rom = open(sys.argv[1] if len(sys.argv) > 1 else 'disassembly/baserom.gba', 'rb').read()

def ascii_runs(min_len=20):
    runs = []
    i = 0
    while i < len(rom):
        j = i
        while j < len(rom) and (0x20 <= rom[j] < 0x7F or rom[j] in (0x0A,)):
            j += 1
        if j - i >= min_len:
            runs.append((i, rom[i:j].decode('ascii', 'replace')))
        i = max(j + 1, i + 1)
    return runs

runs = ascii_runs(24)
# Filter: must look like a sentence (multiple words, mostly letters/spaces/punct)
def sentence_like(s):
    letters = sum(c.isalpha() for c in s)
    spaces = s.count(' ')
    return letters > len(s) * 0.6 and spaces >= 3

dialogue = [(o, s) for o, s in runs if sentence_like(s)]
print(f'Dialogue-like runs (>=24 chars, sentence-like): {len(dialogue)}')
print(f'Address range: 0x{dialogue[0][0]:06X} - 0x{dialogue[-1][0]:06X}' if dialogue else 'none')
print()
for o, s in dialogue[:50]:
    print(f'0x{o:06X}: {s!r}')
