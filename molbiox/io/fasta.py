#!/usr/bin/env python3
# encoding: utf-8

import os
import re
import six
from molbiox.frame import interactive
from molbiox.frame.common import SRecord
from molbiox.frame.compat import omni_writer


@interactive.castable
def read(infile, concise=True):
    """
    Reading a FASTA file should NOT be complicated!

    :param infile: a file object or a string
    :param concise: remove chars after first whitespace in cmt field
    :return: a generator of SRecord objects

    Say we have

        >ORF00024
        ATCTGTCCTACTCCCGTC...TC
        >ORF00025
        GTCTGTCCTACTCCCGTC...TC

    Then we will get

        [
            {
                'cmt': 'ORF00024',
                'seq': 'ATCTGTCCTACTCCCGTC...TC'
            },
            {
                'cmt': 'ORF00025',
                'seq': 'GTCTGTCCTACTCCCGTC...TC'
            }
        ]

    Nothing frustrates you. If you want to iterate through a multi-seq FASTA
    file a second time, `itertools.tee` may help you:

        seqiter = fasta.read('contigs.fas')
        seqiter, seqiter1 = itertools.tee(seqiter)

        for seqrecord in seqiter:
            print(seqrecord['cmt'], len(seqrecord['seq']))

        for seqrecord in seqiter1:
            print(seqrecord['cmt'], len(seqrecord['seq']))
    """

    # if hasattr(handle, 'read'):
    #     infile = handle
    # else:
    #     infile = open(handle)

    fw = interactive.FileWrapper(infile, 'r')

    cmt = 'anonym.0'
    beg = '>'
    if 'b' in fw.file.mode:
        cmt = cmt.encode('ascii')
        beg = beg.encode('ascii')

    # sequence lines not yielded
    seqlines = []

    # anonymous count
    anonym = 0

    for line in fw.file:
        line = line.strip()

        # a new sequence in a multi-seq fasta
        if line.startswith(beg):
            seq = ''.join(seqlines)
            if seq:
                # yield previous sequence
                # a record with empty seq is discarded
                yield SRecord(cmt=cmt, seq=seq)

            # begin a new sequence
            seqlines = []
            cmt = line[1:]
            if not cmt:
                anonym += 1
                cmt = 'anonym.{}'.format(anonym)
            if concise:
                cmt = cmt.split()[0]
        else:
            seqlines.append(line)

    # yield last sequence
    if seqlines:
        yield SRecord(cmt=cmt, seq=''.join(seqlines))
    fw.close()


def read1(infile, concise=True):
    return read(infile, concise, castfunc=0)


def readseq(infile):
    return read(infile, castfunc=0)['seq']


def write(outfile, records, linesep=os.linesep, linewidth=60):
    """
    Reverse of `fasta.read`.

    :param outfile: a file-like object or path to the output FASTA file
    :param records: an iterable like [{'cmt': 'SEQ1', 'seq': 'ATCTC...T'}, ...]
    :param linesep: newline symbol
    :param linewidth: default 60
    :return: a generator
    """
    # TODO: open mode `w` or `wb`?
    # TODO: use binary project wide
    fw = interactive.FileWrapper(outfile, 'w')

    # accept a single record
    if isinstance(records, dict):
        records = [records]

    for record in records:
        cmtline = '>{}{}'.format(record['cmt'], linesep)
        omni_writer(fw.file, cmtline)
        seq = record['seq']
        for i in six.moves.range(0, len(seq), linewidth):
            omni_writer(fw.file, seq[i:i+linewidth])
            omni_writer(fw.file, linesep)
    fw.close()


def fix_comment(cmt, prefix='', suffix=''):
    """
    Fix seqrecord comment

        >(prefix)Key(suffix) other_descriptions
        ATTCGGGGGTCTGGCTAG...
    """
    regex_key = re.compile(r'^\S+')
    return regex_key.sub(prefix + r'\g<0>' + suffix, cmt)


def fix_filename(name, prefix='', suffix=''):
    """
    Remove common fasta extensions and join with prefix & suffix

        (prefix)N2700.contigs<.fa>(suffix)
    """
    regex_ext = re.compile(r'\.(fa|fas|fasta|fna|ffn|faa|frn)$')
    return prefix + regex_ext.sub('', name) + suffix


def match_contig_name(names, keyword):
    keyword = re.escape(keyword)
    regex = re.compile(r'^(.*[^a-zA-Z0-9]+)?' + keyword + '([^a-zA-Z0-9]+.*)?$', re.I)
    for name in names:
        if regex.match(name):
            return name
