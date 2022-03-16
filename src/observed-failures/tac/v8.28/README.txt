Execution commands that lead to hangs (executed from src directory) -
    "./targets/coreutils/src/tac -s .+5 -r FILE/E.coli" (the value to '-s' option needs to be of the form '.+<int>' and both option are required)

E.coli is gathered by -
    wget -q http://corpus.canterbury.ac.nz/resources/large.tar.gz
    tar -zxf large.tar.gz
    chmod 644 E.coli
