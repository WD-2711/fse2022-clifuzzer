#!/bin/bash
DIR="$(pwd)"

echo "Downloading util-linux 2.37.2 (for col, colcrt, colrm, column, rev and look) now"
wget --no-hsts https://mirrors.edge.kernel.org/pub/linux/utils/util-linux/v2.37/util-linux-2.37.2.tar.xz

tar -xf util-linux-2.37.2.tar.xz

mv util-linux-2.37.2 util-linux

echo "util-linux downloaded successfully, deleting the tarball."
rm util-linux-2.37.2.tar.xz

cd util-linux
echo Executing configure and creating Makefile
# export FORCE_UNSAFE_CONFIGURE=1 # was needed when I ran this in root mode in lxd
./configure CFLAGS="-g --coverage -w" --quiet
# unset $FORCE_UNSAFE_CONFIGURE # was needed when I ran this in root mode in lxd
if [ $? -eq 0 ] && [ -s Makefile ]
then
   echo Configure was successful. Attempting to make.
   make colrm colcrt col column rev look
   if [ $? -eq 0 ]
   then
       echo Make is successful.
   else
       echo Make is unsuccessful. Exiting now
   fi
fi

# binaries - ./, except for column which is ./.libs/column and not ./column
# manpages - ./text-utils/, ./misc-utils/look.1

cd $DIR
