#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function

import sys

if __name__ == '__main__':
    pass

blast_fieldmap_rev = {
    'bitscore':     'bit.score',
    'btop':         'BTOP',
    'evalue':       'evalue',
    'frames':       'query.sbjct.frames',
    'gapopen':      'gap.opens',
    'gaps':         'gaps',
    'length':       'alignment.length',
    'mismatch':     'mismatches',
    'nident':       'identical',
    'pident':       'percent.identity',
    'positive':     'positives',
    'ppos':         'percent.positives',
    'qacc':         'query.acc',
    'qaccver':      'query.acc.ver',
    'qcovhsp':      'percent.query.coverage.per.hsp',
    'qcovs':        'percent.query.coverage.per.subject',
    'qend':         'q.end',
    'qframe':       'query.frame',
    'qgi':          'query.gi',
    'qlen':         'query.length',
    'qseq':         'query.seq',
    'qseqid':       'query.id',
    'qstart':       'q.start',
    'sacc':         'subject.acc',
    'saccver':      'subject.acc.ver',
    'sallacc':      'subject.accs',
    'sallgi':       'subject.gis',
    'sallseqid':    'subject.ids',
    'salltitles':   'subject.titles',
    'sblastnames':  'subject.blast.names',
    'scomnames':    'subject.com.names',
    'score':        'score',
    'send':         's.end',
    'sframe':       'sbjct.frame',
    'sgi':          'subject.gi',
    'slen':         'subject.length',
    'sscinames':    'subject.sci.names',
    'sseq':         'subject.seq',
    'sseqid':       'subject.id',
    'sskingdoms':   'subject.super.kingdoms',
    'sstart':       's.start',
    'sstrand':      'subject.strand',
    'staxids':      'subject.tax.ids',
    'stitle':       'subject.title'}

blast_fieldmap = dict(zip(blast_fieldmap_rev.values(),
                          blast_fieldmap_rev.keys()))
