#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function

from molbiox.compatible import zrange

L = 60


class SRecord(object):
    def __init__(self, key, seq):
        self.key = key
        self.seq = seq

    def __repr__(self):
        return '<SRecord {}.. {}>'.format(self.seq[:6], self.key)

    def __str__(self):
        length = len(self.seq)
        slices = (self.seq[i:i+L] for i in zrange(0, length, L))
        return '>{}\n{}'.format(self.key, '\n'.join(slices))
