#!/bin/bash
DIR="$(pwd)"

echo "Downloading and compiling grep 3.7 now"
wget --no-hsts https://ftp.gnu.org/gnu/grep/grep-3.7.tar.xz
tar -xf grep-3.7.tar.xz
mv grep-3.7  grep
echo "grep downloaded successfully, deleting the tarball."
rm grep-3.7.tar.xz

cd grep
echo "Executing configure and creating Makefile"
# export FORCE_UNSAFE_CONFIGURE=1 # was needed when I ran this in root mode in lxd
./configure CFLAGS="-g --coverage -w" --quiet
# afl compilation - ./configure CC="afl-gcc" CFLAGS="-g --coverage -w" --quiet
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

# binary - ./src/grep
# man - ./doc/grep.1

cd $DIR
