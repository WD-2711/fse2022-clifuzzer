#!/bin/bash
DIR="$(pwd)"

echo "Downloading and compiling bc-1.07.1 (for dc-1.4.1) now"
wget --no-hsts  https://ftp.gnu.org/gnu/bc/bc-1.07.1.tar.gz
tar -zxf bc-1.07.1.tar.gz
mv bc-1.07.1 bc
echo "Bc downloaded successfully, deleting the tarball."
rm bc-1.07.1.tar.gz

cd bc
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

# binary - ./dc/dc
# man - ./doc/dc.1
# stdin dc
cd $DIR