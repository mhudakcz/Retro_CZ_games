#!/usr/bin/env python3
"""Report translation progress per chunk, plus line-width violations."""
import json, glob, re

BS = chr(92)
SPLIT = re.compile(re.escape(BS) + r'(?:r|e|f|x[0-9A-Fa-f]{2})')
MAX_LINE = 40

done = total_chunks = 0
all_filled = all_total = 0
wide = []
for path in sorted(glob.glob('translate/chunks/chunk_*.json')):
    total_chunks += 1
    chunk = json.load(open(path, encoding='utf-8'))
    filled = sum(1 for e in chunk if e.get('cz', '').strip())
    all_filled += filled
    all_total += len(chunk)
    for e in chunk:
        for line in SPLIT.split(e.get('cz', '')):
            if len(line) > MAX_LINE:
                wide.append((e['idx'], len(line), line))
    pct = filled * 100 // max(len(chunk), 1)
    if pct == 100:
        done += 1
    print('%s: %4d/%4d (%3d%%)' % (path, filled, len(chunk), pct))

print('CHUNKS_DONE=%d/%d  STRINGS=%d/%d (%.1f%%)'
      % (done, total_chunks, all_filled, all_total,
         100.0 * all_filled / max(all_total, 1)))
if wide:
    print('\nLines over %d chars: %d' % (MAX_LINE, len(wide)))
    for idx, n, line in sorted(wide, key=lambda x: -x[1])[:15]:
        print('  idx %5d  %3d  %r' % (idx, n, line[:60]))
