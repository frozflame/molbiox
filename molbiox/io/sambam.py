#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function

from molbiox.frame.common import Dict


def filter_linker_reads(reads, ):
    for read in reads:
        if not isinstance(read.reference_start, int):
                continue
        if not isinstance(read.reference_end, int):
            continue


def build_readrecord(samfile, rfilter=None):
    if rfilter:
        reads = rfilter(samfile)
    else:
        reads = samfile
    for read in reads:
        record = Dict()
        record['alen'] = read.reference_length
        record['qlen'] = read.query_length
        record['rlen'] = samfile.lengths[read.reference_id]

        record['qhead'] = read.query_alignment_start
        record['qtail'] = read.query_alignment_end

        record['rhead'] = read.reference_start
        record['rtail'] = read.reference_end

        record['cigar'] = read.cigarstring

        yield record

