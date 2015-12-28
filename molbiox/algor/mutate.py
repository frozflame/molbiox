#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import math
import numpy as np
import scipy


class MutSimulator(object):
    @classmethod
    def gen_randarr(cls, length):
        """
        Generate a random uint8 array
        :param length: size of the resulting array
        :return: numpy.ndarray of dtype=uint8
        """
        num_dw = math.ceil(length / 4.)
        arr = np.random.randint(0, 2**32, int(num_dw))
        arr = arr.astype(np.uint32)     # get a new array
        arr.dtype = np.uint8
        return arr[:length]

    @classmethod
    def gen_randseq(cls, length):
        """
        Generate a random DNA sequence
        :param length: size of the resulting sequence
        :return: a binary string (bytes)
        """
        arr = cls.gen_randarr(length)
        arr &= 3            # set all bits to 0 except lowest 2
        arr |= ord('@')     # @ A B C   (TAGC)
        arr[arr == ord('@')] = ord('G')
        arr[arr == ord('B')] = ord('T')
        return arr.tostring()

    def __init__(self, seq):
        self.arr = np.fromstring(seq, dtype=np.uint8)

    def mutate(self, pmatrix, t=1):
        """
        Mutate
        :param pmatrix: transition matrix in Markov model
        :param t: time
        :return: None
        """
        matrx = scipy.linalg.fractional_matrix_power(pmatrix, t)
        raise NotImplementedError
