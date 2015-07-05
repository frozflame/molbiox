#!/usr/bin/env python3
# encoding: utf-8

import os
import sys

# be Python 3 compatible
if sys.version.startswith('3'):
    zrange = range
else:
    zrange = xrange


def read(filename):
    """
    Read a FASTQ file and yield dicts.

    Say we have

        @HWI-ST1426:113:HGTH7ADXX:1:1101:1358:2170 1:N:0:ATCACG
        ATATGAGGACAAACGATAATACCGCCGCCTTGGTTATCTAGGATCTCTTGAA...
        +
        BBBFFFFFFFFFFIIIIIIIIIIIIIIIIIIIIFIIIIIIIIIIIIIIIIII...

    Then we will get

        {
            'title': 'HWI-ST1426:113:HGTH7ADXX:1:1101:1358:2170 1:N:0:ATCACG',
            'sequence': 'ATATGAGGACAAACGATAATACCGCCGCCTTGGTTATCTAGGATCTCT...',
            'qualiseq': 'BBBFFFFFFFFFFIIIIIIIIIIIIIIIIIIIIFIIIIIIIIIIIIII...',
        }

    """

    # input FASTQ file
    infile = open(filename)

    while True:
        title = infile.readline().strip()
        sequence = infile.readline().strip()
        plussign = infile.readline().strip()
        qualiseq = infile.readline().strip()

        if not title:
            break
        if not title.startswith('@') or plussign != '+':
            raise ValueError('fastq file "{}" is corrupted'.format(filename))
        yield dict(title=title[1:], sequence=sequence, qualiseq=qualiseq)


def write(filename, seqdicts, linesep=os.linesep):
    outfile = open(filename, 'w')
    template = '@{title}{eol}{sequence}{eol}+{qualiseq}{eol}'
    for seqdict in seqdicts:
        block = template.format(eol=linesep, **seqdict)
        outfile.write(block)

