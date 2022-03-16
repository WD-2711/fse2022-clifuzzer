#!/bin/bash
DIR="$(pwd)"

echo "Downloading and compiling m4 1.4.19 now"
wget --no-hsts https://ftp.gnu.org/gnu/m4/m4-1.4.19.tar.xz
tar -xf m4-1.4.19.tar.xz
mv m4-1.4.19  m4
echo "m4 downloaded successfully, deleting the tarball."
rm m4-1.4.19.tar.xz

cd m4
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

# binary - ./src/m4
# man - ./doc/m4.1

cd $DIR
