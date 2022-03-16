#!/bin/bash

# Run this before executing the code files (for UT or otherwise)

DIR="$(pwd)"
OUTPUTDIR=./outputdir
if [ ! -d "$OUTPUTDIR" ]; then
    mkdir $OUTPUTDIR
else
    rm -f $OUTPUTDIR/*
fi
echo "Generating library objects!"
cd c-lib
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "linux-gnu type OS detected"
    make
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "darwin/MacOS/OSX type OS detected "
    make -f Makefile.osx
fi
echo "Generating library objects done!"
echo "Generating tests for fuzzing!"

cd -
cd tests
make clean-cov
make
cd -
cp tests/testopt FILE_backup/
if [ ! -d "FILE_backup/emptydir" ]; then
    # Control will enter here if $DIRECTORY doesn't exist.
    echo "FILE_backup/emptydir doesn't exist already, creating now"
    mkdir FILE_backup/emptydir
else
    echo "FILE_backup/emptydir already exists, nothing to create"
fi
rm -rf FILE/*

python3 generate_argfiles.py --length-level 3

echo "Downloading audio and video files"
wget -q https://upload.wikimedia.org/wikipedia/commons/b/bb/Test_ogg_mp3_48kbps.wav
mv Test_ogg_mp3_48kbps.wav FILE_backup/audio.wav

wget -q https://upload.wikimedia.org/wikipedia/commons/c/c3/%27Sauvages_de_la_Mer_Pacifique%27%2C_panels_1-10_of_woodblock_printed_wallpaper_designed_by_--Jean-Gabriel_Charvet--_and_manufacturered_by_--Joseph_Dufour--.jpg
mv "'Sauvages_de_la_Mer_Pacifique',_panels_1-10_of_woodblock_printed_wallpaper_designed_by_--Jean-Gabriel_Charvet--_and_manufacturered_by_--Joseph_Dufour--.jpg" image.jpg
mv image.jpg FILE_backup/

wget -q https://filesamples.com/samples/audio/wav/sample1.wav
mv sample1.wav FILE_backup/largeaudio.wav

# large txt file.
wget -q http://corpus.canterbury.ac.nz/resources/large.tar.gz
tar -zxf large.tar.gz
chmod 644 bible.txt E.coli world192.txt
mv bible.txt FILE_backup/
mv E.coli FILE_backup/
mv world192.txt FILE_backup/
rm large.tar.gz

cp -r FILE_backup/* FILE/
ln -s HelloWorld.py FILE/linkedfile
echo "Generating tests for fuzzing done!"

echo "Downloading and building targets!"
cd targets
./setup-all-targets.sh
cd -

cd latest-targets
./setup-all-targets.sh
cd -

cd afl-targets
./setup-all-targets.sh
cd -
echo "Downloading and building targets done!"
