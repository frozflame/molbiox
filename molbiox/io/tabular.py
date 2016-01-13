#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import itertools
import csv
from collections import OrderedDict, defaultdict
from molbiox.frame import streaming, containers, interactive


@interactive.castable
def read(infile, fieldlist=None, sep=None):
    """
    Read a tabular text file
    :param infile: a file object or a file path
    :param fieldlist: [(fieldname, fieldtype), ...] see `io/blast` for examples
    :param sep: separator use in `string.split(sep)`
    :return: a generator, yielding OrderedDict objects
    """

    # if fieldlist is NOT given, generate list-like dicts
    if not fieldlist:
        fieldlist = ((i, None) for i in itertools.count())

    with streaming.FileWrapper(infile, 'r') as fw:
        for line in fw.file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            values = line.split(sep, len(fieldlist)-1)

            if len(values) < len(fieldlist):
                raise ValueError('too few columns in data file')

            pairs = []
            for (key, cast), val in zip(fieldlist, values):
                if cast is not None:
                    val = cast(val)
                pairs.append((key, val))
            yield OrderedDict(pairs)


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
    :return: an OrderedDict
    """

    with streaming.FileWrapper(infile, 'r') as fw:
        resdict = OrderedDict()
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


class Aggregator(object):
    def __init__(self, records, idx_key=0, idx_val=0):
        self.records = records
        self.idx_key = idx_key
        self.idx_val = idx_val

    @staticmethod
    def _lookup(record, index=None, default=None):
        """
        One-based lookup
        :param record: an object having a __getitem__ interface
        :param index: an integer, 0-based index
        :param default:
        :return:
        """
        if index is None:
            return default
        try:
            return record[index]
        except LookupError:
            return default

    @property
    def kv_pairs(self):
        for rec in self.records:
            key = self._lookup(rec, self.idx_key)
            val = self._lookup(rec, self.idx_val)
            yield key, val

    def _ag_sum(self):
        groups = containers.DefaultOrderedDict(lambda: defaultdict(float))
        for key, val in self.kv_pairs:
            groups[key]['sum'] += float(val)
            groups[key]['count'] += 1
        return groups

    def ag_sum(self):
        groups = self._ag_sum()
        for key in groups:
            groups[key] = groups[key]['sum']
        return groups

    def ag_ave(self):
        """
        :return:
        """
        groups = self._ag_sum()
        for key in groups:
            groups[key] = groups[key]['sum'] / groups[key]['count']
        return groups

    def ag_list(self):
        groups = containers.DefaultOrderedDict(list)
        for key, val in self.kv_pairs:
            groups[key].append(val)
        return groups

    def ag_set(self):
        groups = containers.DefaultOrderedDict(set)
        for key, val in self.kv_pairs:
            groups[key].add(val)
        return groups

    def ag_count(self):
        init_agval = containers.DefaultOrderedDict(float)
        groups = containers.DefaultOrderedDict(lambda: init_agval)
        for key, val in self.kv_pairs:
            groups[key][val] += 1
        return groups

    def ag_pass(self):
        return containers.DefaultOrderedDict(None, self.kv_pairs)

    def ag_line(self):
        groups = containers.DefaultOrderedDict()
        for rec in self.records:
            key = self._lookup(rec, self.idx_key)
            val = '\t'.join
            yield key, val


class LineGrouper(object):
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


