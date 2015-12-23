#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function

import sys

ambig_nucl = {
    'M': 'AC',
    'R': 'AG',
    'W': 'AT',
    'S': 'CG',
    'Y': 'CT',
    'K': 'GT',
    'V': 'ACG',
    'H': 'ACT',
    'D': 'AGT',
    'B': 'CGT',
    'X': 'GATC',
    'N': 'GATC',
}


ambig_nucl_gc_equiv = {
    'B': 0.6666666666666666,
    'D': 0.3333333333333333,
    'H': 0.3333333333333333,
    'K': 0.5,
    'M': 0.5,
    'N': 0.5,
    'R': 0.5,
    'S': 1.0,
    'V': 0.6666666666666666,
    'W': 0.0,
    'X': 0.5,
    'Y': 0.5,
}

ambig_prot = {}

# config for complementary DNA
complDNA = {
    'src':      'MNHKDGABCXYTUWRS-.mnhkdgabcxytuwrs',
    'dest':     'KNDMHCTVGXRAAWYS-.kndmhctvgxraawys',
    'outlier':  '-',
    '_checksum': 'md5:d27052fe982c16e72be9a25b7134b6d0',
}

# config for complementary RNA
complRNA = {
    'src':      'MNHKDGABCXYTUWRS-.mnhkdgabcxytuwrs',
    'dest':     'KNDMHCUVGXRAAWYS-.kndmhcuvgxraawys',
    'outlier':  '-',
    '_checksum': 'md5:8bade416147076110798613102008da6',
}

test_data_dna = {
    '+': 'TTGATGGCTAAGAGTAAAATCTTAAAAAACACACTGGTTCTATATTTTCGTCAAGTTTTG',
    '-': 'CAAAACTTGACGAAAATATAGAACCAGTGTGTTTTTTAAGATTTTACTCTTAGCCATCAA',

}

test = complDNA
