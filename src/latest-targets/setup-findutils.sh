#!/bin/bash
DIR="$(pwd)"

echo "Downloading findutils 4.8.0 (for xargs)  now"
wget --no-hsts https://ftp.gnu.org/gnu/findutils/findutils-4.8.0.tar.xz

tar -xf findutils-4.8.0.tar.xz

mv findutils-4.8.0 findutils

echo "Diffutils downloaded successfully, deleting the tarball."
rm findutils-4.8.0.tar.xz

cd findutils
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

# xargs binary - ./xargs/xargs
# manpages - ./xargs/xargs.1

cd $DIR
