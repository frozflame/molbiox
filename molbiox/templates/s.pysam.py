#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function

import argparse
import pysam


desc = 'MBX Script'
parser = argparse.ArgumentParser(description=desc)

parser.add_argument(
    'filename', metavar='BAM-file', help='an input BAM file')

args = parser.parse_args()


samfile = pysam.AlignmentFile(args.filename, "rb")

# list of reference contigs
contigs = samfile.references


ref = contigs[0]
for read in samfile.fetch(ref, 0, 1000):
    mate = samfile.mate(read)
    if mate.reference_id != read.reference_id:
        print(contigs[read.reference_id])
        print(contigs[mate.reference_id])
