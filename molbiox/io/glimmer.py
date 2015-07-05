#!/usr/bin/env python3
# encoding: utf-8

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

def read_g3_predict(filename):

    title = 'Anonymous.CONTIG'

    # input FASTA file
    infile = open(filename)

    for line in infile:
        line = line.strip()

        if line.startswith('>'):
            title = title or 'Anonymous.CONTIG'
            continue
        else:
            values = line.strip().split()
            if len(values) != len(GLIMMER3_FIELDS):
                raise ValueError('Too few or too many values in data file')

            pairs = [('title', title)]
            for (key, type_), val in zip(GLIMMER3_FIELDS, values):
                if type_:
                    val = type_(val)
                pairs.append((key, val))
            contig = re.sub(r'\s+', '_', title)
            pairs.insert(1, ('contig', contig))
            yield OrderedDict(pairs)

