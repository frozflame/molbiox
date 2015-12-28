#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import numpy as np


def show_path(matrx):
    symbols = ord('-'), ord('|'), ord('\\'), ord('3')
    symbols = np.array(symbols, dtype='uint8')
    idx = matrx[:, :, 3]
    darr = symbols[idx]

    for row in d:
        # print(row.shape)
        line = row.tostring().decode('ascii')
        print(line)
        # print(len(line))


def match(istring, jstring, indelchar='-'):
    if len(istring) != len(jstring):
        raise ValueError('2 strings must be of same lengths')
    iarr = np.fromstring(istring, dtype='uint8')
    jarr = np.fromstring(jstring, dtype='uint8')

    # set all remaining positions to '?'
    marr = np.empty(len(istring), dtype='uint8')
    marr[:] = ord('.')

    # if same char, use that char
    mask = iarr ^ jarr
    marr[mask == 0] = iarr[mask == 0]

    # if indel, use indel char
    marr[iarr == ord(indelchar)] = ord(indelchar)
    marr[jarr == ord(indelchar)] = ord(indelchar)

    return marr.tostring().decode('ascii')


