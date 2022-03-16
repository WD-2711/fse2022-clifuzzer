#!/bin/bash
DIR="$(pwd)"

echo "Downloading and compiling groff-1.22.3 (for troff-1.22.3) now"
wget --no-hsts http://git.savannah.gnu.org/cgit/groff.git/snapshot/groff-1.22.3.tar.gz
tar -zxf groff-1.22.3.tar.gz
mv groff-1.22.3 groff
echo "Groff downloaded successfully, deleting the tarball."
rm groff-1.22.3.tar.gz
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
    make src/roff/troff
    if [ $? -eq 0 ]
    then
        echo Make is successful.
    else
        echo Make is unsuccessful. Exiting now
    fi
fi

# Just the "make" command finishes with some errors about some commands not found. Hence the special make command above instead of general "make".
# binary - ./src/roff/troff/troff
# man - ./src/roff/troff/troff.man
# file troff [-a -b -c -C -E -U -z]

cd $DIR