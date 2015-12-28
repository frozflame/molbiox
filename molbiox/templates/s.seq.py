#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function

import sys
import argparse

from molbiox.io import fasta

ext = '.out.fa'

def handle_file(filename):
    # TODO: --rude option
    outfile = open(filename + ext)
    for seqrecord in fasta.read(filename):
        fasta.write(outfile, seqrecord)

if __name__ == '__main__':
    desc = 'MBX Script'
    parser = argparse.ArgumentParser(description=desc)

    # parser.add_argument(
    #     '--rude', action='store_true',
    #     help='overwriting existing files if needed')

    parser.add_argument(
        'filenames', metavar='FASTA-file', nargs='+',
        help='an input data file')

    args = parser.parse_args()

    for filename in args.filenames:
        try:
            handle_file(filename)
        except:
            print('fail: {}'.format(filename), file=sys.stderr)
