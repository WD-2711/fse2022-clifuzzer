A lot of files lead to crashes for this version of bison. All of them use the option "--trace".
So add any of these files ['s1', 's4', 's10', 's15', 's17', 's18', 's22', 's24', 's29', 'l4', 'l6', 'l8', 'l11', 'l12', 'l13', 'l16', 'l18', 'l20', 'l21', 'l29'] 
to the end of command below (from the src directory) and it will crash -
    "./latest-targets/bison/src/bison --trace observed-failures/bison/v3.8/"
