#!/usr/bin/env python3
# encoding: utf-8

import os

from molbiox.frame.containers import SDict
from molbiox.frame import compat, interactive


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

    with compat.FileWrapper(infile, 'r') as fw:
        while True:
            cmt = fw.file.readline().strip()
            seq = fw.file.readline().strip()
            plus = fw.file.readline().strip()
            qual = fw.file.readline().strip()

            if not cmt:
                break
            if not cmt.startswith('@') or plus != '+':
                raise ValueError('fastq file <{}> is corrupted'.format(fw.path))
            yield SDict(cmt=cmt[1:], seq=seq, qual=qual)


def readone(infile):
    return read(infile, castfunc=0)


def readseq(infile):
    return read(infile, castfunc=0).seq


def write(outfile, seqdicts, linesep=os.linesep):
    # `handle` is either a file object or a string

    with compat.FileWrapper(outfile, 'w') as fw:
        template = '@{cmt}{eol}{seq}{eol}+{qual}{eol}'
        for seqdict in seqdicts:
            block = template.format(eol=linesep, **seqdict)
            fw.file.write(block)

# TODO
# <instrument>:<run number>:<flowcell ID>:<lane>:<tile>
# :<x-pos>:<y-pos> <read>:<is filtered>:<control number>:<index sequence>
# http://support.illumina.com/help/SequencingAnalysisWorkflow/Content/Vault/Informatics/Sequencing_Analysis/CASAVA/swSEQ_mCA_FASTQFiles.htm
