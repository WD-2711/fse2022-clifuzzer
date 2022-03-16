#!/bin/bash
DIR="$(pwd)"

echo "Downloading and compiling groff-1.22.4 (for troff-1.22.4) now"
# since all utilities in groff are written in cpp and name mangling changes 
# getopt to something else, extracting the grammars programmatically is not straigtforward
# so, troff is fuzzed to recreate the failure but other utilities such as 
# eqn, neqn, groff, pic, soelim, tbl and ul are not fuzzed (they were in Miller's 2020 paper)
wget --no-hsts https://ftp.gnu.org/gnu/groff/groff-1.22.4.tar.gz
tar -zxf groff-1.22.4.tar.gz
mv groff-1.22.4 groff
echo "Groff downloaded successfully, deleting the tarball."
rm groff-1.22.4.tar.gz
export GROFF_FONT_PATH=/usr/share/groff/1.22.4/font/

cd groff
echo "Executing configure and creating Makefile"
# export FORCE_UNSAFE_CONFIGURE=1 # was needed when I ran this in root mode in lxd

./configure CFLAGS="-g --coverage -w" LDFLAGS="--coverage" CPPFLAGS="-g --coverage -w" --quiet
# afl compilation - ./configure CC="afl-gcc" CXX="afl-g++" CFLAGS="-g --coverage -w" LDFLAGS="--coverage" CPPFLAGS="-g --coverage -w" --quiet
# remember to export GROFF_FONT_PATH=/usr/share/groff/1.22.4/font/ otherwise the running won't work.

# unset $FORCE_UNSAFE_CONFIGURE # was needed when I ran this in root mode in lxd
if [ $? -eq 0 ] && [ -s Makefile ]
then
    echo Configure was successful. Attempting to make.
    make 
    if [ $? -eq 0 ]
    then
        echo Make is successful.
    else
        echo Make is unsuccessful. Exiting now
    fi
fi

# binary - ./troff
# man - ./src/roff/troff/troff.1.man

cd $DIR
