#!/bin/bash
DIR="$(pwd)"

echo "Downloading and compiling spell now"
wget --no-hsts https://ftp.gnu.org/gnu/spell/spell-1.1.tar.gz
tar -zxf spell-1.1.tar.gz
mv spell-1.1 spell
echo "Spell downloaded successfully, deleting the tarball."
rm spell-1.1.tar.gz

cd spell
echo "Executing configure and creating Makefile"
# export FORCE_UNSAFE_CONFIGURE=1 # was needed when I ran this in root mode in lxd

./configure CC="afl-gcc" CFLAGS="-g --coverage -w" LDFLAGS="--coverage" --quiet
# afl compilation - ./configure CC="afl-gcc" CFLAGS="-g --coverage -w" LDFLAGS="--coverage" --quiet

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

# binary - ./spell
# info spell.info
# file spell [-l -n -s -v -x]

cd $DIR
