#!/usr/bin/env python3
"""Inject translated AW2 text: relocate strings to free space + repoint.

Reads aw2_strings.json (with 'cz' filled). For each entry:
  - encode cz (or fall back to en) back to bytes
  - write to free region (0x617EE4+), 1-byte aligned, null-terminated
  - rewrite the 4-byte pointer at ptr_loc to 0x08000000 + new_off

Then fix GBA header complement checksum. Output patched ROM.
"""
import sys, struct, json

ROM_IN  = sys.argv[1] if len(sys.argv) > 1 else 'disassembly/baserom.gba'
ROM_OUT = sys.argv[2] if len(sys.argv) > 2 else 'roms/Advance_Wars_2_CZ.gba'
JSON_IN = 'translate/aw2_strings.json'

FREE_START = 0x617EE4   # 1.95 MB of 0xFF padding here
GBA_BASE   = 0x08000000

rom = bytearray(open(ROM_IN, 'rb').read())
entries = json.load(open(JSON_IN, encoding='utf-8'))

def encode(s):
    """Reverse of extract.decode(). Handles \\r \\e \\f \\xNN escapes."""
    out = bytearray()
    i = 0
    while i < len(s):
        c = s[i]
        if c == '\\' and i+1 < len(s):
            n = s[i+1]
            if n == 'r': out.append(0x0D); i += 2; continue
            if n == 'e': out.append(0x0E); i += 2; continue
            if n == 'f': out.append(0x0F); i += 2; continue
            if n == 'n': out.append(0x0D); i += 2; continue  # tolerate \n as newline
            if n == 'x' and i+3 < len(s):
                out.append(int(s[i+2:i+4], 16)); i += 4; continue
            out.append(ord(c)); i += 1; continue
        # Map any non-ASCII (e.g. accidental Czech diacritics) to ASCII fallback
        o = ord(c)
        if o < 0x80:
            out.append(o)
        else:
            out.append(TRANSLIT.get(c, ord('?')))
        i += 1
    return bytes(out)

# ASCII fallback for Czech diacritics (v0.1 = no diacritics)
TRANSLIT = {}
for a, b in [('á','a'),('é','e'),('í','i'),('ó','o'),('ú','u'),('ý','y'),
             ('č','c'),('š','s'),('ž','z'),('ř','r'),('ě','e'),('ť','t'),
             ('ď','d'),('ň','n'),('ů','u'),
             ('Á','A'),('É','E'),('Í','I'),('Ó','O'),('Ú','U'),('Ý','Y'),
             ('Č','C'),('Š','S'),('Ž','Z'),('Ř','R'),('Ě','E'),('Ť','T'),
             ('Ď','D'),('Ň','N'),('Ů','U')]:
    TRANSLIT[a] = ord(b)

write_pos = FREE_START
n_translated = 0
n_fallback = 0
for e in entries:
    text = e['cz'].strip() if e['cz'].strip() else e['en']
    if e['cz'].strip():
        n_translated += 1
    else:
        n_fallback += 1
    data = encode(text) + b'\x00'
    # write
    rom[write_pos:write_pos+len(data)] = data
    new_off = write_pos
    write_pos += len(data)
    # repoint
    struct.pack_into('<I', rom, e['ptr_loc'], GBA_BASE + new_off)

used = write_pos - FREE_START
print(f'Entries: {len(entries)}  translated: {n_translated}  fallback(EN): {n_fallback}')
print(f'Free space used: {used} bytes ({used/1024:.1f} KB) of {len(rom)-FREE_START} available')
if write_pos > len(rom):
    print('ERROR: overflowed ROM!'); sys.exit(1)

# Fix GBA header complement check (byte 0xBD): sum bytes 0xA0..0xBC
chk = 0
for i in range(0xA0, 0xBD):
    chk = (chk - rom[i]) & 0xFF
chk = (chk - 0x19) & 0xFF
rom[0xBD] = chk

import os
os.makedirs(os.path.dirname(ROM_OUT), exist_ok=True)
open(ROM_OUT, 'wb').write(rom)
print(f'Wrote {ROM_OUT} ({len(rom)} bytes)')
