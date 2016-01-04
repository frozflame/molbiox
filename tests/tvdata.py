#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import sys
import numpy as np
from oct2py import octave


"""
Trivial data for trials / debugging
"""

istring = 'LMAKSKILKNTLVLYFRQVLIVLITLYSMRVVLNELGVDDFGIYSVVAGFVTLMMLAFLPGSMASAQQRFFTS'
jstring = 'LMAKSKILKNTLVLYFRQVLIVLITLYSMRVVLNELGVDDFGIYSVVAGFVTLLAFLPGSMASATQRFFS'
dna = 'TATTATCACGGCGCGTTGATCTCGACGCGTAAAACACCGTCTAAAGCGATCAGCACTGTA'


arr1 = np.array([
    [0, 0, 0, 0, 0],
    [0, 1, 0, 0, 1],
    [0, 1, 0, 0, 1],
    [0, 1, 0, 0, 1],
    [0, 0, 1, 1, 0],
    [0, 0, 1, 1, 0]])

marr = np.array([
    [8, 1,  6],
    [3, 5,  7],
    [4, 9,  2]])

x = 1
s = dna
bs = dna.encode('ascii')



