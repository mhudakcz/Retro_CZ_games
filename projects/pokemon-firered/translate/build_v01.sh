#!/bin/bash
# Aggregate + lint + build FireRed v0.1
set -e

ROOT="$(cd "$(dirname "$0")"/.. && pwd)"
DISASM="$ROOT/disassembly"
TRANS="$ROOT/translations"
ROMS="$ROOT/roms"

cd "$DISASM"

echo "=== 1. Lint all .inc files ==="
py -3 -X utf8 ../translate/width_check.py data/maps/ data/text/ 2>&1 | tail -3
echo ""

echo "=== 2. Sync translations to tracked dir ==="
bash ../translate/sync_translations.sh
echo ""

echo "=== 3. Build pokefirered_modern.gba ==="
cd "$ROOT"
bash build.sh MODERN=1 2>&1 | tail -5
echo ""

echo "=== 4. Verify + copy to roms/ ==="
SHA1=$(sha1sum "$DISASM/pokefirered_modern.gba" | awk '{print $1}')
echo "Build SHA1: $SHA1"
mkdir -p "$ROMS"
cp "$DISASM/pokefirered_modern.gba" "$ROMS/Pokemon_FIRERED_CZ_v0.1.gbc"
ls -la "$ROMS/"
