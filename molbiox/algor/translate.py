#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import numpy as np


class CodonTable(object):
    def __init__(self, dic):
        """
        :param dic: a dict which maps condons to AAs
        """
        condons = [c.upper() for c in dic]
        condons.sort()
        packarr = self._gen_packarr(''.join(condons))

        # max(packarr) < 64 (2**6)
        self.refarr = np.empty(128, dtype='uint8')

        # refarr[packed_value] = amino_acid
        self.refarr[packarr] = [ord(dic[c]) for c in condons]
        self.refarr[64:] = ord('X')

    @classmethod
    def _gen_packarr(cls, string):
        """
        A   0100 0001
        C   0100 0011
        G   0100 0111
        T   0101 0100
        :param string: containing only upper-case letters and len(string) % 3 == 0
        :return:
        """
        arr = np.fromstring(string, dtype='uint8')
        arr[arr == ord('T')] = 0
        arr[arr == ord('A')] = 1
        arr[arr == ord('G')] = 2
        arr[arr == ord('C')] = 3

        arr[arr > 3] = int('01010101', base=2)

        arr.shape = -1, 3

        # mask out unwanted bits
        arr <<= np.array([0, 2, 4], dtype='uint8')

        # 50x faster than arr.sum(axis=1)
        packarr = arr[:, 0] | arr[:, 1] | arr[:, 2]
        return packarr

    def translate(self, seq):
        """
        Translate DNA seq to protein seq
        :param seq: a string whose length is a multiple of 3
        :return: a string (bytes)
        """
        packarr = self._gen_packarr(seq)
        arr = self.refarr[packarr]
        return arr.tostring()

