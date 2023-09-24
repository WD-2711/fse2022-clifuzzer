#!/usr/bin/env python3

from OptionRunner import OptionRunner
from fuzzingbook.GrammarCoverageFuzzer import GrammarCoverageFuzzer
from utils import Coverage, random_string, check_file_existence
from ManualTestCoverage import ManualTestCov
from pprint import pprint
import subprocess, os, re, sys, stat, random
from pathlib import Path
import filecmp


class CovClass():

    def __init__(self, executable):
        self.executable = executable
        self.coverage_output = None

    def clear_coverage_data(self):
        invocation =  "rm -f " + self.executable + ".gcda"
        dlt_call = subprocess.run(invocation.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        if dlt_call.returncode != 0 or dlt_call.stderr != "" :
            print ("The subprocess rm call returned {} with the following stderr:\n{}".format(dlt_call.returncode, dlt_call.stderr))
            sys.exit(1)

    def run_coverage(self, gcov_options=False):
        executable = self.executable
        gcov_options1 = ""
        if gcov_options:
            gcov_options1 = "-b "
        invocation =  "gcov " + gcov_options1 + executable
        # 使用 gcov 工具生成覆盖率报告
        gcov_call = subprocess.run(invocation.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        if gcov_call.returncode != 0 or gcov_call.stdout == "":
            print ("The subprocess gcov call returned {} with the following stderr:\n{}".format(gcov_call.returncode, gcov_call.stderr))
            self.coverage_output = ""
        else:
            gcov_list = gcov_call.stdout.split("File ")
            for file_coverage in gcov_list:
                if os.path.basename(executable) in file_coverage.split('\n')[0]:
                    self.coverage_output = file_coverage

        if gcov_call.returncode == 0 and gcov_call.stderr != "":
            print("The subprocess gcov call returned 0 with stderr:\n{}".format(gcov_call.stderr))

    def extract_coverage_data(self):
        self.run_coverage(True)
        lc = 0
        bc = 0
        bt = 0
        ce = 0

        lines_cov =  re.search(r'Lines executed:(.*)% of (.*)', self.coverage_output)
        if lines_cov is not None:
            lc = float(lines_cov.group(1))

        branches_cov =  re.search(r'Branches executed:(.*)% of (.*)', self.coverage_output)
        if branches_cov is not None:
            bc = float(branches_cov.group(1))

        branches_taken =  re.search(r'Taken at least once:(.*)% of (.*)', self.coverage_output)
        if branches_taken is not None:
            bt = float(branches_taken.group(1))

        calls_executed =  re.search(r'Calls executed:(.*)% of (.*)', self.coverage_output)
        if calls_executed is not None:
            ce = float(calls_executed.group(1))

        return Coverage(lc, bc, bt, ce, 0)

class OptionFuzzer(GrammarCoverageFuzzer):
    link_tools = [ 'link', 'readlink', 'unlink', 'ln']
    link_tools_that_need_the_file = ['readlink', 'unlink']
    mkpipe_tools = ['mkfifo', 'mknod']
    # 这些工具需要来自 stdin 的输入，普通的 subprocess.run 无法从文件重定向，因此我们必须调用 shell
    redirect_in_tools = ["as-new", "bc", "col", "colrm", "dc", "gdb", "tee", "tr", "xargs"]

    def __init__(self, runner, extra_rules=None, invalid_options=False, invalid_values=False, *args, **kwargs):
        assert issubclass(type(runner), OptionRunner)
        self.runner = runner
        self.executable = runner.get_executable()
        self.tool_name = self.executable.split("/")[-1]
        # 其中 self.executable='/usr/bin/ls'，self.tool_name='ls'
        self.cov_class = CovClass(self.executable)
        # 以下 Coverage() 元组包含以下详细信息：[%lines covered, %branches covered, %branches taken, %calls taken, %successful_calls]
        self.base_coverage = Coverage()
        self.manual_test_coverage = Coverage()
        self.fuzz_coverage = dict()
        self.get_manual_test_coverage()
        self.invocation = ""
        self.grammar = runner.grammar()
        if self.grammar is None:
            raise TypeError("Extracted grammar returned None. Cannot proceed with fuzzing")
        super().__init__(self.grammar, *args, **kwargs)

    def check_dir(self):
        dircheck = "FILE"
        dirreference = "FILE_backup"
        emptydir = "FILE/emptydir"
        needs_update_list = []
        # 一开始是没有注释的，但是如果不注释的话就运行不下去
        # if not check_file_existence(dirreference):
        #     raise FileNotFoundError("The reference directory {} wasn't found".format(dirreference))
        if not check_file_existence(dircheck):
            needs_update_list.append(dircheck)
            needs_update_list.append(emptydir) #also add the empty dir
        else:
            #expected st are "0o40777" or "0o40775"
            expected_st = ["0o40777", "0o40775", "0o40755"]
            dc_st = os.stat(dircheck)
            dc_oct_st = oct(dc_st.st_mode)
            dr_st = os.stat(dirreference)
            dr_oct_st = oct(dr_st.st_mode)
            if dr_oct_st not in expected_st:
                raise PermissionError("The reference directory's ({}) ".format(dirreference) + "permissions- {} don't belong in {}".format(dr_oct_st, expected_st))
            if dc_oct_st != dr_oct_st:
                needs_update_list.append(dircheck)
            #check for the empty directory in FILE needed to test only rmdir (not needed for mkdir)
            if not check_file_existence(emptydir):
                needs_update_list.append(emptydir)
        return needs_update_list

    def check_files(self):
        # this filelist is static.
        # can actually be moved to init.
        filelist = ["HelloWorld.py", "README", "emptyfile", "bible.txt", "world192.txt",
                    "testopt", "audio.wav", "largeaudio.wav", "image.jpg", "E.coli",
                    "as.s", "bison.y", "dc.txt", "gdb.txt", "bc.txt"]
        for i in range(30):
            filelist.append("s"+str(i))
        for i in range(30):
            filelist.append("l"+str(i))
        fileprefix = "FILE/"
        referencefileprefix = "FILE_backup/"
        needs_update_list = []
        for f in filelist:
            if not check_file_existence(referencefileprefix + f):
                raise FileNotFoundError("The reference file {} wasn't found".format(referencefileprefix + f))
            if not check_file_existence(fileprefix + f):
                needs_update_list.append(fileprefix + f)
            else:
                expected_st = ["0o100666", "0o100664", "0o100775", "0o100644", "0o100755"]
                fc_st = os.stat(fileprefix + f)
                fc_oct_st = oct(fc_st.st_mode)
                fr_st = os.stat(referencefileprefix + f)
                fr_oct_st = oct(fr_st.st_mode)
                if fr_oct_st not in expected_st:
                    raise PermissionError("The reference file's ({}) ".format(referencefileprefix + f) + "permissions- {} don't belong in {}".format(fr_oct_st, expected_st))
                if fc_oct_st != fr_oct_st:
                    needs_update_list.append(fileprefix + f)
                elif not filecmp.cmp(fileprefix + f, referencefileprefix + f, shallow=False):
                    needs_update_list.append(fileprefix + f)
        return needs_update_list

    def update_files(self, needs_update_list, is_dir):
        for df in needs_update_list:
            path = Path(df)
            if is_dir:
                rm_invocation = ["sudo", "rm", "-rf"]
                cp_invocation = ["cp", "-r"]
            else:
                rm_invocation = ["sudo", "rm", "-f"]
                cp_invocation = ["cp"]
            if path.exists():
                rm_invocation.append(df)
                subprocess.run(rm_invocation)
            copy_from = df.replace("FILE","FILE_backup")
            cp_invocation.append(copy_from)
            cp_invocation.append(df)
            subprocess.run(cp_invocation)

    def remove_linked_file(self):
        if check_file_existence("FILE/linkedfile"):
            rm_invocation = ["sudo", "rm", "-f", "FILE/linkedfile"]
            subprocess.run(rm_invocation)

    def add_linked_file(self):
        softlink_invocation = ["ln", "-s", "HelloWorld.py", "FILE/linkedfile"]
        subprocess.run(softlink_invocation)

    def delete_empty_dir(self):
        if check_file_existence("FILE/emptydir"):
            rmdir_invocation = ["rmdir", "FILE/emptydir"]
            subprocess.run(rmdir_invocation)

    def delete_pipe(self):
        if check_file_existence("FILE/pipe1"):
            rm_invocation = ["rm", "FILE/pipe1"]
            subprocess.run(rm_invocation)

    def run(self, fuzzit=True, random_string_length=100, exclude_whitespace=True):
        runner = self.runner
        assert issubclass(type(runner), OptionRunner)
        if fuzzit:
            # check_dir 函数总是 raise FileNotFoundError，因为程序找不到 FILE_backup
            # update_dir_list = self.check_dir()
            # if update_dir_list:
            #     self.update_files(update_dir_list, True)
            # update_file_list = self.check_files()
            # if update_file_list:
            #     self.update_files(update_file_list, False)
            if self.tool_name in self.link_tools:
                self.remove_linked_file()
            if self.tool_name in self.link_tools_that_need_the_file:
                self.add_linked_file()
            if self.tool_name == "mkdir":
                self.delete_empty_dir()
            if self.tool_name in self.mkpipe_tools:
                self.delete_pipe()
            shell=False
            if self.tool_name in self.redirect_in_tools:
                shell=True
            # self.grammar
            # 对于 ls，fuzzstring=' --dereference'
            # 重要：产生 fuzz 字符串
            fuzzstring = self.fuzz()
            if exclude_whitespace:
                exclude_list = [' ']
            else:
                exclude_list = []
            # 仅当单个选项字符与 str 之间有空格（如果它强制需要 str）时，这才有效
            # 生成随机字符串来放入到选项中
            while re.search("=str\?", fuzzstring) is not None:
                if random.random() > 0.3:
                    rstr = random_string(random_string_length, exclude_list, shell)
                    fuzzstring = fuzzstring.replace("=str?", "=" + rstr, 1)
                else :
                    fuzzstring = fuzzstring.replace("=str?", "", 1)
            while re.search("str\?", fuzzstring) is not None:
                if random.random() > 0.3:
                    rstr = random_string(random_string_length, exclude_list, shell)
                    fuzzstring = fuzzstring.replace("str?", rstr, 1)
                else :
                    fuzzstring = fuzzstring.replace("str?", "", 1)
            # So many rules because "str" can be a substring of some option names
            # e.g. string, strip, strict etc.
            while re.search("=str", fuzzstring) is not None:
                rstr = random_string(random_string_length, exclude_list, shell)
                fuzzstring = fuzzstring.replace("=str", "=" + rstr, 1)

            while re.search(" str", fuzzstring) is not None:
                rstr = random_string(random_string_length, exclude_list, shell)
                fuzzstring = fuzzstring.replace(" str", " " + rstr, 1)

            while re.search("=\"str\"", fuzzstring) is not None:
                rstr = random_string(random_string_length, exclude_list, shell)
                fuzzstring = fuzzstring.replace("=\"str\"", "=\"" + rstr + "\"", 1)

            while re.search(" \"str\"", fuzzstring) is not None:
                rstr = random_string(random_string_length, exclude_list, shell)
                fuzzstring = fuzzstring.replace(" \"str\"", " \"" + rstr + "\"", 1)

            while re.search("str:", fuzzstring) is not None:
                rstr = random_string(random_string_length, exclude_list, shell)
                fuzzstring = fuzzstring.replace("str:", rstr + ":", 1)

            while re.search("/str/", fuzzstring) is not None:
                rstr = random_string(random_string_length, exclude_list, shell)
                fuzzstring = fuzzstring.replace("/str/", "/" + rstr + "/", 1)

            while re.search("str ", fuzzstring) is not None:
                rstr = random_string(random_string_length, exclude_list, shell)
                fuzzstring = fuzzstring.replace("str ", rstr + " ", 1)

            while re.search("str$", fuzzstring) is not None:
                rstr = random_string(random_string_length, exclude_list, shell)
                fuzzstring = re.sub("str$", rstr, fuzzstring, count=1)
            # /usr/bin/ls --dereference
            self.invocation = runner.get_executable() + fuzzstring
        else:
            self.invocation = runner.get_executable()
        # print ('invocation:', self.invocation)
        if shell:
            runner.set_invocation(self.invocation)
        else:
            self.invocation = self.invocation.split(' ')
            runner.set_invocation(self.invocation)
            if self.tool_name == "timeout":
                return runner.run(timeout=100)
        return runner.run(shell=shell)

    def get_base_coverage(self, clear_data="True"):
        successful_run = 0
        if clear_data:
            self.cov_class.clear_coverage_data()
        result, outcome = self.run(False)
        if result.stderr == "":
            successful_run = 1
        self.base_coverage =  Coverage._make(self.cov_class.extract_coverage_data()[0:4] +
                                    (round((successful_run/1)*100, 2),))

    def get_fuzz_coverage(self, inp="", no_runs=20, clear_data=True, print_invocation=True):
        successful_runs = 0

        if clear_data:
            self.cov_class.clear_coverage_data()
            self.reset_coverage()

        for i in range(no_runs):
            result, outcome = self.run(True)
            if print_invocation:
                print(self.invocation)
            if result.stderr == "":
                successful_runs += 1

        coverage = Coverage._make(self.cov_class.extract_coverage_data()[0:4] +
                                        (round((successful_runs/no_runs)*100, 2),))
        self.fuzz_coverage[no_runs] = coverage

    def get_manual_test_coverage(self):
        executable_name = self.executable.split('/')[-1]
        self.manual_test_coverage = ManualTestCov.get(executable_name, Coverage())

    def get_coverage(self):
        return self.cov_class.extract_coverage_data()

# The extracted and expected fuzz coverage values depend on the OS (Linux-Ubuntu/WSL/macOS)
# and the compiler used gcc/clang. I have changed this in the past a lot of times
# to be successful at UT but with such variance, it doesn't make much sense. So, leaving
# this as such for now. Peace.

testlongopt_bc = Coverage(lines_covered=14.55, branches_covered=23.08,
                    branches_taken=11.54, calls_executed=5.26, successful_calls=100.0)

testlongopt_fc = {20: Coverage(lines_covered=85.45, branches_covered=92.31,
                    branches_taken=80.77, calls_executed=78.95, successful_calls=100.0)}

testopt_bc = Coverage(lines_covered=25.71, branches_covered=23.53,
                    branches_taken=11.76, calls_executed=16.67, successful_calls=100.0)

testopt_fc = {20: Coverage(lines_covered=80.0, branches_covered=88.24,
                branches_taken=64.71, calls_executed=58.33, successful_calls=35.0)}

if __name__ == "__main__":
    # testopt is tested with invalid options
    torunner = OptionRunner("tests/testopt")
    tofuzzer = OptionFuzzer(torunner, max_nonterminals=5, invalid_options=True)
    tofuzzer.get_base_coverage(clear_data=True)
    print ("testopt base coverage:", tofuzzer.base_coverage)
    # fuzzes testopt 20 times
    tofuzzer.get_fuzz_coverage(clear_data=True, print_invocation=False)
    print ("Extracted testopt coverage:")
    pprint(tofuzzer.fuzz_coverage)
    print ("Expected testopt coverage:")
    pprint(testopt_fc)

    # testlongopt is tested with only valid options
    tlorunner = OptionRunner("tests/testlongopt")
    tlofuzzer = OptionFuzzer(tlorunner, max_nonterminals=5)
    tlofuzzer.get_base_coverage(clear_data=True)
    print ("testlongopt base coverage:", tlofuzzer.base_coverage)
    # fuzzes testopt 20 times
    tlofuzzer.get_fuzz_coverage(clear_data=True, print_invocation=False)
    print ("Extracted testlongopt coverage:")
    pprint(tlofuzzer.fuzz_coverage)
    print ("Expected testlongopt coverage:")
    pprint(testlongopt_fc)
