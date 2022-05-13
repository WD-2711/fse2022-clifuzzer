# Replication package for _Mining Grammars for Command-Line Invocations_

Our submission is a tool that implements the algorithm described in the paper
_Mining Grammars for Command-Line Invocations_. We provide a LXD container which
contains the complete artifacts necessary to reproduce our experiments. We describe
the process of invoking the container below.

We also note that you can setup any Ubuntu image on LXD, install a list of
requirements and clone this repository to reproduce our experiments and results.
The steps on doing this is listed in the file [etc/new\_lxd\_notes.txt](https://github.com/clifuzzer/fse2022-clifuzzer/blob/main/etc/new_lxd_notes.txt).


## Overview

This paper presents an automated procedure to extract the configuration options
of command-line utilities in Linux that use _getopt_, _getopt\_long_  or 
_getopt\_long\_only_ to parse their command-line invocation.
The extracted options is converted into a context-free grammar and saved.
We used the extracted grammars of 44 utilities in Linux to fuzz them, finding
failures in 25% (11/44) of them.


## Prerequisites

### Environment
All experiments were done inside a container launched using [LXD](https://linuxcontainers.org/lxd/)
on a Ubuntu 20.04.3 64-bit system running Intel Core Processor (Skylake, IBRS)
with 16 gigabytes of RAM. The container run Ubuntu 20.04.3 LTS with the same 
processor and memory as the host and uses gcc 9.4.0 and afl-c++2.59d.

### Setup
First, please make sure that LXD is installed in your host system.
In case of Linux host OSs, please also ensure that /proc/sys/kernel/core\_pattern
doesn't point to apport (to run AFL++). This can be updated by the following 
commands on the host OS (the commands in the host system are indicated by
leading `$` and the other lines indicate the expected output):

```bash
$ cat /proc/sys/kernel/core_pattern
|/usr/share/apport/apport %p %s %c %d %P %E
$ sudo sh -c "echo /tmp/core.%e.%p.%t > /proc/sys/kernel/core_pattern"
$ cat /proc/sys/kernel/core_pattern
/tmp/core.%e.%p.%t
```

#### Download
Next, please download the container image tarball from the link:
https://sandbox.zenodo.org/record/1035217#.YjFTii1Q1TY

This downloads a tarball called `clifuzzer-image.tar.gz` which is 967 MB in size

```bash
$ du -ksh clifuzzer-image.tar.gz
967M    clifuzzer-image.tar.gz
```

and has the following _md5_ checksum

```bash
$ md5sum clifuzzer-image.tar.gz
0250cabcc06cc2bde8f8ccdb992c04f8  clifuzzer-image.tar.gz
```

#### Importing and starting the container

The container can be imported and started as follows:

```bash

$ lxc image import clifuzzer-image.tar.gz --alias clifuzzer-image
Image imported with fingerprint: ee430354830c7beced231f293d0f51805e221eb7c498453adca30b7ddc1fefe9

$ lxc init clifuzzer-image clifuzzer
Creating clifuzzer

$ lxc start clifuzzer

$ lxc ls
+-----------+---------+---------------------+----------------------------------------------+-----------+-----------+
|   NAME    |  STATE  |        IPV4         |                     IPV6                     |   TYPE    | SNAPSHOTS |
+-----------+---------+---------------------+----------------------------------------------+-----------+-----------+
| clifuzzer | RUNNING | 10.34.31.153 (eth0) | fd42:3f23:6d2:e033:216:3eff:fe1c:a741 (eth0) | CONTAINER | 0         |
+-----------+---------+---------------------+----------------------------------------------+-----------+-----------+
```

#### Logging into the container

You can login to the `clifuzzer` container using the following command -

```bash
$ lxc exec clifuzzer -- sudo --login --user ubuntu
ubuntu@clifuzzer:~$
```
This logs you inside the container with the username `ubuntu` and the `ubuntu@clifuzzer:~$`
prompt.
You can verify the contents using the following commands

```bash
ubuntu@clifuzzer:~$ pwd
/home/ubuntu

ubuntu@clifuzzer:~$ ls
clifuzzer-image.tar.gz  fse2022-clifuzzer

ubuntu@clifuzzer:~/fse2022-clifuzzer/src$ ls
FILE         OptionFuzzer.py        OptionRunner.py  c-lib       fuzzable_binaries.py  generate_argfiles.py  latest-targets     run-cf-cmd.py  setup.sh  tests
FILE_backup  OptionGrammarMiner.py  afl-targets      exports.sh  gather-coverage.py    grammar               observed-failures  run-cf.py      targets   utils.py
```

We note the important files inside the `/fse2022-clifuzzer/src` directory. They are-

| File/Directory               | Description                                                                 |
|------------------------------|-----------------------------------------------------------------------------|
| run-cf-cmd.py                | The script to run clifuzzer on any binary                                   |
| setup.sh                     | The script to populate FILE with fuzzing inputs and download and build the fuzzing targets|
| generate\_argfiles.py        | The script generates the random inputs for the purpose of fuzzing |
| fuzzable\_binaries.py        | The file containing paths to binaries that are fuzzed |
| grammar                      | The directory containing all the utilities' extracted grammars |
| latest-targets               | The directory containing all the target utilities in their latest versions (also their gathered coverage post fuzzing), compiled with gcc |
| afl-targets                  | The directory containing all the target utilities in their latest versions (also their gathered coverage post fuzzing), compiled with afl-c++|
| latest-targets               | The directory containing all the target utilities in their older versions, compiled with gcc|
| observed-failures            | The directory containing details of all the observed failures, including their invocation and input files |

## Running the experiments

Before running the experiments we need to download and build the targets and generate the input files.
To do this, run `setup.sh`. This will also create an `outputdir` directory which
will hold the logs of fuzzing.

```bash
ubuntu@clifuzzer:~/fse2022-clifuzzer/src$ ./setup.sh
Generating library objects!
...
linux-gnu type OS detected
gcc -shared -fPIC mygetopt.c -o mygetopt.so -ldl
Generating library objects done!
Generating tests for fuzzing!
...
/home/ubuntu/fse2022-clifuzzer/src
FILE_backup/emptydir doesn't exist already, creating now
generating FILE_backup/s0
generating FILE_backup/s1
...
```
Once this is over, the `FILE\_backup` and `FILE` directories will be full of input files,
and the `targets`, `latest-targets` and `afl-targets` directories 
will contain built utilities inside them

We are ready to generate grammars and fuzz at this point. We use the `run-cf-cmd.py` script
for this purpose:

```bash
ubuntu@clifuzzer:~/fse2022-clifuzzer/src$ python3 run-cf-cmd.py --help
usage: run-cf-cmd.py [-h] [--get-grammar | --get-options | -f FUZZ | --get-coverage | --fuzz-coverage FUZZ_COVERAGE | --get-manual-coverage] [-o O] [-g GRAM_FILE] [--log-pass] [--invalid-options] [--invalid-values] [--seed SEED]
                     binary

Run Configuration fuzzing on the given binary

positional arguments:
  binary                Binary or path to Binary to fuzz on

optional arguments:
  -h, --help            show this help message and exit
  --get-grammar         Print the grammar extracted from options
  --get-options         Print a list of cmdline options available in the binary
  -f FUZZ, --fuzz FUZZ  No. of times the fuzzer should fuzz the binary and note unexpected behaviour including crashes and interesting return codes
  --get-coverage        Extract the coverage achieved in the tool
  --fuzz-coverage FUZZ_COVERAGE
                        Run fuzz FUZZ_COVERAGE times and then report the extracted coverage. Equivalent to running -f FUZZ_COVERAGE first and then running --get-coverage on a binary
  --get-manual-coverage
                        Extract the manual testing coverage of the binary
  -o O                  File to dump the output to. Defaults to binary-name.out
  -g GRAM_FILE, --gram-file GRAM_FILE
                        File containing the grammar to fuzz from.
  --log-pass            logs passing invocations as well.
  --invalid-options     Inserts invalid options into the grammar
  --invalid-values      Inserts invalid values for some options in the grammar
  --seed SEED           Seed for randomising
```

If we wished to extract the grammar of say, the `ls` utility, and write it to `ls-gram.json`
then we will invoke `run-cf-cmd.py` script as

```bash
ubuntu@clifuzzer:~/fse2022-clifuzzer/src$ python3 run-cf-cmd.py --get-grammar -o ls-gram.json ./latest-targets/coreutils/src/ls
```

If we wished to fuzz the `ls` utility 3000 times using the `ls-gram.json` grammar (already extracted
and saved in the `grammar` directory), while logging the results of all the invocations (including the passing ones)
then we invoke the `run-cf-cmd.py` script as

```bash
ubuntu@clifuzzer:~/fse2022-clifuzzer/src$ python3 run-cf-cmd.py -f 3000 -g grammar/ls-gram.json -o outputdir/ls.out --log-pass ./latest-targets/coreutils/src/ls
```

## Failure inducing CLI invocations found by CLIFuzz

| Utility                      | Failure type  | Invocation                                                  |
|------------------------------|---------------|-------------------------------------------------------------|
| as (v2.30)                   | hang | `as -a < l8` |
| as (v2.37)                   | hang | `as -a < l8` |
| bison (v3.0.4)               | hang | `bison l26` |
| bison (v3.8)                 | crash | `bison --trace s1` |
| column (v2.37.2)             | crash | `column testopt largeaudio.wav` (returns SIGSEGV) |
| column (v2.37.2)             | crash | `column E.coli image.jpg` (returns SIGABRT) |
| dc (v1.41)                   | hang | `dc -f largeaudio.wav < l5` |
| gdb (v8.1)                   | crash | `gdb < l10` (returns SIGSEGV)|
| gdb (v11.1)                  | crash | `gdb < l10` (returns SIGABRT)|
| ptx (v8.28)                  | hang | `ptx --references --traditional testopt` |
| ptx (v9.0)                   | hang | `ptx --references --traditional testopt` |
| spell (v1.0)                 | hang | `spell E.coli` |
| spell (v1.0)                 | crash | `spell s0`  |
| spell (v1.1)                 | hang | `spell E.coli` |
| tac (v9.0)                   | hang | `tac --separator .+5 --regex E.coli` |
| tee (v9.0)                   | hang | `tee --append README < README` |
| troff (v1.22.3)              | hang | `troff l22` |
| troff (v1.22.4)              | hang | `troff l22` |
| tsort (v9.0)                 | hang | `tsort largeaudio.wav` |

## Recreating the failures

The detailed descriptions of the observed failures for each of the 11 utilities
have been noted in the observed-failures directory, which can be used to recreate
the failures. For example, the recreate the failure observed in `as`'s latest version,
we learn from the following notes that it can be recreated by invoking `./latest-targets/binutils/gas/as-new -a < observed-failures/as/v2.37/l8`.

```bash
ubuntu@clifuzzer:~/fse2022-clifuzzer/src$ ls observed-failures/
README.txt  as  bison  column  dc  gdb  ptx  spell  tac  tee  troff  tsort
ubuntu@clifuzzer:~/fse2022-clifuzzer/src$ ls observed-failures/as
v2.30  v2.37
ubuntu@clifuzzer:~/fse2022-clifuzzer/src$ ls observed-failures/as/v2.37
README.txt  l2  l7  l8
ubuntu@clifuzzer:~/fse2022-clifuzzer/src$ cat observed-failures/as/v2.37/README.txt
Execution commands that lead to hangs (executed from src directory)-
    "./latest-targets/binutils/gas/as-new -a < observed-failures/as/v2.37/l8"
    "./latest-targets/binutils/gas/as-new -a < observed-failures/as/v2.37/l7"
    "./latest-targets/binutils/gas/as-new -a < observed-failures/as/v2.37/l2"

these inputs were generated by the command-
    "python3 generate_argfiles.py -p --length-level 3"
```


### Details of utilities' options and option-arguments

| Utility | Options with arguments?  | Exits on wrong option-argument type? | Exit inducing sample invocation | Valid values in example | Options mismatch in code vs documentation (with example)| 
|---|---|---|---|---|---|
| as (v2.30) | yes | yes | `as --msse-check=a1 < l1` | One of ["none", "error", ...] | yes, `--dumpconfig` |
| bc (v1.07.1) | no | NA | NA | NA | yes (-c)|
| bison (v3.8) | yes | yes | `bison --feature=a1 l1` | One of ["none", "caret", ...]  | yes, `--trace` |
| cat (v9.0) | no | NA | NA | NA | no|
| cmp (v3.8) | yes | yes | `cmp -n 4t l1 l2` | Integer | yes, `-c`|
| col (v2.37.2) | yes | yes | `col -l 0x4 < l1` | Integer | no |
| colcrt (v2.37.2) | no | NA | NA | NA | no|
| colrm (v2.37.2) | no | NA | NA | NA | no|
| column (v2.37.2) |yes | yes| `column -c 0x4 l1` | Integer | yes, `--columns`
| comm (v9.0) | no | NA | NA | NA | no|
| cut (v9.0) | no | NA | NA | NA | no|
| dc (v1.4.1) | no | NA | NA | NA | no|
| diff (v3.8) | yes | yes | `diff -C 0x4 l1 l2` | Integer | yes, `-0`|
| expand (v9.0) | yes | yes | `expand -t 0x4 l1` | Integer | yes, `-0`|
| fmt (v9.0) | yes | yes | `fmt -w 0x6 l1` | Integer | no |
| fold (v9.0) | yes | yes | `fold -w 0x4 l1` | Integer | yes, `-0`|
| gdb (v11.1)  | yes | no | NA | NA | yes, `-i`|
| grep (v3.7) | yes | yes | `grep -A 0x4 abc l1` | Integer | yes, `-0`|
| head (v9.0) | yes | yes | `head -n 0x4 l1` | Integer | yes, `-0`|
| join (v9.0) | yes | yes | `join -v ox4 l1 l2` | Integer | no |
| look (v2.37.2) | yes | no | NA | NA | no |
| m4 (v1.4.19) | yes | no | NA | NA | yes, `-B`|
| nl (v9.0) | yes | yes | `nl -b b l1`| One of ['a', 't', 'n', 'p'] | no|
| nm (v2.37) | yes | yes | `nm -t e l1` | One of ['d', 'x', 'o'] | yes, `-j`|
| od (v9.0)  | yes | yes | `od -A p l1` | One of ['d', 'x', 'o', 'n' ] | yes, `-b`|
| paste (v9.0) | no | no | NA | NA | no |
| pr (v9.0) | yes | yes | `pr -N 4t l1` | Integer | yes, `-0`|
| ptx (v9.0) | yes | yes | `ptx --format=a1 l1` | One of ["roff", "tex"] | no |
| rev (v2.37.2) | no | no | NA | NA | no |
| sdiff (v3.8) | yes | yes | `sdiff -w 0x4 l1 l2` | Integer | no |
| sort (v9.0) | yes | yes | `sort -S 4t l1` | Integer | yes, `-y` |
| spell (v1.1) | yes | no | NA | NA | yes, `-l`|
| strings (v2.37) | yes | yes | `strings -t e l1` | One of ['d', 'x', 'o'] | yes, `-0`|
| strip (v2.37) | yes | yes | `strip -F none1 l1` | One of ["ihex", "srec", ...] | yes, `--keep-section-symbols`|
| tac (v9.0) | no | no | NA | NA | no |
| tail (v9.0) | yes | yes | `tail -c 4t l1` | Integer | yes, `-0`|
| tee (v9.0) | yes | yes | `tee --output-error=a1 < false.c   ` | One of ["warn", "srec", ...] | no |
| tr (v9.0)  | no | no | NA | NA | yes, `-A`|
| troff (v1.22.4) | yes | yes | `./troff -f t a.txt` | A character in CAPS | yes, `-t` |
| tsort (v9.0) | no | no | NA | NA | no |
| unexpand(v9.0) | yes | yes | `unexpand -t 0x4 l1` | Integer | yes, `-0`|
| uniq (v9.0) | yes | yes | `uniq -f 4t l1` | Integer | no |
| wc (v9.0) | no | no | NA | NA | yes, `--debug` |
| xargs (v4.8.0) | yes | yes | `xargs -n 4t < l1` | Integer | no|

Here, "NA" means "Not Applicable".

A total of 31 out of 44 utilities have options that take arguments.

A total of 27, out of those 31, utilities exit when their options receive an argument of a different type.

A total of 24 out of 44 utilities have a option mismatch between their getopt strings and their manpage.
