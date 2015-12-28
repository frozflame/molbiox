#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import sys
from molbiox.algor.arrows import ArrowCalculator
from molbiox.io.arrows import read_lwcfile


def test_read_lwcfile():
    path = 'data/sample_lwcfile.txt'
    table = read_lwcfile(path, castfunc=list)
    for x in table:
        print(x)

def test_arrow_factory():
    path = 'data/sample_lwcfile.txt'
    tab = read_lwcfile(path, castfunc=list)
    arr = [[r['head'], r['tail']] for r in tab]

    print(arr)

    arrfactory = ArrowCalculator()
    data = arrfactory.make(arr)
    print(data)



if __name__ == '__main__':
    # test_read_lwcfile()
    test_arrow_factory()
