#!/bin/bash
# Build Advance Wars 2: Black Hole Rising via MSYS2 + ARM toolchain + agbcc.
set -e

ROOT="$(cd "$(dirname "$0")" && pwd)"
MSYS_BASH="$ROOT/../../tools/msys64/usr/bin/bash.exe"

exec "$MSYS_BASH" -lc '
  set -e
  export PATH=/mingw64/bin:/e/vibe_project/Retro_CZ_games/tools/bin:/usr/bin:$PATH
  # AW2 Makefile uses DEVKITARM env to find arm-none-eabi-* tools.
  # Point it at our portable ARM toolchain root (parent of bin/).
  export DEVKITARM=/e/vibe_project/Retro_CZ_games/tools
  cd /e/vibe_project/Retro_CZ_games/projects/advance-wars-2/disassembly
  echo "[aw2 build] gcc=$(which gcc)  arm-as=$(which arm-none-eabi-as)  make=$(which make)"
  make CC=gcc CXX=g++ '"$*"'
'
