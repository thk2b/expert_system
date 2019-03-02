#!/usr/local/bin/python3

from execute import execute_file, execute_interactive
import argparse

def main(args):
    if len(args.filenames) == 0:
        return execute_interactive()
    for filename in args.filenames:
        print(filename, end=':\n')
        execute_file(filename)
        print()
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser('expert_system')
    parser.add_argument('--verbose', '-v', action='store_true', help='verbose mode')
    parser.add_argument('filenames', metavar='filename', type=str, nargs='*', help='file to execute (default: stdin)', default=[])
    main(parser.parse_args())
