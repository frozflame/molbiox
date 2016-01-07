#!/usr/bin/env python3
# encoding: utf-8

from __future__ import unicode_literals
import collections

from molbiox.io import tabular
from molbiox.frame import interactive


# blast6m / blast7m
fieldlist_mini = [
    ('query.id',            None),
    ('query.length',        int),
    ('subject.length',      int),
    ('subject.id',          None),
    ('alignment.length',    int),
    ('percent.identity',    float),
    ('q.start',             int),
    ('q.end',               int),
    ('s.start',             int),
    ('s.end',               int),
]


# blast7 / blast7d
fieldlist_default = [
    ('query.id',         None),
    ('subject.id',       None),
    ('precent.identity', float),
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


# blast7a
fieldlist_all = [
    ('query.id',        None),
    ('query.gi',        None),
    ('query.acc',       None),
    ('query.acc.ver',   None),
    ('query.length',    int),
    ('subject.id',      None),
    ('subject.ids',     None),
    ('subject.gi',      None),
    ('subject.gis',     None),
    ('subject.acc',     None),
    ('subject.acc.ver', None),
    ('subject.accs',    None),
    ('subject.length',  int),
    ('q.start',         int),
    ('q.end',           int),
    ('s.start',         int),
    ('s.end',           int),
    ('query.seq',       None),
    ('subject.seq',     None),
    ('evalue',          None),
    ('bit.score',       None),
    ('score',           float),
    ('alignment.length',    int),
    ('percent.identity',    float),
    ('identical',       None),
    ('mismatches',      None),
    ('positives',       None),
    ('gap.opens',       None),
    ('gaps',            None),
    ('percent.positives',   None),
    ('query.sbjct.frames',  None),
    ('query.frame',     None),
    ('sbjct.frame',     None),
    ('BTOP',            None),
    ('subject.tax.ids', None),
    ('subject.sci.names',   None),
    ('subject.com.names',   None),
    ('subject.blast.names', None),
    ('subject.super.kingdoms',  None),
    ('subject.title',   None),
    ('subject.titles',  None),
    ('subject.strand',  None),
    ('percent.query.coverage.per.subject',  None),
    ('percent.query.coverage.per.hsp',      None),
]


@interactive.castable
def read_fmt6m(infile):
    return tabular.read(infile, fieldlist_mini)


@interactive.castable
def read_fmt6(infile):
    return tabular.read(infile, fieldlist_default, sep='\t')


@interactive.castable
def read_fmt6a(infile):
    return tabular.read(infile, fieldlist_all, sep='\t')


@interactive.castable
def read_fmt7(infile):
    return tabular.read(infile, fieldlist_default, sep='\t')


@interactive.castable
def read_fmt7a(infile):
    return tabular.read(infile, fieldlist_all, sep='\t')


def aggregate(records, subsep=None):
    """
    :param records: an iterable of blast records
    :param subsep: seperator use on subject name;
                after splitting, the first part is used
    :return: a defaultdict object, query_id's as keys
    """
    querydic = collections.defaultdict(set)
    for rec in records:
        key = rec.get('query.id')
        if subsep:
            val = rec.get('subject.id').split(subsep)[0]
        else:
            val = rec.get('subject.id')
        querydic[key].add(val)
    return querydic
