Both commands below lead to crashes with different return codes (executed from src directory) -
    "./latest-targets/util-linux/.libs/column FILE/testopt FILE/largeaudio.wav" -> returns -11 (or 139)
    "./latest-targets/util-linux/.libs/column FILE/E.coli FILE/image.jpg" -> returns -6 (or 134)

these inputs were gathered using the following commands -
    testopt - 
        "testopt" is the executable of the "testopt.c" program in the "tests" directory.(Also added in this directory. Compile as "gcc -g --coverage -o testopt testopt.c"
        
    image.jpg-
        wget -q https://upload.wikimedia.org/wikipedia/commons/c/c3/%27Sauvages_de_la_Mer_Pacifique%27%2C_panels_1-10_of_woodblock_printed_wallpaper_designed_by_--Jean-Gabriel_Charvet--_and_manufacturered_by_--Joseph_Dufour--.jpg
        mv "'Sauvages_de_la_Mer_Pacifique',_panels_1-10_of_woodblock_printed_wallpaper_designed_by_--Jean-Gabriel_Charvet--_and_manufacturered_by_--Joseph_Dufour--.jpg" image.jpg

    largeaudio.wav-
        wget -q https://filesamples.com/samples/audio/wav/sample1.wav
        mv sample1.wav FILE_backup/largeaudio.wav

    E.coli-
        wget -q http://corpus.canterbury.ac.nz/resources/large.tar.gz
        tar -zxf large.tar.gz
        chmod 644 E.coli
