#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function

import argparse

ext = '.mbx-script-output'

if __name__ == '__main__':
    desc = 'Calculate set operation set1 - set2'
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument(
        '--sep', metavar='SEPARATOR', choices=[],
        help='overwriting existing files if needed')

    parser.add_argument(
        'filenames', metavar='DATA-file', nargs='+',
        help='an input data file')

    args = parser.parse_args()

    for filename in args.filenames:
        filename_out = filename + ext
