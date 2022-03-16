#!/bin/bash
DIR="$(pwd)"

echo "Downloading and compiling bison-3.0.4 now"
wget --no-hsts https://ftp.gnu.org/gnu/bison/bison-3.0.4.tar.gz
tar -zxf bison-3.0.4.tar.gz
mv bison-3.0.4 bison
echo "Bison downloaded successfully, deleting the tarball."
rm bison-3.0.4.tar.gz

cp ./bison-3.0.4.diff bison/
cd bison
patch -p0 < bison-3.0.4.diff

echo "Executing configure and creating Makefile"
# export FORCE_UNSAFE_CONFIGURE=1 # was needed when I ran this in root mode in lxd
./configure CFLAGS="-g --coverage -w" --quiet
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