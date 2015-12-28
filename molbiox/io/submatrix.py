#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
from molbiox.frame import interactive
from molbiox.frame.regexon import Regexon


def read(infile):

    fw = interactive.FileWrapper(infile, 'r')
    sub = Regexon.alpha()

    istring_ = []
    jstring = None
    scores = []

    for line in fw.file:
        line = line.strip()
        if line and not line.startswith('#'):
            jstring = sub(line)
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
        istring_.append(items[0])
        scores.append([int(s) for s in items[1:]])

    fw.close()

    istring = ''.join(istring_)
    return istring, jstring, scores


