#!/usr/bin/python3

import argparse
import sys
import utils
import os
import json
import random
from datetime import datetime
from pprint import pprint
from OptionGrammarMiner import OptionGrammarMiner
from OptionRunner import OptionRunner
from OptionFuzzer import OptionFuzzer
from utils import Coverage

#Update this to true if we wish to also store the pass list.
STORE_PASS_VALUE = False

def get_fuzz_results (outstream, myfuzzer, fuzz_count, get_coverage):
    fail_list = []
    unresolved_list = []
    exception_list = []
    pass_list = []
    for i in range(fuzz_count):
        print("attempt ", i)
        try:
            output = myfuzzer.run(fuzzit=True)
            if type(output[0].args) == list:
                args = " ".join(output[0].args)
            elif type(output[0].args) == str:
                args = output[0].args
            if output[1] == 'FAIL':
                fail_list.append([i, args, output[0].returncode])
                # uncomment the next two lines if output and error needs to be logged.
                # fail_list.append([i, " ".join(output[0].args), output[0].returncode,
                                    # (output[0].stdout + " ::: " + output[0].stderr)])

            elif output[1] == 'UNRESOLVED' and output[0].returncode >2 :
                unresolved_list.append([i, args, output[0].returncode])
                # uncomment the next two lines if output and error needs to be logged.
                # unresolved_list.append([i, output[0].returncode, " ".join(output[0].args),
                                    # (output[0].stdout + " ::: " + output[0].stderr)])
            else:
                if STORE_PASS_VALUE :
                    # only note down the parameters passed and not the output.
                    pass_list.append([i, args, output[0].returncode])
        except Exception as e:
            exception_list.append("Exception occured - {}: {}, for invocation number - {} and input - {}".format(e.__class__,
            e, i, myfuzzer.invocation))

    if get_coverage:
        coverage = myfuzzer.get_coverage()
        if coverage == utils.Coverage():
            outstream.write("Empty coverage received.\n".encode('latin1'))
            outstream.write(str(coverage).encode('latin1'))
        else:
            outstream.write(str(coverage).encode('latin1'))
        outstream.write("\n".encode('latin1'))
    outstream.write("\nEXCEPTION REPORTS - \n".encode('latin1'))
    for exception_details in exception_list:
        outstream.write(exception_details.encode('latin1'))
        outstream.write("\n".encode('latin1'))
    outstream.write("\nCRASH RESULTS - \n".encode('latin1'))
    for fail_result in fail_list:
        outstream.write(str(fail_result).encode('latin1'))
        outstream.write("\n".encode('latin1'))
    outstream.write("\nUNRESOLVED RESULTS - \n".encode('latin1'))
    for unresolved_result in unresolved_list:
        outstream.write(str(unresolved_result).encode('latin1'))
        outstream.write("\n".encode('latin1'))
    outstream.write("\n".encode('latin1'))
    if STORE_PASS_VALUE :
        outstream.write("\nPASSING RESULTS - \n".encode('latin1'))
        for passing_result in pass_list:
            outstream.write(str(passing_result).encode('latin1'))
            outstream.write("\n".encode('latin1'))
        outstream.write("\n".encode('latin1'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Configuration fuzzing on the given binary')
    parser.add_argument("binary", help="Binary or path to Binary to fuzz on")
    ex_group = parser.add_mutually_exclusive_group()
    ex_group.add_argument("--get-grammar", help="Print the grammar extracted from options",
                            action="store_true")
    ex_group.add_argument("--get-options", help="Print a list of cmdline options available in the binary",
                            action="store_true")
    ex_group.add_argument("-f","--fuzz", help="No. of times the fuzzer should fuzz the binary and note unexpected behaviour including crashes and interesting return codes", type=int)
    ex_group.add_argument("--get-coverage", help="Extract the coverage achieved in the tool",
                            action="store_true")
    ex_group.add_argument("--fuzz-coverage", help="Run fuzz FUZZ_COVERAGE times and then report the extracted coverage. Equivalent to running -f FUZZ_COVERAGE first and then running --get-coverage on a binary", type=int)
    ex_group.add_argument("--get-manual-coverage", help="Extract the manual testing coverage of the binary",
                            action="store_true")
    parser.add_argument("-o", help="File to dump the output to. Defaults to binary-name.out")
    parser.add_argument("-g", "--gram-file", help="File containing the grammar to fuzz from.")
    parser.add_argument("--log-pass", help="logs passing invocations as well.", action="store_true")
    parser.add_argument("--invalid-options", help="Inserts invalid options into the grammar ",
                            action="store_true")
    parser.add_argument("--invalid-values", help="Inserts invalid values for some options in the grammar",
                            action="store_true")
    parser.add_argument("--seed", help="Seed for randomising")
    args = parser.parse_args()

    gram_file = None
    test_bin = args.binary
    # print (args)
    if args.seed:
        random.seed(args.seed)
    else:
        random.seed(utils.RANDOM_SEED)

    if (args.o):
        outputfilename = args.o
    else:
        outputfilename = "outputdir/" + os.path.basename(test_bin) + ".out"
    fout = open(outputfilename, 'wb', buffering=0)

    print("Test binary: {}!".format(test_bin))
    print("Writing to:", outputfilename)
    fout.write("Test binary: {}!\n".format(test_bin).encode('latin1'))

    if (args.log_pass):
        STORE_PASS_VALUE = True

    if (args.gram_file):
        print("Reading grammar from:", args.gram_file)
        gram_file = args.gram_file

    if (args.get_options):
        opt_list = utils.get_options(test_bin, args.invalid_options)
        fout.write(utils.Option_tuple_description.encode('latin1'))
        fout.write("\n".encode('latin1'))
        for opt in opt_list:
            fout.write(str(opt).encode('latin1'))

    elif (args.get_grammar):
        miner = OptionGrammarMiner(test_bin, log=False)
        mined_grammar = miner.mine_ebnf_grammar(args.invalid_options, args.invalid_values)
        fout.write(json.dumps(mined_grammar, indent=4).encode('latin1'))

    elif (args.fuzz):
        if gram_file:
            myrunner = OptionRunner(test_bin, gram_file)
        else:
            myrunner = OptionRunner(test_bin)
        myfuzzer = OptionFuzzer(myrunner, invalid_options=args.invalid_options,
                                invalid_values=args.invalid_values, max_nonterminals=5)
        print("Fuzzing {} {} times now starting at {}!".format(test_bin,
            args.fuzz, datetime.now()))
        fout.write("Fuzzing {} {} times now starting at {}!\n".format(test_bin,
            args.fuzz, datetime.now()).encode('latin1'))
        get_fuzz_results(fout, myfuzzer, args.fuzz, False)
        fout.write("\nFinished fuzzing {} {} times  at {}!".format(test_bin,
        args.fuzz, datetime.now()).encode('latin1'))
        print("Finished fuzzing {} {} times at {}!".format(test_bin, args.fuzz, datetime.now()))

    elif (args.get_coverage):
        myrunner = OptionRunner(test_bin)
        myfuzzer = OptionFuzzer(myrunner, invalid_options=args.invalid_options,
                                invalid_values=args.invalid_values, max_nonterminals=5)
        coverage = myfuzzer.get_coverage()
        if coverage == Coverage():
            fout.write("Empty coverage received.".encode("latin1"))
            fout.write(str(coverage).encode("latin1"))
        else:
            fout.write(str(coverage).encode("latin1"))

    elif (args.get_manual_coverage):
        myrunner = OptionRunner(test_bin)
        myfuzzer = OptionFuzzer(myrunner, invalid_options=args.invalid_options,
                                invalid_values=args.invalid_values, max_nonterminals=5)
        fout.write(str(myfuzzer.manual_test_coverage).encode("latin1"))

    elif (args.fuzz_coverage):
        if gram_file:
            myrunner = OptionRunner(test_bin, gram_file)
        else:
            myrunner = OptionRunner(test_bin)
        myfuzzer = OptionFuzzer(myrunner, invalid_options=args.invalid_options,
                                invalid_values=args.invalid_values, max_nonterminals=5)
        print("Fuzzing {} {} times now starting at {}!".format(test_bin,
            args.fuzz, datetime.now()))
        fout.write("Fuzzing {} {} times now starting at {}!\n".format(test_bin,
            args.fuzz, datetime.now()).encode('latin1'))
        get_fuzz_results(fout, myfuzzer, args.fuzz_coverage, True)
        fout.write("\nFinished fuzzing {} {} times  at {}!".format(test_bin,
        args.fuzz, datetime.now()).encode('latin1'))
        print("Finished fuzzing {} {} times at {}!".format(test_bin, args.fuzz, datetime.now()))
    print("Writing done!")
    fout.close()
