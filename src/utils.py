#!/usr/bin/env python3
import sys, subprocess, os, string, re, random
from collections import namedtuple
from pprint import pprint
from pathlib import Path

name_description = '''The field 'name' contains the name of the option.\n'''

hasarg_description = '''The field 'has_arg' is:
no_argument (or 0) if the option does not take an argument,
required_argument (or 1) if the option requires an argument,
optional_argument (or 2) if the option takes an optional argument.\n'''

char_option_description = '''The field 'char_option' is "True" if the option is a \
character option, "False" otherwise.\n'''

Option_tuple_description =  name_description + hasarg_description + char_option_description

Option = namedtuple('Option', ['name', 'has_arg', 'char_option'])

Coverage = namedtuple('Coverage', ['lines_covered', 'branches_covered',
                        'branches_taken', 'calls_executed', 'successful_calls'])
Coverage.__new__.__defaults__ = (0,) * len(Coverage._fields)

possible_char_options = string.ascii_letters + string.digits + string.punctuation

RANDOM_SEED = 20001

class ParseInterrupt(Exception):
    pass

# All of these can possibly go inside classes.
def random_string(stringlength=30, exclude_list=[], shell=False):
    # subprocess isn't capable of taking in 0x00 as an input
    # shell determines if the final subprocess invocation would be with shell=True
    # we wish to eliminate shell special characters in such cases.
    str1 = ""
    length = random.randrange(1, stringlength)
    bash_special_characters = ['`', '!', ';', '&', '"', "'", '|', '$']
    whitespace_characters = [' ', '\t', '\r', '\n', '\x0b', '\x0c']
    quote_characters = ["'"]
    for i in range(length):
        a = random.choice(string.printable)
        # a = chr(random.randint(1,255))
        while a in exclude_list:
            a = random.choice(string.printable)
            # a = chr(random.randint(1,255))
        if shell :
            while a in (bash_special_characters + whitespace_characters) and \
                random.random() > 0.2:
                a = random.choice(string.printable)
                # a = chr(random.randint(1,255))
        str1 += a
    if shell:
        str1 = "$'" + str1 + "'"
    return str1

# The LD_PRELOAD trick works differently in Linux and MacOS.
# os.uname() returns a tuple of (sysname nodename release version machine). I need the sysname.
def get_env(dynlink_list):
    # require dynlink_list to contain just names and not extensions. e.g. myopen, mystrcmp.
    dl_path = os.getcwd() + '/c-lib/'
    env = {
        **os.environ
    }
    if os.uname()[0] == "Darwin":
        extension = ".dylib"
    elif os.uname()[0] == "Linux":
        extension = ".so"
    else:
        raise OSError("Couldn't detect OSType, can't load shared libraries")
    dynlink_value = ""
    for dynlink in dynlink_list:
        if dynlink_value == "":
            dynlink_value = dl_path + dynlink + extension
        else:
            dynlink_value = dynlink_value + ":" + dl_path + dynlink + extension
    if os.uname()[0] == "Darwin":
        env["DYLD_FORCE_FLAT_NAMESPACE"] = '1'
        env["DYLD_INSERT_LIBRARIES"] = dynlink_value
    elif os.uname()[0] == "Linux":
        env["LD_PRELOAD"] =  dynlink_value
    return env


def check_file_existence(file):
    filepath = Path(file)
    return filepath.exists()



'''
This function extract_valid_option_values tries to extract the valid set of arguments for options that
(optionally) require an argument.
The design is a bit clunky. We overwrote libc functions strcmp and strncmp to print the values being
compared before continuing the execution. This poses a threat to testing programs that could change the state
of the system. So, for now we focus on the those programs that don't change states.
We pass a random string to the program as an input to the argument. Then we see if that argument turns up
anywhere to be compared.
There's no one single programming style across multiple C binaries within the coreutils package.
So I have hacked around a bit to find out the arguments. The algorithm is more of a heuristic because
there will be cases where it can fail.

If this returns "number", then that options requires a number.
If this returns empty list, then it isn't compared to any value and whatever is passed is instead used up
somewhere inside the program.
Otherwise it returns a list of arguments that's the option value is being compared to.
'''
def extract_valid_option_values(inp_str, arg='lkjfhsfr'):
    inp_str_list = inp_str.split('\n')
    inp_str_list[:] = (value for value in inp_str_list if value != '')
    args_list = []
    # ls returns it in second parameter
    # also possibly the following list of programs
    # du, touch, cp, rm, date, uniq, tee, numfmt, sort, tail, ptx, od
    # basically anything that uses XARGMATCH
    search_pattern = r'second parameter:\' *' + arg + "'"
    upper_search_pattern = r'second parameter:\' *' + arg.upper() + "'"
    pattern_found = False

    for line in inp_str_list:
        if re.search(search_pattern, line) or re.search(upper_search_pattern, line):
            pattern_found = True
            # tac (and all utilities that expect separators) may return None
            # on the next check
            if re.search(r"first parameter:'(.*?)', .*", line) is not None:
                arg = re.search(r"first parameter:'(.*?)', .*", line).group(1)
                args_list.append(arg)
    if pattern_found:
        return args_list

    # this set of programs use streq for comparing, in the first parameter
    # wc
    search_pattern = r'first parameter:\' *' + arg + "'"
    upper_search_pattern = r'first parameter:\' *' + arg.upper() + "'"
    for line in inp_str_list:
        if re.search(search_pattern, line) or re.search(upper_search_pattern, line):
            pattern_found = True
            #similar to tac in previous case
            if re.search(r"second parameter:'(.*?)', .*", line) is not None:
                arg = re.search(r"second parameter:'(.*?)', .*", line).group(1)
                args_list.append(arg)
    if pattern_found:
        return args_list
    # if the string has been found by now, then it takes values from a fixed set

    # if the "invalid" word is found after this, then it takes a number

    if args_list == []:
        search_pattern = r'invalid.*'+arg;
        pattern_found = False
        for line in inp_str_list:
            if re.search(search_pattern, line) is not None:
                pattern_found = True
                break
        if pattern_found:
            return "Number"
    # if neither has been found then it is used in the program internally
    # even if it takes particular values, we can't know it.
    # So we pass some random strings.
    return args_list

def extract_valid_arg_number(inp_str, arg='lkjfhsfr'):
    stat_search_pattern = r'stat: '+ arg
    open_search_pattern = r'open: '+ arg
    missing_operand_search_pattern = r"missing.*operand after .*" + arg
    failed_access_search_pattern = r"failed to access .*" + arg #for ln
    cannot_access_search_pattern = r"cannot access .*" + arg #for dir

    if inp_str == "":
        return 0

    elif re.search(stat_search_pattern, inp_str) is not None:
        return 1

    elif re.search(open_search_pattern, inp_str) is not None:
        return 1

    elif re.search(cannot_access_search_pattern, inp_str) is not None:
        return 1

    elif re.search(missing_operand_search_pattern, inp_str) is not None:
        return 2

    elif re.search(failed_access_search_pattern, inp_str) is not None:
        return 2

    else: # bilkul nahi ricks lene ka
        return 0

# IMP: This logic works with only code. No guarantees for system installed programs.
# might also fail with code. No guarantees. Will update for individual cases
# as and when they appear
def run_process_with_test_arg(process, arg="lkjfhsfr"):
    env = get_env(["myopen", "mystat"])
    args =  [process, arg]
    try:
        exec_result = subprocess.run(args, env=env, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE, timeout=1,
                                        universal_newlines=True)
        if exec_result.returncode == 1:
            # this could be for other reasons too, like readlink which just doesn't care. :P
            print ("Checking if file required failed. Please check. Maybe dynamic libraries weren't found.")
            print (exec_result)
            sys.exit(1)
        else:
            if exec_result.stderr == '':
                return (extract_valid_arg_number(exec_result.stdout, arg))
            else:
                return (extract_valid_arg_number(exec_result.stderr, arg))
    except FileNotFoundError:
        print ("FileNotFoundError: The process file wasn't found")
        sys.exit(1)
    except Exception as e:
        print (e)



def run_process_with_test_option_value(process, Option, num_args, arg="lkjfhsfr"):
    env = get_env(["mystrcmp"])
    file_arg = ["randomfile"]
    if num_args == 1:
        file_arg = ["FILE/README"]
    elif num_args == 2:
        file_arg = ["FILE/sortedfile1.txt", "FILE/sortedfile2.txt"]
    if Option.char_option:
        args = [process, "-" + Option.name + " " + arg] + file_arg
    else:
        args = [process, "--" + Option.name + "=" + arg] + file_arg
    try:
        exec_result = subprocess.run(args, env=env, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE, timeout=20,
                                        universal_newlines=True)
    except subprocess.TimeoutExpired as e:
        print ("couldn't extract values for option {} as attempt timed out.".format(Option.name))
        return None
    except Exception as e:
        print (e)
        return None
    return (extract_valid_option_values(exec_result.stdout + exec_result.stderr, arg))

'''
From https://linux.die.net/man/3/getopt

By default, getopt() permutes the contents of argv as it scans, so that eventually all the nonoptions are at the end. Two other modes are also implemented. If the first character of optstring is '+' or the environment variable POSIXLY_CORRECT is set, then option processing stops as soon as a nonoption argument is encountered. If the first character of optstring is '-', then each nonoption argv-element is handled as if it were the argument of an option with character code 1. (This is used by programs that were written to expect options and other argv-elements in any order and that care about the ordering of the two.) The special argument "--" forces an end of option-scanning regardless of the scanning mode.
If the first character (following any optional '+' or '-' described above) of optstring is a colon (':'), then getopt() returns ':' instead of '?' to indicate a missing option argument.
'''
def get_options(process, insert_invalid_options=False, log=False):
    env = get_env(["mygetopt"])
    try:
        exec_result = subprocess.run(process, env=env, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,
                                        universal_newlines=True)
        out = exec_result.stdout
        err = exec_result.stderr
        if log:
            print (exec_result.returncode)
            print ("out:", out, "\nerr:", err, "\nend of err.")
    except FileNotFoundError as e:
        print ("FileNotFoundError Exception: Called Process to get_options not found", e)
        return None
    except subprocess.CalledProcessError as e:
        print ("subprocess.CalledProcessError Exception: Called Process to get_options returned error", e.returncode)
        return None

    if out == "":
        if log:
            print ("options extraction return code:", exec_result.returncode)
            print ("options return failed with no output")
        return None

    args_list = out.split('\n')[:-1]# ignoring the last ''

    # this means the program doesn't use getopt or its variants
    # the exception is handled in the caller "get_grammar"
    if 'optstring: ' not in args_list[0]:
        return None
    # first we parse the single character options
    if len(args_list[0].split()) <2:
        single_c_options = ""
    else:
        single_c_options = args_list[0].split()[1]
    options_list = []
    ind = 0
    # we don't consider getopt list starting with '+' or '-' or ':'
    if single_c_options != "" and (single_c_options[0] in ['+', '-', ':']):
        single_c_options = single_c_options[1:]
    # the following check eliminates the cases when single_c_options would begin with '+:' or '-:'
    if single_c_options != "" and single_c_options[0] == ':':
        single_c_options = single_c_options[1:]

    while ind < len(single_c_options):
        if ind < len(single_c_options) - 2 and single_c_options[ind+1] == ':' \
            and single_c_options[ind+2] == ':':
            options_list.append(Option(single_c_options[ind], 2, True))
            ind += 2

        elif ind < len(single_c_options) - 1 and single_c_options[ind + 1] == ':':
            options_list.append(Option(single_c_options[ind], 1, True))
            ind += 1
        else:
            options_list.append(Option(single_c_options[ind], 0, True))
        ind += 1

    if (insert_invalid_options):
        for char in possible_char_options:
            if char not in single_c_options:
                options_list.append(Option(char, 0, True))
                break

    for longarg in args_list[1:]:
        name = longarg.split()[0].split(':')[1]
        has_arg = int(longarg.split()[1].split(':')[1])
        options_list.append(Option(name, has_arg, False))

    if (args_list[1:] and insert_invalid_options):
        name = "invalid-option-r5frh4"
        options_list.append(Option(name, 0, False))


    if log:
        for arg in options_list:
           print (arg.name, arg.has_arg)
    return options_list

expected_testopt_list =[
                        Option(name='b', has_arg=1, char_option=True),
                        Option(name='a', has_arg=0, char_option=True),
                        Option(name='c', has_arg=2, char_option=True),
                        Option(name='d', has_arg=0, char_option=True)]

expected_testlongopt_list =[Option(name='a', has_arg=0, char_option=True),
                            Option(name='b', has_arg=0, char_option=True),
                            Option(name='c', has_arg=1, char_option=True),
                            Option(name='d', has_arg=1, char_option=True),
                            Option(name='m', has_arg=2, char_option=True),
                            Option(name='f', has_arg=2, char_option=True),
                            Option(name='verbose', has_arg=0, char_option=False),
                            Option(name='brief', has_arg=0, char_option=False),
                            Option(name='add', has_arg=0, char_option=False),
                            Option(name='noarg_dummy', has_arg=0, char_option=False),
                            Option(name='delete', has_arg=1, char_option=False),
                            Option(name='reqarg_dummy', has_arg=1, char_option=False),
                            Option(name='modify', has_arg=2, char_option=False),
                            Option(name='optarg_dummy', has_arg=2, char_option=False)]

if __name__ == "__main__":
    testopt_options = get_options("tests/testopt", insert_invalid_options=True)
    if testopt_options is None:
        raise TypeError("unable to extract testopt_options")
    if (sorted(testopt_options) != sorted(expected_testopt_list)):
        print ("ERROR: extracted testopt options don't match expected testopt options")
        print ("Extracted testopt options:")
        pprint(testopt_options)
        print ("Expected testopt options:")
        pprint(expected_testopt_list)
        print("**Not conducting further tests. Exiting now!!")
        sys.exit(1)

    testlongopt_options = get_options("tests/testlongopt")
    if testlongopt_options is None:
        raise TypeError("unable to extract testlongopt_options")
    if (sorted(testlongopt_options) != sorted(expected_testlongopt_list)):
        print ("ERROR: extracted testlongopt options don't match expected testlongopt options")
        print ("Extracted testlongopt options:")
        pprint(testlongopt_options)
        print ("Expected testlongopt options:")
        pprint(expected_testlongopt_list)
        sys.exit(1)
    print("Extraction of testopt and testlongopt went successfully. Yayy!")
