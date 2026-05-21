#!/bin/bash
# Build pret/agbcc and install into pokefirered disassembly.
set -e
export PATH=/mingw64/bin:/e/vibe_project/Retro_CZ_games/tools/bin:/usr/bin:$PATH
cd /e/vibe_project/Retro_CZ_games/projects/pokemon-firered/agbcc

echo "[agbcc] building..."
./build.sh
echo "[agbcc] installing into ../disassembly/tools/agbcc..."
./install.sh ../disassembly
echo "[agbcc] done."
ls ../disassembly/tools/agbcc/bin/
