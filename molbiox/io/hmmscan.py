#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function

from molbiox import tolerant
from molbiox.io import tabfile


TBLOUT_FIELDS = [
    ('target.name',         None),
    ('target.accession',    None),
    ('query.name',          None),
    ('query.accession',     None),
    ('fullseq.evalue',      float),
    ('fullseq.score',       float),
    ('fullseq.bias',        float),
    ('bestdom.evalue',      float),
    ('bestdom.score',       float),
    ('bestdom.bias',        float),
    ('dom.num.exp',         float),
    ('dom.num.reg',         int),
    ('dom.num.clu',         int),
    ('dom.num.ov',          int),
    ('dom.num.env',         int),
    ('dom.num.dom',         int),
    ('dom.num.rep',         int),
    ('dom.num.inc',         int),
    ('target.description',  None),
]

@tolerant.castable
def read_tblout(handle):
    """
    Read tabfile generated by `hmmscan --tblout`
    """
    return tabfile.read(handle, TBLOUT_FIELDS)


if __name__ == '__main__':
    import sys
    res = read_tblout(sys.argv[1])
    print(res)


