#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function

import itertools
from collections import OrderedDict
from molbiox.frame import interactive


@interactive.castable
def read(infile, fieldlist=None, sep=None):
    """
    Read a tabular text file
    :param infile: a file object or a file path
    :param fieldlist: [(fieldname, fieldtype), ...] see `io/blast` for examples
    :param sep: separator use in `string.split(sep)`
    :return: a generator, yielding OrderedDict objects
    """
    fw = interactive.FileWrapper(infile, 'r')

    # if fieldlist is NOT given, generate list-like dicts
    if not fieldlist:
        fieldlist = ((i, None) for i in itertools.count())

    for line in fw.file:
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        values = line.split(sep, maxsplit=len(fieldlist)-1)

        if len(values) < len(fieldlist):
            raise ValueError('too few columns in data file')

        pairs = []
        for (key, cast), val in zip(fieldlist, values):
            if cast is not None:
                val = cast(val)
            pairs.append((key, val))

        yield OrderedDict(pairs)
    fw.close()


@interactive.castable
def read_lenfile(infile, multi=False):
    """
    Parse file format like `wc` or `fastalength` output

    Say we have

        264531 2045177 65877908 google.chrome.dmg
        181167 1408149 48452451 picasa.mac.39.dmg
        ...

    Then we will get

        {
            'google.chrome.dmg': 264531,
            'picasa.mac.39.dmg': 181167,
        }

    Or if `multi` is True

        {
            'google.chrome.dmg': (264531, 2045177, 65877908),
            'picasa.mac.39.dmg': (181167, 1408149, 48452451),
        }

    :param infile: a file object or a file path
    :param multi: boolean
    :return: a generator, yielding OrderedDict objects
    """

    fw = interactive.FileWrapper(infile, 'r')
    resdict = dict()
    for line in fw.file:
        line = line.strip()

        # skip empty line or comment
        if not line or line.startswith('#'):
            continue

        itemlist = line.split()
        key = itemlist[-1]

        if multi:
            val = tuple(int(x) for x in itemlist[:-1])
        else:
            val = int(itemlist[0])
        resdict[key] = val
    fw.close()
    return resdict


class LGrouper(object):
    def __init__(self, groupby):
        self.lines = []
        self.groupby = groupby
        self.lastkey = None

    def feed(self, line):
        key = self.groupby(line)
        if key != self.lastkey:
            self.lastkey = key
            self.lines.append('')
        self.lines.append(line)

    def harvest(self):
        lines = self.lines
        self.lines = []
        return lines


