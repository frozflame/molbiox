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
