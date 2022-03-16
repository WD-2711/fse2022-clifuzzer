#!/bin/bash
DIR="$(pwd)"

echo "Downloading diffutils 3.8 (for diff, cmp and sdiff) now"
wget --no-hsts https://ftp.gnu.org/gnu/diffutils/diffutils-3.8.tar.xz

tar -xf diffutils-3.8.tar.xz

mv diffutils-3.8 diffutils

echo "Diffutils downloaded successfully, deleting the tarball."
rm diffutils-3.8.tar.xz

cd diffutils
echo Executing configure and creating Makefile
# export FORCE_UNSAFE_CONFIGURE=1 # was needed when I ran this in root mode in lxd
./configure CFLAGS="-g --coverage -w" --quiet
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
