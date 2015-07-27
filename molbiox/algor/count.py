#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import collections

from molbiox.knowledge.codes import ambig_nucl_gc_equiv


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





