#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import numpy as np
from molbiox.frame import compat
from molbiox.frame.regexon import remove_whitespaces
from molbiox.frame.locate import locate_submat


def read(infile):
    try:
        fw = compat.FileWrapper(infile, 'r')
    except IOError:
        respath = locate_submat(infile.lower())
        fw = compat.FileWrapper(respath, 'r')

    with fw:
        fw_lines = (l.strip() for l in fw.file)
        ichars = []
        jstring = None
        jsize = 0
        scores = []

        for line in fw_lines:
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

            if len(items) != jsize:
                raise ValueError('this sub matrix file is broken')
            ichars.append(items[0])
            scores.append([int(s) for s in items[1:]])

    istring = ''.join(ichars)
    submatr = np.array(scores, dtype=int)
    return istring, jstring, submatr
