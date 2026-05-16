#!/usr/bin/env bash
# Build wrapper for pokefirered (GBA disassembly).
# Sets PATH for ARM toolchain + host gcc + GNU make (all from the Yellow project + this project's tools/).
set -e

ROOT="$(cd "$(dirname "$0")" && pwd)"
ARM_BIN="$ROOT/../../tools/bin"
HOST_GCC="$ROOT/../../../Pockemon_GBC/tools/mingw64/bin"
MAKE_BIN="$ROOT/../../../Pockemon_GBC/tools/make-bin"

export PATH="$ARM_BIN:$HOST_GCC:$MAKE_BIN:$PATH"

cd "$ROOT/disassembly"
echo "[firered build] Tools:"
echo "  arm-gcc : $(which arm-none-eabi-gcc)"
echo "  host gcc: $(which gcc)"
echo "  make    : $(which make)"
echo

exec make "$@"
