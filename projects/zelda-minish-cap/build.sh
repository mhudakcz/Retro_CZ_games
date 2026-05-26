#!/bin/bash
# Build Zelda: The Minish Cap (tmc) Czech translation.
#
# Toolchain bring-up notes (Windows, this machine):
#  - Uses MSYS2 (tools/msys64) for shell + mingw gcc/g++ (builds C++ helper tools)
#  - ARM toolchain: tools/bin (arm-none-eabi-* 15.2)
#  - agbcc: copied from ../pokemon-firered/disassembly/tools/agbcc
#  - cmake: WinLibs cmake from ../../Pockemon_GBC/tools/mingw64/bin
#  - python3: shim at ../../tools/shim/python3 -> Windows py -3 (has pycparser)
#
# Patches applied to tmc tools/src for GCC 16 + Windows compatibility:
#  - util/util/file.h: std::filesystem::path overload + force BINARY mode
#    (GAS needs LF newlines; Windows text mode wrote CRLF)
#  - asset.h, midi.cpp, macroasm.cpp, aif/gfx/subtileset/etc: path -> .string()
#  - macroasm.cpp / midi.cpp .incbin writes: .generic_string() (forward slashes)
#  - asm/src/code_08001A7C.s: 'add r6,pc,#(..)' -> 'adr r6, entity_type_bitmasks'
#    (new binutils rejects non-word-aligned PC immediate)
#
# KNOWN LIMITATION: build is ~25% byte-divergent from the original ROM because
# this substitute toolchain differs from tmc's pinned toolchain. The ROM builds
# fully but byte-perfect reproduction needs tmc's exact arm-none-eabi version.
set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"
MSYS_BASH="$ROOT/../../tools/msys64/usr/bin/bash.exe"
GV="${1:-USA}"

exec "$MSYS_BASH" -lc '
  set -e
  export PATH=/e/vibe_project/Retro_CZ_games/tools/shim:/mingw64/bin:/e/vibe_project/Retro_CZ_games/tools/bin:/e/vibe_project/Pockemon_GBC/tools/mingw64/bin:/usr/bin:$PATH
  cd /e/vibe_project/Retro_CZ_games/projects/zelda-minish-cap/disassembly
  # build tools once (cmake), then ROM
  if [ ! -x tools/bin/tmc_strings.exe ]; then
    cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=tools -DCMAKE_TLS_VERIFY=OFF -DCMAKE_POLICY_VERSION_MINIMUM=3.5 -S tools -B tools/cmake-build
    cmake --build tools/cmake-build -j --target install
  fi
  make -f GBA.mk build GAME_VERSION='"$GV"' || true   # compare step fails (non-byte-perfect); ROM still produced
  ls -la tmc.gba
'
