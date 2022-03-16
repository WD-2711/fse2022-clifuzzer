#!/bin/bash
DIR="$(pwd)"

echo "Downloading and compiling all targets"

./setup-bc.sh
./setup-binutils.sh
./setup-bison.sh
./setup-coreutils.sh
./setup-gdb.sh
# spell "configure" doesn't really work with the correct FLAGS. it errors out.
# run configure normally in the spell directory downloaded by this script
# Then manually change the flags in the generated makefiles and (copy from
# setup-spell.sh) and run make again.
./setup-spell.sh
. ./setup-troff.sh
