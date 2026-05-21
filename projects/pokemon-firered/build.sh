#!/bin/bash
# Build pokefirered.gba via MSYS2 mingw64 + ARM toolchain.
# Run from anywhere — wrapper invokes msys2 bash.
set -e

ROOT="$(cd "$(dirname "$0")" && pwd)"
MSYS_BASH="$ROOT/../../tools/msys64/usr/bin/bash.exe"

# Build the inner command. Don't use $ROOT here — we're crossing shells.
exec "$MSYS_BASH" -lc '
  set -e
  export PATH=/mingw64/bin:/e/vibe_project/Retro_CZ_games/tools/bin:/usr/bin:$PATH
  cd /e/vibe_project/Retro_CZ_games/projects/pokemon-firered/disassembly
  echo "[firered build] gcc=$(which gcc)"
  echo "[firered build] arm-gcc=$(which arm-none-eabi-gcc)"
  echo "[firered build] make=$(which make)"
  make CC=gcc CXX=g++ '"$*"'
'
