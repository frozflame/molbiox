#!/usr/bin/env python3
# encoding: utf-8

import os
import sys

from molbiox.frame import interactive


@interactive.castable
def read(infile):
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

    :param infile: a file object or path
    :return: a generator
    """

    fw = interactive.FileWrapper(infile, 'r')

    while True:
        cmt = fw.file.readline().strip()
        seq = fw.file.readline().strip()
        plus = fw.file.readline().strip()
        qual = fw.file.readline().strip()

        if not cmt:
            break
        if not cmt.startswith('@') or plus != '+':
            raise ValueError('fastq file <{}> is corrupted'.format(fw.path))
        yield dict(cmt=cmt[1:], seq=seq, qual=qual)

    fw.close()


def read1(infile):
    return read(infile, castfunc=0)


def write(outfile, seqdicts, linesep=os.linesep):
    # `handle` is either a file object or a string

    # TODO: binary?
    fw = interactive.FileWrapper(outfile, 'w')

    template = '@{cmt}{eol}{seq}{eol}+{qual}{eol}'
    for seqdict in seqdicts:
        block = template.format(eol=linesep, **seqdict)
        fw.file.write(block)
    fw.close()

# TODO
# <instrument>:<run number>:<flowcell ID>:<lane>:<tile>
# :<x-pos>:<y-pos> <read>:<is filtered>:<control number>:<index sequence>
# http://support.illumina.com/help/SequencingAnalysisWorkflow/Content/Vault/Informatics/Sequencing_Analysis/CASAVA/swSEQ_mCA_FASTQFiles.htm
