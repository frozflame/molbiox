#!/usr/bin/env python3
# encoding: utf-8

import os
from molbiox.compat import zrange


def read(handle):
    """
    Reading a FASTA file should NOT be complicated!

    Say we have

        >ORF00024
        ATCTGTCCTACTCCCGTC...TC
        >ORF00025
        GTCTGTCCTACTCCCGTC...TC

    Then we will get

        [
            {
                'count': 0,
                'title': 'ORF00024',
                'sequence': 'ATCTGTCCTACTCCCGTC...TC'
            },
            {
                'count': 1,
                'title': 'ORF00025',
                'sequence': 'GTCTGTCCTACTCCCGTC...TC'
            }
        ]

    Nothing frustrates you. If you want to iterate through a multi-seq FASTA
    file a second time, `itertools.tee` may help you:

        seqiter = fasta.read('contigs.fas')
        seqiter, seqiter1 = itertools.tee(seqiter)

        for seqdict in seqiter:
            print(seqdict['title'], len(seqdict['sequence']))

        for seqdict in seqiter1:
            print(seqdict['title'], len(seqdict['sequence']))
    """

    # `handle` is either a file object or a string
    if hasattr(handle, 'read'):
        infile = handle
    else:
        infile = open(handle)

    title = ''

    # sequence lines not yielded
    seqlines = []
    for line in infile:
        line = line.strip()

        # a new sequence in a multi-seq fasta
        if line.startswith('>'):
            if seqlines:
                # yield previous sequence
                title = title or 'Anonymous.SEQ'
                sequence = ''.join(seqlines)
                yield dict(title=title, sequence=sequence)
            # begin a new sequence
            title = line[1:]
            seqlines = []

        else:
            seqlines.append(line)

    # yield last sequence
    if seqlines:
        yield dict(title=title, sequence=''.join(seqlines))

    # close the file only if it is opened within this func
    if infile is not handle:
        infile.close()


def write(handle, seqdicts, linesep=os.linesep, linewidth=60):
    """
    Reverse of `fasta.read`.

    :param handle: a file-like object or path to the output FASTA file
    :param seqdicts: an iterable like
        [{'title': 'SEQ1', 'sequence': 'ATCTC...T'}, ...]
    :return: None
    """
    # TODO: open mode `w` or `wb`?
    # `handle` is either a file object or a string
    if hasattr(handle, 'write'):
        outfile = handle
    else:
        outfile = open(handle, 'w')

    # accept a single seqdict
    if isinstance(seqdicts, dict):
        seqdicts = [seqdicts]

    for seqdict in seqdicts:
        tline = '>{}{}'.format(seqdict['title'], linesep)
        outfile.write(tline)
        sequence = seqdict['sequence']
        for i in zrange(0, len(sequence), linewidth):
            outfile.write(sequence[i:i+linewidth])
            outfile.write(linesep)

    # close the file only if it is opened within this func
    if outfile is not handle:
        outfile.close()

