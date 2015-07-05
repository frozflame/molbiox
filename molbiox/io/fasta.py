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

    title = ''

    # input FASTA file
    infile = open(filename)

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


def write(filename, seqdicts, linesep=os.linesep, linewidth=60):
    """
    Reverse of `fasta.read`.

    :param filename: path of the output FASTA file
    :param seqdicts: an iterable like
        [{'title': 'SEQ1', 'sequence': 'ATCTC...T'}, ...]
    :return: None
    """
    outfile = open(filename, 'w')
    for seqdict in seqdicts:
        outfile.write(seqdict['title'])
        outfile.write(linesep)
        sequence = seqdict['sequence']
        for i in zrange(0, len(sequence), linewidth):
            outfile.write(sequence[i:i+linewidth])
            outfile.write(linesep)
    outfile.close()

