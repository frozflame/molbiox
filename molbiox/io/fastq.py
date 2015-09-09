#!/usr/bin/env python3
# encoding: utf-8

import os
import sys
from molbiox import tolerant

# be Python 3 compatible
if sys.version.startswith('3'):
    zrange = range
else:
    zrange = xrange

@tolerant.castable
def read(handle):
    """
    Read a FASTQ file and yield dicts.

    Say we have

        @HWI-ST1426:113:HGTH7ADXX:1:1101:1358:2170 1:N:0:ATCACG
        ATATGAGGACAAACGATAATACCGCCGCCTTGGTTATCTAGGATCTCTTGAA...
        +
        BBBFFFFFFFFFFIIIIIIIIIIIIIIIIIIIIFIIIIIIIIIIIIIIIIII...

    Then we will get

        {
            'cmt':  'HWI-ST1426:113:HGTH7ADXX:1:1101:1358:2170 1:N:0:ATCACG',
            'seq':  'ATATGAGGACAAACGATAATACCGCCGCCTTGGTTATCTAGGATCTCT...',
            'qual': 'BBBFFFFFFFFFFIIIIIIIIIIIIIIIIIIIIFIIIIIIIIIIIIII...',
        }

    """

    # `handle` is either a file object or a string
    if hasattr(handle, 'write'):
        infile = handle
    else:
        infile = open(handle, 'w')

    while True:
        cmt = infile.readline().strip()
        seq = infile.readline().strip()
        plus = infile.readline().strip()
        qual = infile.readline().strip()

        if not cmt:
            break
        if not cmt.startswith('@') or plus != '+':
            raise ValueError('fastq file "{}" is corrupted'.format(handle))
        yield dict(cmt=cmt[1:], seq=seq, qual=qual)

    if infile is not handle:
        infile.close()


def read1(handle):
    return read(handle, castfunc=0)


def write(handle, seqdicts, linesep=os.linesep):
    # `handle` is either a file object or a string
    if hasattr(handle, 'write'):
        outfile = handle
    else:
        outfile = open(handle, 'w')

    template = '@{cmt}{eol}{seq}{eol}+{qual}{eol}'
    for seqdict in seqdicts:
        block = template.format(eol=linesep, **seqdict)
        outfile.write(block)

    if outfile is not handle:
        outfile.close()


# TODO
# <instrument>:<run number>:<flowcell ID>:<lane>:<tile>:<x-pos>:<y-pos> <read>:<is filtered>:<control number>:<index sequence>
# http://support.illumina.com/help/SequencingAnalysisWorkflow/Content/Vault/Informatics/Sequencing_Analysis/CASAVA/swSEQ_mCA_FASTQFiles.htm
