#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
from molbiox.iofmt.tabular import LGrouper

import os
import sys
import argparse

ext = '.lgrouped'
col = 2


def groupby_func(line):
    if line.startswith('#'):
        return '#'
    else:
        return line.split()[col]


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

        if not args.rude and os.path.exists(filename_out):
            message = 'Fail: "{}" exists already'.format(filename_out)
            print(message, file=sys.stderr)
            continue

        lgrouper = LGrouper(groupby_func)
        for l in open(filename):
            lgrouper.feed(l.strip())

        outfile = open(filename_out, 'w')
        for l in lgrouper.harvest():
            print(l, file=outfile)
