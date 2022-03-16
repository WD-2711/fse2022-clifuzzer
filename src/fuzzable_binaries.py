all_fuzzable_binaries = {
 'as': './latest-targets/binutils/gas/as-new', # -> found bugs in
 'bc': './latest-targets/bc/bc/bc',
 'bison': './latest-targets/bison/src/bison', # -> found bugs in
 'cat': './latest-targets/coreutils/src/cat',
 'col': './latest-targets/util-linux/col',
 'colcrt': './latest-targets/util-linux/colcrt',
 'column': './latest-targets/util-linux/.libs/column', # -> found bugs in
 'colrm': './latest-targets/util-linux/colrm',
 'comm': './latest-targets/coreutils/src/comm',
 'cmp': './latest-targets/diffutils/src/cmp',
 'cut': './latest-targets/coreutils/src/cut',
 'dc': './latest-targets/bc/dc/dc', # -> found bugs in
 'diff': './latest-targets/diffutils/src/diff',
 'expand': './latest-targets/coreutils/src/expand',
 'fmt': './latest-targets/coreutils/src/fmt',
 'fold': './latest-targets/coreutils/src/fold',
 'gdb': './latest-targets/gdb/gdb/gdb', # -> found bugs in
 'grep': './latest-targets/grep/src/grep',
 'head': './latest-targets/coreutils/src/head',
 'join': './latest-targets/coreutils/src/join',
 'look': './latest-targets/util-linux/look',
 'm4': './latest-targets/m4/src/m4',
 'nl': './latest-targets/coreutils/src/nl',
 'nm': './latest-targets/binutils/binutils/nm-new',
 'od': './latest-targets/coreutils/src/od',
 'paste': './latest-targets/coreutils/src/paste',
 'pr': './latest-targets/coreutils/src/pr',
 'ptx': './latest-targets/coreutils/src/ptx', # -> found bugs in
 'rev': './latest-targets/util-linux/rev',
 'sdiff': './latest-targets/diffutils/src/sdiff',
 'spell': './latest-targets/spell/spell', # -> found bugs in
 'strings': './latest-targets/binutils/binutils/strings',
 'strip': './latest-targets/binutils/binutils/strip-new',
 'sort': './latest-targets/coreutils/src/sort',
 'tac': './latest-targets/coreutils/src/tac', # -> found bugs in
 'tail': './latest-targets/coreutils/src/tail',
 'tee': './latest-targets/coreutils/src/tee', # -> found bugs in
 'tr': './latest-targets/coreutils/src/tr',
 'troff': './latest-targets/groff/troff', # -> found bugs in
 'tsort': './latest-targets/coreutils/src/tsort', # -> found bugs in
 'unexpand': './latest-targets/coreutils/src/unexpand',
 'uniq': './latest-targets/coreutils/src/uniq',
 'wc': './latest-targets/coreutils/src/wc',
 'xargs': './latest-targets/findutils/xargs/xargs'
}
fastest_binaries = {
 # takes <5 minutes to fuzz
 'colrm': './latest-targets/util-linux/colrm',
 'cmp': './latest-targets/diffutils/src/cmp',
 'cut': './targets/coreutils/src/cut',
 'head': './targets/coreutils/src/head',
 'look': './latest-targets/util-linux/look',
 'nm': './latest-targets/binutils/binutils/nm-new',
 'rev': './latest-targets/util-linux/rev',
 'strip': './latest-targets/binutils/binutils/strip-new'
}
fast_binaries = {
 # takes 5-10 minutes to fuzz
 'cat': './latest-targets/coreutils/src/cat',
 'comm': './latest-targets/coreutils/src/comm',
 'grep': './latest-targets/grep/src/grep',
 'nl': './latest-targets/coreutils/src/nl',# not sure to fuzz or to not
 'tee': './latest-targets/coreutils/src/tee',
 'unexpand': './latest-targets/coreutils/src/unexpand',
 'uniq': './latest-targets/coreutils/src/uniq'
}
medium_binaries = {
 # takes 10-30 minutes to fuzz
 'expand': './latest-targets/coreutils/src/expand',
 'dc': './latest-targets/bc/dc/dc',
 'diff': './latest-targets/diffutils/src/diff',
 'fmt': './latest-targets/coreutils/src/fmt',
 'fold': './latest-targets/coreutils/src/fold',
 'join': './latest-targets/coreutils/src/join',
 'm4': './latest-targets/m4/src/m4',
 'paste': './latest-targets/coreutils/src/paste',
 # 'ptx': './latest-targets/coreutils/src/ptx',
 'sdiff': './latest-targets/diffutils/src/sdiff',
 'strings': './latest-targets/binutils/binutils/strings',
 'tac': './latest-targets/coreutils/src/tac',
 'wc': './latest-targets/coreutils/src/wc'
}
slow_binaries = {
 # takes 30-60 minutes to fuzz
 'colcrt': './latest-targets/util-linux/colcrt',
 'pr': './latest-targets/coreutils/src/pr',
 'xargs': './latest-targets/findutils/xargs/xargs'
 # 'tsort': './latest-targets/coreutils/src/tsort'
}
slowest_binaries = {
# takes over an hour to fuzz
 'bc': './latest-targets/bc/bc/bc',
 'col': './latest-targets/util-linux/col',
 'column': './latest-targets/util-linux/.libs/column',
 'od': './latest-targets/coreutils/src/od',
 'sort': './latest-targets/coreutils/src/sort', #also generates lots of files. unnecessarily
 'tail': './latest-targets/coreutils/src/tail',
 'tr': './latest-targets/coreutils/src/tr'
}

# all the following groups take approximately the same time to fuzz. Can parallely call them
group1 = {
 'bc': './latest-targets/bc/bc/bc'
}

group2 = {
 'col': './latest-targets/util-linux/col',
 'comm': './latest-targets/coreutils/src/comm',
 'dc': './latest-targets/bc/dc/dc',
 'fmt': './latest-targets/coreutils/src/fmt'
}

group3 = {
 # 'column': './latest-targets/util-linux/.libs/column', # -> already found bugs in
 'tr': './latest-targets/coreutils/src/tr',
 'fold': './latest-targets/coreutils/src/fold',
 'join': './latest-targets/coreutils/src/join',
 # 'ptx': './latest-targets/coreutils/src/ptx', # -> found bugs in
 'sdiff': './latest-targets/diffutils/src/sdiff',
 # 'tsort': './latest-targets/coreutils/src/tsort', # -> found bugs in
 'grep': './latest-targets/grep/src/grep',
 'look': './latest-targets/util-linux/look',
 'nm': './latest-targets/binutils/binutils/nm-new',
 'expand': './latest-targets/coreutils/src/expand',
 'diff': './latest-targets/diffutils/src/diff'
}

group4 = {
 'od': './latest-targets/coreutils/src/od',
 'colcrt': './latest-targets/util-linux/colcrt',
 'strings': './latest-targets/binutils/binutils/strings',
 'nl': './latest-targets/coreutils/src/nl',# not sure to fuzz or to not
 'rev': './latest-targets/util-linux/rev',
 'strip': './latest-targets/binutils/binutils/strip-new'
}

group5 = {
 'sort': './latest-targets/coreutils/src/sort', #also generates lots of files. unnecessarily
 'pr': './latest-targets/coreutils/src/pr',
 # 'tac': './latest-targets/coreutils/src/tac', # -> found bugs in
 # 'tee': './latest-targets/coreutils/src/tee', # -> found bugs in
 'm4': './latest-targets/m4/src/m4',
 'cat': './latest-targets/coreutils/src/cat',
 'colrm': './latest-targets/util-linux/colrm',
 'cmp': './latest-targets/diffutils/src/cmp'
}

group6 = {
 'tail': './latest-targets/coreutils/src/tail',
 'paste': './latest-targets/coreutils/src/paste',
 'cut': './targets/coreutils/src/cut',
 'head': './targets/coreutils/src/head',
 'xargs': './latest-targets/findutils/xargs/xargs',
 'wc': './latest-targets/coreutils/src/wc',
 'unexpand': './latest-targets/coreutils/src/unexpand',
 'uniq': './latest-targets/coreutils/src/uniq'
}
