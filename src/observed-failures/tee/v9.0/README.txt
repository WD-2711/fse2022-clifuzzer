Execution commands that lead to hangs (executed from src directory) -
    "./latest-targets/coreutils/src/tee -a FILE/README < FILE/README" goes into an infinite loop. Basically any non empty file appended to itself

README is the README file of the FILE directory
