#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import os
import sys
import ctypes
import numpy as np
from numpy.ctypeslib import ndpointer
from molbiox.frame.locate import locate_lib


class Aligner(object):

    cindel = '-'
    index_type = ctypes.c_int64
    score_type = ctypes.c_int64
    short_type = ctypes.c_int16

    score_dtype = 'int64'
    index_dtype = 'int64'

    def __init__(self, rho, sigma, scorebook):
        """
        :param rho: gap opening penalty
        :param sigma: gap extension penalty
        :param scorebook: see `from_submatrix` method
        """
        self.rho = rho
        self.sigma = sigma
        self.scorebook = scorebook

        arrflages = str('C')

        self.lib = ctypes.cdll.LoadLibrary(locate_lib('align.so'))
        self.build = self.lib.build
        self.build.argtypes = [
            ndpointer(self.score_type, flags=arrflages),
            self.index_type,   # isize
            self.index_type,   # jsize
            self.score_type,   # rho
            self.score_type,   # sigma
            self.short_type,  # local_
        ]

        self.backtrack = self.lib.backtrack
        self.backtrack.rettype = self.index_type
        self.backtrack.argtypes = [
            ndpointer(self.score_type, flags=arrflages),
            self.index_type,   # isize
            self.index_type,   # jsize
            self.index_type,   # istart
            self.index_type,   # jstart
            ndpointer(self.index_type, flags=arrflages),    # iarr index
            ndpointer(self.index_type, flags=arrflages),    # jarr index
            self.short_type,  # global_
        ]

    def calculate(self, istring, jstring, scheme=1, backtrack=False):
        """
        :param istring: a string
        :param jstring: a string
        :param scheme: 1 for global, 2 for overlap, 3 for local
        :param backtrack:   do backtrack? True or False
        :return:    (matrix, istring_arr, jstring_arr)
        """
        isize = len(istring) + 1
        jsize = len(jstring) + 1

        # convert strings to 1d arrays
        iarr = np.empty(isize, dtype='uint8')
        jarr = np.empty(jsize, dtype='uint8')

        iarr[1:] = np.fromstring(istring, dtype='uint8')
        jarr[1:] = np.fromstring(jstring, dtype='uint8')

        iarr[0] = ord(self.cindel)
        jarr[0] = ord(self.cindel)

        ixarr = self.build_ixarr(iarr, jarr)
        matrx = np.empty(shape=[isize, jsize, 4], dtype=self.score_dtype)

        # mark scores on matrx
        matrx[:, :, 2] = self.scorebook[ixarr]

        # overlap and local
        if scheme in (2, 3):
            matrx[:, 0, :3] = 0  # j = 0, of isize x 3
            matrx[0, :, :3] = 0  # i = 0, of jsize x 3
        else:
            # TODO: when sigma == 0
            border = np.arange(max(isize, jsize), dtype='int') * -1 * self.sigma
            border.shape = -1, 1
            matrx[:, 0, :3] = border[:isize]
            matrx[0, :, :3] = border[:jsize]

        matrx[:, 0, 3] = 0
        matrx[0, :, 3] = 1
        matrx[0, 0, 3] = 3

        # dynamic programming -- main step
        self.build(matrx, isize, jsize, self.rho, self.sigma, scheme)

        if not backtrack:
            return matrx, None, None

        ipos_arr = np.empty(max(isize, jsize), dtype=self.index_dtype)
        jpos_arr = np.empty(max(isize, jsize), dtype=self.index_dtype)

        # print('start backtrack')
        # TODO: local/ overlap backtrack not from last point
        # backtrack -- another major step
        l = self.backtrack(
            matrx, isize, jsize, isize-1, jsize-1, ipos_arr, jpos_arr, scheme)

        # # debug
        # print('sizes:', l, iarr.shape, jarr.shape)
        return matrx, iarr[ipos_arr[:l]], jarr[jpos_arr[:l]]

    @classmethod
    def build_ixarr(cls, iarr, jarr):
        """
        Build an array of indexes. Each value represent a pair of letters.
        :param iarr: a 1d array representing a string
        :param jarr: a 1d array representing a string
        :return: a 2d array
        """

        iarr = iarr.astype('uint16') << 8
        jarr = jarr.astype('uint16')
        iarr[0] = 0
        jarr[0] = 0
        iarr.shape = -1, 1
        jarr.shape = 1, -1

        return iarr | jarr

    @classmethod
    def from_submatrix(cls, istring, jstring, submatr, rho=12, sigma=1):
        scorebook = np.zeros(2 ** 16, dtype=submatr.dtype)
        iarr = np.fromstring(istring, 'uint8')
        jarr = np.fromstring(jstring, 'uint8')
        ixarr = cls.build_ixarr(iarr, jarr)
        scorebook[ixarr] = submatr
        return cls(rho, sigma, scorebook)

    def align(self, istring, jstring, scheme=1, backtrack=False):
        matrx, iarr, jarr = self.calculate(istring, jstring, scheme, backtrack)
        if backtrack:
            return matrx[-1, -1, 2], iarr.tostring()[::-1], jarr.tostring()[::-1]
        else:
            return matrx[-1, -1, 2], iarr.tostring()[::-1], jarr.tostring()[::-1]


def debug_trace(matrx):
    symbols = ord('-'), ord('|'), ord('\\'), ord('3')
    symbols = np.array(symbols, dtype='uint8')
    idx = matrx[:, :, 3]
    darr = symbols[idx]
    for row in darr:
        line = row.tostring().decode('ascii')
        print(line, file=sys.stderr)


def gen_match_string(istring, jstring, indelchar='-'):
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
    return marr.tostring()
