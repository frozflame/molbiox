#!/usr/bin/env python3

from __future__ import unicode_literals, print_function
import re
import string
import six
from molbiox.io import fasta
from molbiox.frame.locate import locate_tests


def test_buffer():
    s = string.digits
    assert fasta.Buffer(0).put(s) == s
    assert fasta.Buffer(0).put('') == ''
    assert fasta.Buffer(1).put('') == ''
    assert fasta.Buffer(1).put(s) == s[1:]

    # normal use case
    for i in six.moves.range(len(s) + 2):
        buffer = fasta.Buffer(i)
        remainder = buffer.put(s)
        assert len(remainder) == max(0, len(s)-i)

        buffer.get()
        assert buffer.get() == ''

        remainder = buffer.put(s)
        assert buffer.get() + remainder == s


def test_cmtstate():
    pass


def _test_fasta_read(path):
    recs = fasta.read(path, limit=50, castfunc=list)
    print(len(recs))
    assert len(recs) == 4 * 3
    for rec in recs:
        assert re.match(r'^(anonym|randseq)\.\d$', six.u(rec.cmt))
        assert len(rec.seq) in (50, 20)


def test_fasta_read():
    # anonym
    path = locate_tests('data/test_fasta/test.anonym.fa')
    assert path.startswith('/')
    _test_fasta_read(path)

    # empty lines
    path = locate_tests('data/test_fasta/test.empty-lines.fa')
    _test_fasta_read(path)

    # normal lines
    path = locate_tests('data/test_fasta/test.normal.fa')
    _test_fasta_read(path)
