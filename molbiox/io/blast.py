
from collections import OrderedDict

__author__ = 'Hailong'


FMT7_FIELDS = [
    ('query.id',         None),
    ('subject.id',       None),
    ('identity',         float),
    ('alignment.length', int),
    ('mismatches',       int),
    ('gap.opens',        int),
    ('q.start',          int),
    ('q.end',            int),
    ('s.start',          int),
    ('s.end',            int),
    ('evalue',           float),
    ('bit.score',        float),
]


def read_fmt6(handle, fields=FMT7_FIELDS):
    return read_fmt7(handle, fields=fields)


def read_fmt7(handle, fields=FMT7_FIELDS):

    if hasattr(handle, 'read'):
        infile = handle
    else:
        infile = open(handle)

    for line in infile:
        if line.startswith('#'):
            continue
        values = line.strip().split('\t')
        if len(values) != len(fields):
            raise ValueError('Too few or too many values in data file')
        pairs = []
        for (key, type_), val in zip(fields, values):
            if type_:
                val = type_(val)
            pairs.append((key, val))
        yield OrderedDict(pairs)

    if infile is not handle:
        infile.close()

