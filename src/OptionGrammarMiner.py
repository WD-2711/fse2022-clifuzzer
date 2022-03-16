#!/usr/bin/env python3
# This file contains the OptionGrammarMiner I wrote during the seminar.

import utils
from fuzzingbook.Grammars import START_SYMBOL
from fuzzingbook.Grammars import crange, srange, convert_ebnf_grammar, is_valid_grammar
import string
from pprint import pprint
from fuzzingbook.GrammarCoverageFuzzer import GrammarCoverageFuzzer
import sys

class OptionGrammarMiner(object):
    OPTION_SYMBOL = "<option>" # all options
    ARGUMENTS_SYMBOL = "<arguments>" # command line arguments
    OTHER_OPTION_SYMBOL = "<other_option>" # non hv_options

    def __init__(self, process, log=False):
        self.process = process
        self.log = log
        self.converted_grammar = None
        self.grammar = None

    def update_str(self):
        if "<str>" in self.grammar:
            self.grammar["<str>"] = [utils.random_string()]

    def get_bnf_grammar(self, insert_invalid_options=False, insert_invalid_values=False):
        if self.grammar is None:
            self.mine_ebnf_grammar(insert_invalid_options, insert_invalid_values)

        if self.converted_grammar is None:
            self.converted_grammar = convert_ebnf_grammar(self.grammar)

        if is_valid_grammar(self.converted_grammar):
            return self.converted_grammar
        else:
            print("The extracted and converted grammar is not valid")
            pprint(self.converted_grammar)
            raise utils.ParseInterrupt

    def mine_ebnf_grammar(self, insert_invalid_options=False, insert_invalid_values=False):
        self.grammar = {
            START_SYMBOL: [self.OPTION_SYMBOL  + self.ARGUMENTS_SYMBOL],
            self.OPTION_SYMBOL: ["(" + self.OTHER_OPTION_SYMBOL+ ")*"],
            self.ARGUMENTS_SYMBOL: [''],
            self.OTHER_OPTION_SYMBOL: []
        }
        try:
            self.get_grammar(insert_invalid_options, insert_invalid_values)
        except utils.ParseInterrupt: #No grammar was extracted in the utils module
            self.grammar = None
        return self.grammar

    def mine_grammar(self):
        return convert_ebnf_grammar(self.mine_ebnf_grammar())

    def get_grammar(self, insert_invalid_options=False, insert_invalid_values=False):
        options_list = utils.get_options(self.process, insert_invalid_options, self.log)
        if options_list == None:
            raise utils.ParseInterrupt

        # this also mightn't work with arguments that need redirection i.e. stdin
        num_args = utils.run_process_with_test_arg(self.process, 'dufo23opq')

        filelist = [" FILE", " FILE/HelloWorld.py",
                    " FILE/emptyfile", " FILE/testopt", " FILE/README",
                    " FILE/image.jpg", " FILE/audio.wav", " FILE/largeaudio.wav",
                    " FILE/E.coli", " FILE/bible.txt", " FILE/world192.txt"]
        # we don't need to do anything for tools that need 0 arguments e.g. date, dd
        if num_args == 1:
            # can send at least one argument
            self.grammar[self.ARGUMENTS_SYMBOL] = ["<files>"]
            self.grammar["<files>"] = filelist
            for i in range(30):
                self.grammar["<files>"].append(" FILE/s"+ str(i))
            for i in range(30):
                self.grammar["<files>"].append(" FILE/l"+ str(i))

            if insert_invalid_values:
                self.grammar["<files>"].append(" FILE/" + utils.random_string(100))
                self.grammar["<files>"].append(" FILE/" + utils.random_string(300))
        elif num_args == 2:
            # need exactly 2 arguments
            self.grammar[self.ARGUMENTS_SYMBOL] = ["<files1><files2>"]

            self.grammar["<files1>"] = filelist
            self.grammar["<files2>"] = filelist
            for i in range(30):
                self.grammar["<files1>"].append(" FILE/s"+ str(i))
                self.grammar["<files2>"].append(" FILE/s"+ str(i))
            for i in range(30):
                self.grammar["<files1>"].append(" FILE/l"+ str(i))
                self.grammar["<files2>"].append(" FILE/l"+ str(i))
            if insert_invalid_values:
                self.grammar["<files1>"].append(" FILE/" + utils.random_string(100))
                self.grammar["<files1>"].append(" FILE/" + utils.random_string(300))
                self.grammar["<files2>"].append(" FILE/" + utils.random_string(100))
                self.grammar["<files2>"].append(" FILE/" + utils.random_string(300))

        for option in options_list:
            self.process_arg(option, num_args, insert_invalid_values)

        if not self.grammar[self.OTHER_OPTION_SYMBOL]: # this is empty
            self.grammar[self.OTHER_OPTION_SYMBOL] = ['']

    def add_str_rule(self, insert_invalid_values=False):
        self.grammar["<str>"] = [utils.random_string()]

    def add_optional_c_str_rule(self):
        self.grammar["<optional_c_str>"] = ["str"]
    # different optional rules for single char options and string options
    # e.g. --color=always & -calways (-c takes in optional argument here)
    def add_optional_str_rule(self):
        self.grammar["<optional_str>"] = ["=str"]

    def add_optional_c_int_rule(self):
        self.grammar["<optional_c_int>"] = ["<int>"]

    def add_optional_int_rule(self):
        self.grammar["<optional_int>"] = ["=<int>"]

    def add_random_elements(self):
        self.grammar["<random_elements>"] = [" FILE/" + utils.random_string(),
            utils.random_string(), utils.random_string(50), utils.random_string(100),
            utils.random_string(300)]

    def add_int_rule(self, insert_invalid_values=False):
        self.grammar["<hex-int>"] = ["0x<hex-digit>+"]
        self.grammar["<octal-int>"] = ["0<octal-digit>+"]
        self.grammar["<decimal-int>"] = ["<non-zero-digit><digit>*"]
        self.grammar["<digit>"] = crange('0', '9')
        self.grammar["<non-zero-digit>"] = crange('1', '9')
        self.grammar["<octal-digit>"] = crange('0', '7')
        self.grammar["<hex-digit>"] = crange('0', '9') + crange('a', 'f')
        if insert_invalid_values:
            self.grammar["<int>"] = ["<digit>+",
                                     "<non-zero-digit><digit>" + utils.random_string(100),
                                     utils.random_string(100) + "<non-zero-digit><digit>"]
        else:
            self.grammar["<int>"] = ["<decimal-int>", "<octal-int>", "<hex-int>"]


    def add_arguments(self, option, args, insert_invalid_values=False):
        if args == "Number":
            self.add_int_rule()
            if option.has_arg == 2:
                if option.char_option:
                    self.add_optional_c_int_rule()
                    return "<optional_c_int>?"
                else:
                    self.add_optional_int_rule()
                    return "<optional_int>?"
            else:
                return "<int>"
        elif args == []:
            # self.add_str_rule()
            if option.has_arg == 2:
                if option.char_option:
                    self.add_optional_c_str_rule()
                    return "<optional_c_str>?"
                else:
                    self.add_optional_str_rule()
                    return "<optional_str>?"
            else:
                return "str"
        elif type(args) is list:
            opt_name = option.name
            # self.add_str_rule()
            # self.add_int_rule()
            if option.has_arg == 2:
                if option.char_option:
                    args = [' {0}'.format(element) for element in args]
                    # args.append(" <str>")
                    # args.append(" <int>")
                    self.grammar["<"+opt_name+"1>"] = args
                    return "<"+opt_name+"1>?"
                else:
                    args = ['={0}'.format(element) for element in args]
                    # args.append('=<str>')
                    # args.append("=<int>")
                    self.grammar["<"+opt_name+"1>"] = args
                    return "<"+opt_name+"1>?"
            else:
                # args.append("<str>")
                # args.append("<int>")
                self.grammar["<"+opt_name+"1>"] = args
                return "<"+opt_name+"1>"
        else:
            print (option, args)

    def process_arg(self, option, num_args, insert_invalid_values=False):

        if option.name == 'help' or option.name == 'version':
            return
        else:
            target = self.OTHER_OPTION_SYMBOL

        if option.char_option:
            prefix = '-'
            separator = " "
        else:
            prefix = "--"
            separator = "="

        # option takes an optional argument.
        if option.has_arg == 2:
            args = utils.run_process_with_test_option_value(self.process, option, num_args)
            if args is None:
                arg = " " + prefix + option.name + "__ optional value expected __"
            else:
                arg = " " + prefix + option.name + self.add_arguments(option,
                        args, insert_invalid_values)


        # option takes an required argument.
        elif option.has_arg == 1:
            args = utils.run_process_with_test_option_value(self.process, option, num_args)
            if args is None:
                arg = " " + prefix + option.name + "__ required value expected __"
            else:
                arg = " " + prefix + option.name + separator + self.add_arguments(option,
                        args, insert_invalid_values)

        # option takes no arguments
        else:
            arg = " " + prefix + option.name

        self.grammar[target].append(arg)

ex_testopt_gram = {'<start>': ['<option><arguments>'],
                    '<option>': ['(<other_option>)*'],
                    '<arguments>': ['<files>'],
                    '<other_option>': [' -a', ' -b str', ' -c<optional_c_str>?'],
                    '<files>': [' FILE', ' FILE/HelloWorld.py', ' FILE/README',
                                ' FILE/emptyfile', ' FILE/testopt'],
                   } # ignores str expansion for comparision

ex_testlongopt_gram = {'<start>': ['<option><arguments>'],
                        '<option>': ['(<other_option>)*'],
                        '<arguments>': [''],
                        '<other_option>': [' -a', ' -b', ' -c str', ' -d str',
                        ' -m<optional_c_str>?', ' -f<optional_c_str>?', ' --verbose',
                        ' --brief', ' --add', ' --noarg_dummy', ' --delete=str',
                        ' --reqarg_dummy=str', ' --modify<optional_str>?',
                        ' --optarg_dummy<optional_str>?'],
                      } # ignores str expansion for comparision


if __name__ == "__main__":
    miner = OptionGrammarMiner("tests/testopt", log=False)

    testopt_grammar = miner.mine_ebnf_grammar(insert_invalid_values = False)
    pprint(testopt_grammar)
    if not (ex_testopt_gram.items() <= testopt_grammar.items() and
            is_valid_grammar(testopt_grammar)):
        print ("ERROR: extracted testopt grammar doesn't contain expected testopt grammar")
        print ("Extracted testopt grammar:")
        pprint(testopt_grammar)
        print ("Expected testopt options:")
        pprint(ex_testopt_gram)
        print("**Not conducting further tests. Exiting now!!")
        sys.exit(1)

    miner = OptionGrammarMiner("tests/testlongopt", log=False)

    testlongopt_grammar = miner.mine_ebnf_grammar(insert_invalid_values = False)
    pprint (testlongopt_grammar)
    if not (ex_testlongopt_gram.items() <= testlongopt_grammar.items() and
            is_valid_grammar(testlongopt_grammar)):
        print ("ERROR: extracted testlongopt grammar doesn't contain expected testlongopt grammar")
        print ("Extracted testlongopt grammar:")
        pprint(testlongopt_grammar)
        print ("Expected testlongopt options:")
        pprint(ex_testlongopt_gram)
        sys.exit(1)
    print("Mining grammars for testopt and testlongopt went successfully. Yayy!")
