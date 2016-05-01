#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import numpy as np

from molbiox.frame import streaming
from molbiox.frame.regexon import remove_whitespaces
from molbiox.frame.environ import locate_submat


def read(infile):
    try:
        fila = streaming.FileAdapter(infile, 'r')
    except IOError:
        respath = locate_submat(infile.lower())
        fila = streaming.FileAdapter(respath, 'r')

    with fila:
        fw_lines = (l.strip() for l in fila.file)
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

        for line in fila.file:
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
