#!/usr/bin/env python3

# This file contains the OptionRunner I wrote during the seminar.

from OptionGrammarMiner import OptionGrammarMiner
from fuzzingbook.Fuzzer import ProgramRunner
from fuzzingbook.Grammars import unreachable_nonterminals
from fuzzingbook.Grammars import convert_ebnf_grammar
import subprocess, os, json

class OptionRunner(ProgramRunner):
    # Pass path to grammarfile in the init
    def __init__(self, program, grammarfile=None):
        if isinstance(program, str):
            self.executable = program
        else:
            self.executable = program[0]
        if grammarfile is not None and os.path.exists(grammarfile):
            with open(grammarfile, 'r') as gramjsonfile:
                self._ebnf_grammar=json.load(gramjsonfile)
        else:
            self.find_grammar()
        super().__init__(program)

    def run_process(self, shell=False, timeout=5):
        """Run the program with `inp` as input.  Return result of `subprocess.run()`."""
        result = subprocess.run(self.program,
                            timeout=timeout,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.STDOUT,
                            encoding='latin1',
                            shell=shell)
        return result

    def run(self, shell=False, timeout=100):
        """Run the program with calling self.program  Return test outcome based on result of `subprocess.run()`."""
        result = self.run_process(shell, timeout)

        if result.returncode == 0:
            outcome = self.PASS
        # All system signals are (< 0) or (128 + a number) in this case.
        #"kill -l" to list them
        elif result.returncode < 0 or result.returncode in range(128, 255):
            outcome = self.FAIL
        # http://www.unixmantra.com/2014/04/linux-aix-os-return-codes.html#linux
        else:
            outcome = self.UNRESOLVED

        return (result, outcome)

    def find_grammar(self, extra_rules=None, invalid_options=False, invalid_values=False):
        miner = OptionGrammarMiner(self.executable)
        self._ebnf_grammar = miner.mine_ebnf_grammar(invalid_options, invalid_values)
        if self._ebnf_grammar is not None and extra_rules is not None:
            self.set_rules(extra_rules)

    def ebnf_grammar(self):
        return self._ebnf_grammar

    def grammar(self):
        if self._ebnf_grammar is None:
            return None
        return convert_ebnf_grammar(self._ebnf_grammar)

    def set_rules(self, rules):
        for key, value in rules.items():
            self._ebnf_grammar[key] = value
        # Delete rules for previous arguments
        for nonterminal in unreachable_nonterminals(self._ebnf_grammar):
            del self._ebnf_grammar[nonterminal]

    def set_invocation(self, program):
        self.program = program

    def get_executable(self):
        return self.executable
