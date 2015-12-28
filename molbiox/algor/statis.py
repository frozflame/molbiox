#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function

import collections
from molbiox.kb.transcode import ambig_nucl_gc_equiv


def calc_gc_content(seq, percent=False):
    counter = collections.Counter(seq.upper())
    count = counter['G'] + counter['C'] + 0.

    for x in counter:
        if x in ambig_nucl_gc_equiv:
            count += ambig_nucl_gc_equiv[x] * counter[x]

    ratio = count / len(seq)

    if percent:
        return int(ratio * 100)
    else:
        return ratio


def calc_n50_statistic(lenths):
    lenths = list(lenths)
    half = sum(lenths) / 2.
    for x in sorted(lenths, reverse=True):
        half -= x
        if half <= 0:
            return x


def guess_seqtype(seq):
    counter = collections.Counter(seq.lower())
    if sum(counter[k] for k in 'atgcn') >= len(seq) * .6:
        return 'nucl'
    else:
        return 'prot'
