#!/bin/bash
# Builds pokefirered helper tools via MSYS2.
set -e
export PATH=/mingw64/bin:/e/vibe_project/Retro_CZ_games/tools/bin:/usr/bin:$PATH
cd /e/vibe_project/Retro_CZ_games/projects/pokemon-firered/disassembly

echo "[pwd] $(pwd)"
echo "[gcc] $(gcc --version | head -1)"

for t in bin2c gbafix gbagfx preproc ramscrgen rsfont scaninc mapjson jsonproc; do
  echo "=== $t ==="
  make -C "tools/$t" CC=gcc CXX=g++ 2>&1 | tail -2
done

echo "--- built tools ---"
ls tools/*/*.exe
