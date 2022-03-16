#!/bin/bash
DIR="$(pwd)"

echo "Downloading coreutils-9.0 now"
wget --no-hsts https://ftp.gnu.org/gnu/coreutils/coreutils-9.0.tar.gz

tar -zxf coreutils-9.0.tar.gz

mv coreutils-9.0 coreutils

echo "Coreutils downloaded successfully, deleting the tarball."
rm coreutils-9.0.tar.gz

cd coreutils
echo Executing configure and creating Makefile
# export FORCE_UNSAFE_CONFIGURE=1 # was needed when I ran this in root mode in lxd
./configure CC="afl-gcc" CFLAGS="-g --coverage -w" --quiet
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

# binaries - ./src/
# manpages - ./man/

cd $DIR
