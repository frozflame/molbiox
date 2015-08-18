#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function

import collections

from molbiox.info.codes import ambig_nucl_gc_equiv


def gc_content(sequence, percent=False):
    counter = collections.Counter(sequence.upper())
    count = counter['G'] + counter['C'] + 0.

    for x in counter:
        if x in ambig_nucl_gc_equiv:
            count += ambig_nucl_gc_equiv[x] * counter[x]

    ratio = count / len(sequence)

    if percent:
        return int(ratio * 100)
    else:
        return ratio


def n50_stats(lenths):
    lenths = list(lenths)
    half = sum(lenths) / 2.
    for x in sorted(lenths, reverse=True):
        half -= x
        if half <= 0:
            return x


def guess_type(seq):
    counter = collections.Counter(seq.lower())
    if sum(counter[k] for k in 'atgcn') >= len(seq) * .6:
        return 'nucl'
    else:
        return 'prot'
