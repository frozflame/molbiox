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



class Dict(dict):
    """
    Friendly with interactive Python shell
    better displayed if it contains long string

    example:

        {'cmt': 'randSEQ', 'seq': 'TGCTTGGGGAATGTCT'~1000}

    """
    @staticmethod
    def _formatter(s, length=32):
        # always use str.format to support non-string type s
        if len(s) <= length:
            return '{}'.format(repr(s))
        else:
            return '{}~{}'.format(repr(s[:length]), len(s))

    def __repr__(self):
        fmt = Dict._formatter
        kvs = ('{}: {}'.format(repr(k), fmt(v)) for k, v in self.items())
        return '{{{}}}'.format(', '.join(kvs))

    # TODO: provide a __str__ method

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)
