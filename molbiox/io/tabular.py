#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function

import collections
import itertools

import six

from molbiox.frame import containers, streaming, interactive
# from molbiox.visual.arrow import get_defaults


@interactive.castable
def read(infile, fieldlist=None, sep=None, comment=None):
    """
    Read a tabular text file
    :param infile: a file object or a file path
    :param fieldlist: [(fieldname, fieldtype), ...] see `io/blast` for examples
    :param sep: separator use in `string.split(sep)`
    :return: a generator, yielding TabRecord objects
    """
    class DefaultFieldlist(object):
        def __iter__(self):
            return ((i, None) for i in itertools.count())

    # if fieldlist is NOT given, generate list-like dicts
    if fieldlist is None:
        fieldlist = DefaultFieldlist()
        numfields = 0
        # attributes = set()
    else:
        numfields = len(fieldlist)
        # attributes = {x for x, _ in fieldlist}

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
            for (key, cast), val in zip(fieldlist, values):
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
    from molbiox.kb.tabels import blast
    if not fmt.startswith('fmt'):
        fmt = 'fmt' + fmt
    try:
        fieldlist = getattr(blast, fmt)
    except AttributeError:
        errmsg = 'invalid blast tabular format: fmt={}'.format(repr(fmt))
        raise ValueError(errmsg)
    return read(infile, fieldlist)


@interactive.castable
def read_tab_vizorf(infile, fmt='lwc'):
    from molbiox.kb import vizorf
    try:
        fieldlist = getattr(vizorf, fmt)
    except AttributeError:
        errmsg = 'invalid awtab format: fmt={}'.format(repr(fmt))
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
    # def _get_align_symbol(item):
    #     try:
    #         float(item)
    #         return ">"
    #     except:
    #         return "<"
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
