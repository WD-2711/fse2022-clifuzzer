This directory contains scripts to download and compile utilities for fuzzing.
The scripts contain general details about the utilities.
As of writing this, the scripts download the latest versions of those utilities for the purpose of fuzzing.

A general overview of the utilities that are compiled, their grammars generated and fuzzed -

setup-all-targets.sh -> runs all the scripts, downloading and compiling everything.

setup-bc.sh -> downloads bc-1.07.1 (for bc-1.07.1 and dc-1.4.1(dc reported failure)) and compiles them.

setup-binutils.sh -> downloads binutils-2.37 (for as, nm, strings, strip 2.37(as reported failure)) and compiles them.

setup-bison.sh -> downloads bison-3.8 (for bison (bison reported failures)) and compiles them.

setup-coreutils.sh -> downloads coreutils-8.32 (for about 21 utilities - cut head cat expand fold join nl uniq comm fmt paste pr ptx tac tsort unexpand wc sort od tee tail, of which ptx, tac, tsort and tee have reported failures) and compiles them.

setup-diffutils.sh -> downloads diffutils-3.8 (for diff, cmp and sdiff) and compiles them.

setup-findutils.sh -> downloads findutils-4.8.0 (for xargs) and compiles them.

setup-gdb.sh -> downloads gdb-11.1 (for gdb which reported failure) and compiles them.

setup-grep.sh -> downloads grep-3.7 (for grep) and compiles it.

setup-m4.sh -> downloads m4-1.4.19 (for m4) and compiles it.
setup-spell.sh -> downloads spell-1.1 (for spell which reported failure) and compiles it.

setup-troff.sh -> downloads groff-1.22.4 (for troff-1.22.4 which reported failure) and compiles them. There are other fuzzable utilities in this package but they are written in c++ and name mangling of getopt, open etc makes programmatic construction of grammar impossible. troff's grammar was manually constructed during the attempt to recreate its failure.

setup-util-linux.sh -> downloads util-linux-2.37.2 (for col, colcrt, colrm, column, rev and look) and compiles them.
column is located in util-linux/.libs/column (and not util-linux/column which is actually a Bash-script wrapper around the column executable)
