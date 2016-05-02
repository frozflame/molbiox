#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function

import collections
import itertools

import six
import dataset

from molbiox.frame import containers, streaming, interactive


class DummyStructure(object):
    def __init__(self, prefix=None, castfuncs=None):
        """
        :param prefix: prefix for column names
        :param castfuncs: a list of functions

        If `prefix` is provided,
        columns are named as "{prefix}0", "{prefix}1" ... (strings)
        If `prefix` is not provided,
        columns are named as 0, 1, ... (integers)

        Try to convert with each function in `castfuncs` until success;
        otherwise keep the original value
        """
        self.prefix = prefix
        self.castfuncs = castfuncs

    def __len__(self):
        return 0

    def c(self, i):
        return '{}{}'.format(self.prefix, i)

    def cast(self, item):
        for castfunc in self.castfuncs:
            try:
                return castfunc(item)
            except:
                pass
        return item

    def __iter__(self):
        cast = self.cast if self.castfuncs else None
        if self.prefix is None:
            return ((i, cast) for i in itertools.count())
        else:
            return ((self.c(i), cast) for i in itertools.count())


@interactive.castable
def read(infile, structure=None, sep=None, comment=None):
    """
    Read a tabular text file
    :param infile: a file object or a file path
    :param structure: [(fieldname, fieldtype), ...] see `io/blast` for examples
    :param sep: separator use in `string.split(sep)`
    :param comment: regex for comments
    :return: a generator, yielding TabRecord objects
    """

    # if structure is NOT given, generate list-like dicts
    if structure is None:
        structure = DummyStructure()
    numfields = len(structure)
    # attributes = {x for x, _ in structure}

    with streaming.FileAdapter.new(infile, 'r') as fila:
        for line in fila:
            line = line.strip()
            if not line:
                continue
            if comment and comment.search(line):
                continue

            values = line.split(sep, numfields - 1)

            if numfields and len(values) < numfields:
                raise ValueError('too few columns in data file')

            pairs = []
            for (key, cast), val in zip(structure, values):
                if cast is not None:
                    val = cast(val)
                pairs.append((key, val))
            tabrec = containers.TabRecord(pairs)
            # tabrec.attributes = attributes
            yield tabrec


@interactive.castable
def read_lentab(infile, multi=False):
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
    :return: an OrderedDict
    """

    with streaming.FileAdapter(infile, 'r') as fw:
        resdict = collections.OrderedDict()
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
        return resdict


@interactive.castable
def read_blasttab(infile, fmt='6m'):
    from molbiox.kb import blast
    if not fmt.startswith('fmt'):
        fmt = 'fmt' + fmt
    try:
        fieldlist = getattr(blast, fmt)
    except AttributeError:
        errmsg = 'invalid blast tabular format: fmt={}'.format(repr(fmt))
        raise ValueError(errmsg)
    return read(infile, fieldlist)


@interactive.castable
def read_vizorftab(infile, fmt='lwc'):
    from molbiox.kb import vizorf
    try:
        fieldlist = getattr(vizorf, fmt)
    except AttributeError:
        errmsg = 'invalid vizorf-tab format: fmt={}'.format(repr(fmt))
        raise ValueError(errmsg)

    for rec in read(infile, fieldlist):
        head = rec.head
        tail = rec.tail
        rec.head = min(head, tail)
        rec.tail = max(head, tail)
        yield rec


def tab_format(infile, sep=None, align='<'):
    """
    Format tabular text file into a human readable form
    :param infile: a path, file object or FileWrapper object
    :param sep:
    :param align: '<' or '>'
    :return:
    """
    max_widths = collections.defaultdict(int)
    with streaming.FilePeeker(infile, 'r') as fila:
        # peek for max width for each column
        fila.peek = True
        records = read(fila, sep=sep)
        for tabrec, _ in six.moves.zip(records, six.moves.range(10)):
            for k in tabrec:
                max_widths[k] = max(max_widths[k], len(tabrec[k]))
            # print(tabrec)
            # print(max_widths)

        fila.peek = False
        for tabrec in read(fila, sep=sep):
            cells = []
            for k in tabrec:
                cells.append("{0:{1}{2}}".format(tabrec[k], align, max_widths[k]))
            yield ' '.join(cells)


def persist(url, tblname, records):
    db = dataset.connect(url)
    tbl = db[tblname]
    tbl.insert_many(records)
