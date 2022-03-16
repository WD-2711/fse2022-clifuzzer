#!/bin/bash
DIR="$(pwd)"

echo "Downloading and compiling bison-3.8 now"
wget --no-hsts https://ftp.gnu.org/gnu/bison/bison-3.8.tar.gz
tar -zxf bison-3.8.tar.gz
mv bison-3.8 bison
echo "Bison downloaded successfully, deleting the tarball."
rm bison-3.8.tar.gz

cd bison

echo "Executing configure and creating Makefile"
# export FORCE_UNSAFE_CONFIGURE=1 # was needed when I ran this in root mode in lxd
./configure CC="afl-gcc" CFLAGS="-g --coverage -w" --quiet
# afl compilation - ./configure CC="afl-gcc" CFLAGS="-g --coverage -w" --quiet
# unset $FORCE_UNSAFE_CONFIGURE # was needed when I ran this in root mode in lxd

# "--help" and "--version" like options removed from 'bison' - "--print-localedir" & "--print-datadir".

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

# binary - ./src/bison
# man - ./doc/bison.1
# file bison [-y -t --locations -l -k -d -v]
cd $DIR
