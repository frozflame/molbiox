#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals
from collections import Counter
from molbiox.algor import interval


def find_next_contigs(samfile, contig, insertmax, orientation='fr'):
    """
    :param samfile:     pysam.calignmentfile.AlignmentFile object
    :param contig:      contig id (an integer)
    :param insertmax:   maximun allowed insert size
    :param orientation: fr / rf
    :param direction:   prev / next
    :return:
    """

    length = samfile.lengths[contig]

    if direction == 'prev':
        headpos = 0
        tailpos = min(insertmax, length)
    elif direction == 'next':
        headpos = max(0, length-insertmax)
        tailpos = length
    else:
        raise ValueError('direction can only be prev or next')

    reads = samfile.fetch(contig, headpos, tailpos)
    reads = (r for r in reads if r.is_paired and not r.mate_is_unmapped)

    # should read be reversed?
    revdict = dict(prevfr=True, prevrf=False, nextfr=False, nextrf=True)
    needrev = revdict[direction + orientation]
    reads = (r for r in reads if bool(r.is_reverse) == needrev)

    valid_pairs = []

    for read in reads:

        # this line, VERY SLOW!
        mate = samfile.mate(read)

        if read.reference_id == mate.reference_id:
            continue

        mcontig = mate.reference_id
        mlength = samfile.lengths[mcontig]

        if not isinstance(mate.reference_start, int):
            continue
        if not isinstance(mate.reference_end, int):
            continue

        if mate.is_reverse and orientation == 'fr' or \
                not mate.is_reverse and orientation == 'rf':
            mheadpos = 0
            mtailpos = min(insertmax, mlength)
        else:
            mheadpos = max(0, length-insertmax)
            mtailpos = mlength

        # overlap size
        ov = interval.overlap_size(
            mheadpos, mtailpos, mate.reference_start, mate.reference_end)

        if ov > 0:
            valid_pairs.append((read, mate))

    refs = samfile.references

    strand = lambda r, m: 'diff' if r.is_reverse == m.is_reverse else 'same'
    nextcontigs = ((refs[m.reference_id], strand(r, m)) for r, m in valid_pairs)
    return Counter(nextcontigs)