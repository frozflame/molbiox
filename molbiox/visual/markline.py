#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals
import math

__author__ = 'Hailong'


class Markline(object):
    """
    Represent positions of features on a sequence with text string
    """
    def __init__(self, length, icount, symbol='-'):
        """
        :param length: total length of the line
        :param icount: number of intervals
        :param symbol: character for empty line
        """
        self.length = length
        self.icount = icount
        self.iwidth = 1. * length / icount
        self.iarray = bytearray(symbol*self.icount, 'ascii')

    def mark(self, position, symbol='*'):
        """
        Mark a position
        """
        if position > self.length:
            raise ValueError('position out of bound')

        # index of interval
        ix = math.floor(1.*position/self.iwidth)
        if ix >= self.icount:
            ix = self.icount
        self.iarray[ix] = ord(symbol)

    @property
    def string(self):
        return self.iarray.decode('ascii')

    def __str__(self):
        return self.string

    def __repr__(self):
        return 'Markline: {}'.format(self.string)
