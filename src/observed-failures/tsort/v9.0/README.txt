Execution commands that lead to hangs (executed from src directory) -
    "./latest-targets/coreutils/src/tsort FILE/world192.txt"  goes into an infinite loop.
    as does "./latest-targets/coreutils/src/tsort FILE/largeaudio.wav"

these inputs were gathered using the following commands -
    largeaudio.wav-
        wget -q https://filesamples.com/samples/audio/wav/sample1.wav
        mv sample1.wav FILE_backup/largeaudio.wav

    world192.txt-
        wget -q http://corpus.canterbury.ac.nz/resources/large.tar.gz
        tar -zxf large.tar.gz
        chmod 644 world192.txt
