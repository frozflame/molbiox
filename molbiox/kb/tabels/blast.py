#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import sys


def get_fieldmap_reversed():
    return {
        'bitscore':     'bit_score',
        'btop':         'btop',
        'evalue':       'evalue',
        'frames':       'query_sbjct_frames',
        'gapopen':      'gap_opens',
        'gaps':         'gaps',
        'length':       'alignment_length',
        'mismatch':     'mismatches',
        'nident':       'identical',
        'pident':       'percent_identity',
        'positive':     'positives',
        'ppos':         'percent_positives',
        'qacc':         'query_acc',
        'qaccver':      'query_acc_ver',
        'qcovhsp':      'percent_query_coverage_per_hsp',
        'qcovs':        'percent_query_coverage_per_subject',
        'qend':         'q_end',
        'qframe':       'query_frame',
        'qgi':          'query_gi',
        'qlen':         'query_length',
        'qseq':         'query_seq',
        'qseqid':       'query_id',
        'qstart':       'q_start',
        'sacc':         'subject_acc',
        'saccver':      'subject_acc_ver',
        'sallacc':      'subject_accs',
        'sallgi':       'subject_gis',
        'sallseqid':    'subject_ids',
        'salltitles':   'subject_titles',
        'sblastnames':  'subject_blast_names',
        'scomnames':    'subject_com_names',
        'score':        'score',
        'send':         's_end',
        'sframe':       'sbjct_frame',
        'sgi':          'subject_gi',
        'slen':         'subject_length',
        'sscinames':    'subject_sci_names',
        'sseq':         'subject_seq',
        'sseqid':       'subject_id',
        'sskingdoms':   'subject_super_kingdoms',
        'sstart':       's_start',
        'sstrand':      'subject_strand',
        'staxids':      'subject_tax_ids',
        'stitle':       'subject_title'}


def get_fieldmap():
    fieldmap_rev = get_fieldmap_reversed()
    return dict(zip(fieldmap_rev.values(),
                    fieldmap_rev.keys()))


# blast6m / blast7m
def get_fieldlist_mini():
    return [
        ('query_id',            None),
        ('query_length',        int),
        ('subject_length',      int),
        ('subject_id',          None),
        ('alignment_length',    int),
        ('percent_identity',    float),
        ('q_start',             int),
        ('q_end',               int),
        ('s_start',             int),
        ('s_end',               int),
    ]


# blast7 / blast7d
def get_fieldlist_default():
    return [
        ('query_id',         None),
        ('subject_id',       None),
        ('precent_identity', float),
        ('alignment_length', int),
        ('mismatches',       int),
        ('gap_opens',        int),
        ('q_start',          int),
        ('q_end',            int),
        ('s_start',          int),
        ('s_end',            int),
        ('evalue',           float),
        ('bit_score',        float),
    ]


# blast7a
def get_fieldlist_all():
    # silly form just to fold in pycharm
    return [
        ('query_id',        None),
        ('query_gi',        None),
        ('query_acc',       None),
        ('query_acc_ver',   None),
        ('query_length',    int),
        ('subject_id',      None),
        ('subject_ids',     None),
        ('subject_gi',      None),
        ('subject_gis',     None),
        ('subject_acc',     None),
        ('subject_acc_ver', None),
        ('subject_accs',    None),
        ('subject_length',  int),
        ('q_start',         int),
        ('q_end',           int),
        ('s_start',         int),
        ('s_end',           int),
        ('query_seq',       None),
        ('subject_seq',     None),
        ('evalue',          None),
        ('bit_score',       None),
        ('score',           float),
        ('alignment_length',    int),
        ('percent_identity',    float),
        ('identical',       None),
        ('mismatches',      None),
        ('positives',       None),
        ('gap_opens',       None),
        ('gaps',            None),
        ('percent_positives',   None),
        ('query_sbjct_frames',  None),
        ('query_frame',     None),
        ('sbjct_frame',     None),
        ('btop',            None),
        ('subject_tax_ids', None),
        ('subject_sci_names',   None),
        ('subject_com_names',   None),
        ('subject_blast_names', None),
        ('subject_super_kingdoms',  None),
        ('subject_title',   None),
        ('subject_titles',  None),
        ('subject_strand',  None),
        ('percent_query_coverage_per_subject',  None),
        ('percent_query_coverage_per_hsp',      None),
    ]


def make_ncbi_spec(fieldlist):
    fieldmap = get_fieldmap()
    return ' '.join(fieldmap[a] for a, t in fieldlist)


fmtdefault = fmt6 = fmt7 = fmt6d = fmt7d = get_fieldlist_default()
fmtmini = fmt6m = fmt7m = get_fieldlist_mini()
fmtall = fmt6a = fmt7a = get_fieldlist_all()

