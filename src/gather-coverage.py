import os
import subprocess
import sys
import re
from pprint import pprint

coverage_data = []
total_statement_sum = 0
total_no_of_statements = 0
no_of_files = 0
total_branches_sum= 0
total_no_of_branches = 0

def clear_coverage_data(path):
    invocation =  "rm -f " + path
    dlt_call = subprocess.run(invocation.split(), stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    universal_newlines=True)

    if dlt_call.returncode != 0 or dlt_call.stderr != "" :
        print ("The subprocess rm call returned {} with the following stderr:\n{}".format(dlt_call.returncode,
                                                                                            dlt_call.stderr))
        sys.exit(1)

def run_coverage(path, get_branches=True):
    executable = path
    gcov_options = ""
    if get_branches:
        gcov_options = "-b "
    invocation =  "gcov " + gcov_options + executable
    gcov_call = subprocess.run(invocation.split(), stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    universal_newlines=True)
    if gcov_call.returncode != 0 or gcov_call.stdout == "":
        print ("The subprocess gcov call returned {} with the following stderr:\n{}".format(gcov_call.returncode,
                gcov_call.stderr))
        return ""
    else:
        gcov_list = gcov_call.stdout.split("\n\n")
        return gcov_list
        # for file_coverage in gcov_list:
        #     if os.path.basename(executable) in file_coverage.split('\n')[0]:
        #         self.coverage_output = file_coverage

    if gcov_call.returncode == 0 and gcov_call.stderr != "":
        print("The subprocess gcov call returned 0 with stderr:\n{}".format(gcov_call.stderr))

def extract_coverage_data(filepath, gcovdata_list):
    if type(gcovdata_list) is not list:
        lines_executed = "cov returned a non list:"
        total_lines = str(type(gcovdata_list))
        coverage_data.append((filepath, lines_executed, total_lines, 'NaN', 'NaN', 'Nan'))
    else:
        for data_para in gcovdata_list:
            if data_para == '':
                continue
            data = data_para.split('\n')
            filename = data[0].split(' ')[1]
            if "/usr/" in filename:
                continue # we skip extracting coverage from globally shared libraries
            lines_cov =  re.search(r'Lines executed:(.*)% of (.*)', data[1])
            if lines_cov is not None:
                lines_executed = lines_cov.group(1)
                total_lines = lines_cov.group(2)
                global total_statement_sum, total_no_of_statements, no_of_files
                total_statement_sum += float(lines_executed)
                total_no_of_statements += int(total_lines)
                no_of_files += 1
            else:
                if re.search(r'No executable lines', data[1]) is not None:
                    lines_executed = '0.00'
                    total_lines = '0.00'
                    continue # No executable lines -> no branches
                else:
                    lines_executed = "cov couldn't be collected. check manually"
                    total_lines = data[1]
            
            branch_cov = re.search(r'Branches executed:(.*)% of (.*)', data[2])
            if branch_cov is not None:
                branches_executed = branch_cov.group(1)
                total_branches = branch_cov.group(2)
                global total_branches_sum, total_no_of_branches
                total_branches_sum += float(branches_executed)
                total_no_of_branches += int(total_branches)
            else:
                if re.search(r'No branches', data[2]) is not None:
                    branches_executed = '0.00'
                    total_branches = '0.00'
                else:
                    branches_executed = "Branch coverage couldn't be collected. check manually"
                    total_branches = data[2]

            coverage_data.append((filepath, filename, lines_executed, total_lines,
                                branches_executed, total_branches))

if len(sys.argv) < 2:
    print('''Usage: python3 gather-coverage.py <path to directory>''')
    sys.exit(1)

'''
cov_output = run_coverage(sys.argv[1])
print("cov_output:", cov_output)
extract_coverage_data(sys.argv[1], cov_output)
pprint(coverage_data)
print(no_of_files)
'''
for dirpath, dirnames, filenames in os.walk(sys.argv[1]):
    for filename in filenames:
        # print(os.path.splitext(f))
        if os.path.splitext(filename)[1] == ".gcda":
            filepath = os.path.join(dirpath, filename)
            cov_output = run_coverage(filepath)
            extract_coverage_data (filepath, cov_output)
# pprint(coverage_data)

print('filepath, filename, statement coverage %, total statements, branch coverage %, total branches')
for (a, b, c, d, e, f) in coverage_data:
    print (a + ', ' +  b + ', ' +c + ', ' + d + ', ' + e + ', ' + f)
print("directory,", os.path.abspath(os.getcwd()))
print("total_no_of_statements,", total_no_of_statements)
print("total_statement_coverage_%, {:.2f}%".format(total_statement_sum/no_of_files))
print("total_no_of_branches,", total_no_of_branches)
print("total_branch_coverage_%, {:.2f}%".format(total_branches_sum/no_of_files))
# '''
