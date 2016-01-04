#!/usr/bin/env python3
# coding: utf-8
from __future__ import unicode_literals, print_function

import sys
import six
from molbiox.algor import aligner
from molbiox.frame import iteration
from molbiox.frame.locate import locate_tests
from molbiox.frame.testing import Timer
from molbiox.io import submat, fasta

score_type = 'int64'
repeat = 1000


def test_align():
    istring, jstring, submatr = submat.read('pam200')
    ali = aligner.Aligner.from_submatrix(istring, jstring, submatr)

    path = locate_tests('data/rmlA.2x.fa')
    iseq, jseq = fasta.read(path, castfunc=lambda x: [s.seq for s in x])

    with Timer('align'):
        for i in range(repeat):
            matrx, istring, jstring = ali.align(iseq, jseq, backtrack=True)

    mstring = aligner.gen_match_string(istring, jstring)

    for items in iteration.chunkwise(60, istring, mstring, jstring):
        bunch = six.b('\n').join(items).decode('ascii')
        print(bunch, end='\n\n', file=sys.stderr)

if __name__ == '__main__':
    test_align()



