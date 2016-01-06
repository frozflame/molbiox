#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import sys
from molbiox.frame.signature import Sig

CHEAT = False

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
} + Sig('md5:916efdf0caefc4e0915fe89bc494d3e4')


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
} + Sig('md5:1e124db4b8893fb1f240308436fa454c')

ambig_prot = {}

# config for complementary DNA
complDNA = {
    'src':  'MNHKDGABCXYTUWRS-.mnhkdgabcxytuwrs',
    'dest': 'KNDMHCTVGXRAAWYS-.kndmhctvgxraawys', 'outlier':  '-',
} + Sig('md5:72b8d46e58ae7cfd1268a50d66adcda5', cheat=CHEAT)


# config for complementary RNA
complRNA = {
    'src':  'MNHKDGABCXYTUWRS-.mnhkdgabcxytuwrs',
    'dest': 'KNDMHCUVGXRAAWYS-.kndmhcuvgxraawys', 'outlier':  '-',
} + Sig('md5:ebbe993330ececd7736b1d4f5e211e51', cheat=CHEAT)

test_data_dna = {
    '+': 'TTGATGGCTAAGAGTAAAATCTTAAAAAACACACTGGTTCTATATTTTCGTCAAGTTTTG',
    '-': 'CAAAACTTGACGAAAATATAGAACCAGTGTGTTTTTTAAGATTTTACTCTTAGCCATCAA',
} + Sig('md5:80df1e8c8c5eba1c54fdb5857e089fef', cheat=CHEAT)

test = complRNA
