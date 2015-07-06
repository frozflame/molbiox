#!/usr/bin/env python3
# encoding: utf-8

import os
import sys
import re
from collections import OrderedDict

# be Python 3 compatible
if sys.version.startswith('3'):
    zrange = range
else:
    zrange = xrange

__author__ = 'Hailong'

GLIMMER3_FIELDS = [
    ('orf',     None),
    ('head',    int),
    ('tail',    int),
    ('frame',   int),
    ('score',   float),
]

def read_g3_predict(handle):
    """
    Parse $TAG.predict file generated by glimmer3

    :param handle: a file-like object or path to the $TAG.predict file
    :return: None
    """

    contig = 'A.CONTIG'

    # `handle` is either a file object or a string
    if hasattr(handle, 'read'):
        infile = handle
    else:
        infile = open(handle)

    for line in infile:
        line = line.strip()

        if line.startswith('>'):
            contig = line.strip()[1:] or 'A.CONTIG'
            continue
        else:
            values = line.strip().split()
            if len(values) != len(GLIMMER3_FIELDS):
                raise ValueError('Too few or too many values in data file')

            pairs = []
            for (key, type_), val in zip(GLIMMER3_FIELDS, values):
                if type_:
                    val = type_(val)
                pairs.append((key, val))

            pairs.insert(1, ('contig', contig))
            yield OrderedDict(pairs)

    # close the file only if it is opened within this func
    if infile is not handle:
        infile.close()


def write_g3_mcoordz(handle, predicts, sep='\t', linesep=os.linesep):
    """
    Generate coord file required by

        glimmer3/3.02b/libexec/multi-extract

    :param handle: a file-like object or path to the output coord file
    :param predicts: an iterable as generated by `read_g3_predict`
    :return: None
    """

    # TODO: open mode `w` or `wb`?
    # `handle` is either a file object or a string
    if hasattr(handle, 'write'):
        outfile, newfile = handle, False
    else:
        outfile = open(handle, 'w')

    for predict in predicts:
        line = sep.join(str(x) for x in predict.values())
        # todo: newline as parameter
        outfile.write(line + linesep)

    # close the file only if it is opened within this func
    if outfile is not handle:
        outfile.close()
