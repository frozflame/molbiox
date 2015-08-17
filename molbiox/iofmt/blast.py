#!/usr/bin/env python3
# encoding: utf-8

from collections import OrderedDict
from molbiox import tolerant
from molbiox.iofmt import tabular

__author__ = 'Hailong'


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


blast7m = """
    qseqid sseqid pident length qstart qend sstart ssend
    """.split()

blast7d = """
    qseqid sseqid pident length mismatch gapopen
    qstart qend sstart ssend evalue bitscore
    """.split()

blast7a = """
    qseqid qgi qacc qaccver qlen sseqid sallseqid sgi sallgi
    sacc saccver sallacc slen qstart qend sstart send qseq
    sseq evalue bitscore score length pident nident mismatch
    positive gapopen gaps ppos frames qframe sframe btop
    staxids sscinames scomnames sblastnames sskingdoms
    stitle salltitles sstrand qcovs qcovhsp""".split()


@tolerant.castable
def read_fmt6m(handle):
    return tabular.read(handle, fieldlist_mini)


@tolerant.castable
def read_fmt6(handle):
    return tabular.read(handle, fieldlist_default, sep='\t')


@tolerant.castable
def read_fmt6a(handle):
    return tabular.read(handle, fieldlist_all, sep='\t')


@tolerant.castable
def read_fmt7(handle):
    return tabular.read(handle, fieldlist_default, sep='\t')


@tolerant.castable
def read_fmt7a(handle):
    return tabular.read(handle, fieldlist_all, sep='\t')
