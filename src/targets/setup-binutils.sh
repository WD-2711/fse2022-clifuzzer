#!/bin/bash
DIR="$(pwd)"

echo "Downloading and compiling binutils-2.30 (for as 2.30) now"
wget --no-hsts  https://ftp.gnu.org/gnu/binutils/binutils-2.30.tar.gz
tar -zxf binutils-2.30.tar.gz
mv binutils-2.30 binutils
echo "Binutils downloaded successfully, deleting the tarball."
rm binutils-2.30.tar.gz

cd binutils
echo "Executing configure and creating Makefile"
# export FORCE_UNSAFE_CONFIGURE=1 # was needed when I ran this in root mode in lxd
./configure CFLAGS="-g --coverage -w" --quiet
# afl compilation - ./configure CC="afl-gcc" CFLAGS="-g --coverage -w" --quiet
# unset $FORCE_UNSAFE_CONFIGURE # was needed when I ran this in root mode in lxd

# "--help" and "--version" like options removed from 'as' - "--dump-config" & "--target-help".

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

# binary -  ./gas/as-new
# man - ./gas/doc/as.1
# stdin as [-a -D -L -R -v -W -Z -w -x]
cd $DIR