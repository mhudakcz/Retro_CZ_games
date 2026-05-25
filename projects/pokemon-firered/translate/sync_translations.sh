#!/bin/bash
# Sync translated .inc files from disassembly/ (gitignored) into
# translations/ (tracked) so they survive disassembly re-clones and
# can be committed.
set -e

ROOT="$(cd "$(dirname "$0")"/.. && pwd)"
SRC="$ROOT/disassembly"
DST="$ROOT/translations"

mkdir -p "$DST/data/maps" "$DST/data/text"

# Maps with text.inc
count=0
for f in "$SRC"/data/maps/*/text.inc; do
  [ -e "$f" ] || continue
  rel="${f#$SRC/}"
  mkdir -p "$DST/$(dirname "$rel")"
  cp "$f" "$DST/$rel"
  count=$((count+1))
done
echo "Synced $count map text.inc files"

# data/text/*.inc
count=0
for f in "$SRC"/data/text/*.inc; do
  [ -e "$f" ] || continue
  rel="${f#$SRC/}"
  cp "$f" "$DST/$rel"
  count=$((count+1))
done
echo "Synced $count data/text/ .inc files"

# Charmap (reference)
cp "$SRC/charmap.txt" "$DST/charmap.txt" 2>/dev/null || true

echo "Done. Tracked under: $DST"
