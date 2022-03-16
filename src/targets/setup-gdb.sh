#!/bin/bash
DIR="$(pwd)"

echo "Downloading and compiling gdb-8.1 now"
wget --no-hsts https://ftp.gnu.org/gnu/gdb/gdb-8.1.tar.gz
tar -zxf gdb-8.1.tar.gz
mv gdb-8.1 gdb
echo "Gdb downloaded successfully, deleting the tarball."
rm gdb-8.1.tar.gz

cp ./gdb-8.1.diff gdb/
cd gdb
patch -p0 < gdb-8.1.diff

echo "Executing configure and creating Makefile"
# export FORCE_UNSAFE_CONFIGURE=1 # was needed when I ran this in root mode in lxd
./configure CFLAGS="-g --coverage -w" LDFLAGS="--coverage" --quiet
# afl compilation - ./configure CC="afl-gcc" CFLAGS="-g --coverage -w" LDFLAGS="--coverage" --quiet
# unset $FORCE_UNSAFE_CONFIGURE # was needed when I ran this in root mode in lxd

# "--help" and "--version" like options removed from 'gdb' - "--configuration"


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

# binary - ./gdb/gdb
# man - ./gdb/doc/gdb.1
# stdin gdb [-write -nh -nx -quiet -batch -fullname]
cd $DIR