#!/bin/bash
DIR="$(pwd)"

echo "Downloading and compiling all targets"

./setup-bc.sh
./setup-binutils.sh
./setup-bison.sh
./setup-coreutils.sh
./setup-diffutils.sh
./setup-findutils.sh
./setup-gdb.sh
./setup-grep.sh
./setup-m4.sh
./setup-spell.sh
./setup-util-linux.sh
. ./setup-troff.sh
