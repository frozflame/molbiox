#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals
import itertools

from molbiox.compatible import (zrange, maketrans)

__author__ = 'Hailong'


complDNAmap = dict(zip('mnhkdgabcxytuwrs-.',
                       'kndmhctvgxraawys-.'))

complRNAmap = dict(zip('mnhkdgabcxytuwrs-.',
                       'kndmhcuvgxraawys-.'))


def case_duplicate(dic):
    for (key, val) in list(dic.items()):
        dic[key.upper()] = val.upper()
    return dic


case_duplicate(complDNAmap)
case_duplicate(complRNAmap)

complDNAtab = maketrans(complDNAmap)
complRNAtab = maketrans(complRNAmap)


# input DNA or RNA, output DNA
def compl_dna(s):
    """
    Get complement of a sequence in DNA alphabets.
    """
    return s.translate(complDNAtab)


# input DNA or RNA, output DNA
def compl_rna(s):
    """
    Get complement of a sequence in RNA alphabets.
    """
    return s.translate(complRNAtab)


def rcompl_dna(s):
    """
    Get reverse complement of a sequence in DNA alphabets.
    """
    return s.translate(complDNAtab)[::-1]


def rcompl_rna(s):
    """
    Get reverse complement of a sequence in RNA alphabets.
    """
    return s.translate(complRNAtab)[::-1]


# ~~~ TRANSLATE ~~~

codons = itertools.product('tcag', 'tcag', 'tcag')
aacids = 'FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG'
condon_map = dict(zip(codons, aacids))


def translate(s):
    """
    Translate DNA sequence to peptide

    :param s: a DNA sequence
    """
    s = s.lower()
    aalist = []

    for i in zrange(0, len(s), 3):
        codon = s[i: i+3]
        aa = condon_map.get(codon, '*')
        if aa != '*':
            aalist.append(aa)
        else:
            break
    return ''.join(aalist)


# ~~~ TRANSCRIPT ~~~

for_transcript_map = str.maketrans({'t': 'u', 'T': 'U'})
rev_transcript_map = str.maketrans({'u': 't', 'U': 'T'})


def transcript(s):
    """Transcript DNA to RNA sequence"""
    return s.translate(for_transcript_map)


def rev_transcript(s):
    """Transcript RNA to DNA sequence"""
    return s.translate(rev_transcript_map)

