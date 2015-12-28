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
        self.refarr = np.empty(64, dtype='uint8')

        # refarr[packed_value] = amino_acid
        self.refarr[packarr] = [ord(dic[c]) for c in condons]

    @classmethod
    def _gen_packarr(cls, string):
        """
        A   01000001
        C   01000011
        G   01000111    ->  0000 0010
        T   01010100
        :param string: assuming containing only ATCG and len(string) % 3 == 0
        :return:
        """
        arr = np.fromstring(string, dtype='uint8')
        arr[arr == ord('G')] = 2
        arr.shape = -1, 3

        # mask out unwanted bits
        arr &= 3
        arr <<= [0, 2, 4]

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

