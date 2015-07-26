#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function

import argparse

# from molbiox.tolerant import safe_bracket

ext = '.mbx-script-output'

def displ(line):
    print(line)


if __name__ == '__main__':
    desc = 'MBX Script'
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument(
        '--rude', action='store_true',
        help='overwriting existing files if needed')

    parser.add_argument(
        'filenames', metavar='DATA-file', nargs='+',
        help='an input data file')

    args = parser.parse_args()

    for filename in args.filenames:
        filename_out = filename + ext

        infile = open(filename)
        outfile = open(filename_out, 'w')

        # ~ code ~

        infile.close()
        outfile.close()
