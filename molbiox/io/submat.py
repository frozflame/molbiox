#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import numpy as np
from molbiox.frame import interactive
from molbiox.frame.regexon import remove_whitespaces
from molbiox.frame.locate import locate_submat


def read(infile):
    try:
        fw = interactive.FileWrapper(infile, 'r')
    except IOError:
        respath = locate_submat(infile.lower())
        fw = interactive.FileWrapper(respath, 'r')

    istring_ = []
    jstring = None
    scores = []

    for line in fw.file:
        line = line.strip()
        if line and not line.startswith('#'):
            jstring = remove_whitespaces(line)
            jsize = len(jstring) + 1
            break

    if jstring is None:
        raise ValueError('this sub matrix file is broken')

    for line in fw.file:
        items = line.split()
        if not items:
            continue
        # print('debug: jstring', jstring)
        # print('debug: jstring', len(jstring))
        # print('debug: items', items)
        # print('debug: items', len(items))
        # print('debug: jsize', jsize)

        if len(items) != jsize:
            raise ValueError('this sub matrix file is broken')
        istring_.append(items[0])
        scores.append([int(s) for s in items[1:]])

    fw.close()

    istring = ''.join(istring_)
    submatr = np.array(scores, dtype=int)
    return istring, jstring, submatr


