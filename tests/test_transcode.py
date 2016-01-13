
from __future__ import print_function
# import os
# import unittest

from molbiox.algor.transcode import CharsMapper
from molbiox.frame.signature import Sig


test_data_dna = {
    '+': 'TTGATGGCTAAGAGTAAAATCTTAAAAAACACACTGGTTCTATATTTTCGTCAAGTTTTG',
    '-': 'CAAAACTTGACGAAAATATAGAACCAGTGTGTTTTTTAAGATTTTACTCTTAGCCATCAA',
} + Sig('md5:d07980025382378c0bc3b98f60ea63b1', cheat=0)

# easy access in interactive shell
t = test_data_dna


def test_revcompl_dna():
    # validate test data
    test_data_dna.inspect()

    mapper = CharsMapper.create_mapper_compl_dna()
    revcompl = mapper.transcode(test_data_dna['+']).decode('ascii')[::-1]
    assert revcompl == test_data_dna['-']

