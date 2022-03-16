import random
import utils
import argparse
import string

def write_to_file(filename, length, exclude_list=[], printable=False):
    lower_range = 0
    upper_range = 255
    print("generating", filename)
    fileob = open(filename, 'wb', 0)
    for i in range(length):
        if printable:
            a = random.choice(string.printable)
        else:
            a = chr(random.randint(lower_range, upper_range))
        while a in exclude_list:
            if printable:
                a = random.choice(string.printable)
            else:
                a = chr(random.randint(lower_range, upper_range))
        fileob.write(a.encode('latin1'))
    fileob.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate input files (30 small sfiles and 30 large lfiles) for fuzzing',
                                    formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--no-newlines", help="Input files won't have newlines at all",
                            action="store_true")
    parser.add_argument("-p","--printable", help="Generate files of only printable characters (ASCII 32-126)",
                            action="store_true")
    parser.add_argument("--seed", help="Seed number for randomising")
    ex_group = parser.add_mutually_exclusive_group()
    ex_group.add_argument("--length", type=int,
        help="Set bytelength of generated sfiles and lfiles to fixed user defined value")
    ex_group.add_argument("--length-level", type=int, choices=[1, 2, 3, 4],
                    default=1,
                    help=
'''Alternately, select bytelength of generated files. Default level=1.
level 1: sfiles-size=100, lfiles-size=10000,
level 2: sfiles-size=10000, lfiles-size=1000000,
level 3: sfiles-size=100000, lfiles-size=10000000,
level 4: sfiles-size=1000000, lfiles-size=100000000''')
    args = parser.parse_args()
    file_prefix = "FILE_backup/"
    sfile_prefix = file_prefix + "s"
    lfile_prefix = file_prefix + "l"

    if args.seed:
        random.seed(args.seed)
    else:
        random.seed(utils.RANDOM_SEED)

    if args.length:
        s_size = args.length
        l_size = args.length
    else:
        if args.length_level == 1:
            s_size = 100
            l_size = 10000
        elif args.length_level == 2:
            s_size = 10000
            l_size = 1000000
        elif args.length_level == 3:
            s_size = 100000
            l_size = 10000000
        elif args.length_level == 4:
            s_size = 1000000
            l_size = 100000000

    for i in range(30):
        if args.no_newlines and args.printable:
            write_to_file(sfile_prefix + str(i), s_size, ['\n'], True)
        elif args.no_newlines:
            write_to_file(sfile_prefix + str(i), s_size, ['\n'])
        elif args.printable:
            write_to_file(sfile_prefix + str(i), s_size, [], True)
        else:
            write_to_file(sfile_prefix + str(i), s_size)

    for i in range(30):
        if args.no_newlines and args.printable:
            write_to_file(lfile_prefix + str(i), l_size, ['\n'], True)
        elif args.no_newlines:
            write_to_file(lfile_prefix + str(i), l_size, ['\n'])
        elif args.printable:
            write_to_file(lfile_prefix + str(i), l_size, [], True)
        else:
            write_to_file(lfile_prefix + str(i), l_size)