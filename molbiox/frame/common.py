#!/usr/bin/env python3
# coding: utf-8
from __future__ import unicode_literals, print_function


Dict = dict


class SRecord(dict):
    """
    Friendly with interactive Python shell
    better displayed if it contains long string

    example:

        {'cmt': 'randSEQ', 'seq': 'TGCTTGGGGAATGTCT'~1000}

    """
    __dot_accessible__ = {'cmt', 'seq'}

    def __repr__(self):
        def fmt(s, length=32):
            # always use str.format to support non-string type s
            if len(s) <= length:
                return '{}'.format(repr(s))
            else:
                return '{}~{}'.format(repr(s[:length]), len(s))
        kvs = ('{}: {}'.format(repr(k), fmt(v)) for k, v in self.items())
        return '{{{}}}'.format(', '.join(kvs))

    # TODO: provide a __str__ method

    def __getattr__(self, key):
        if key in SRecord.__dot_accessible__:
            return self.get(key, None)
        else:
            return self.__getattribute__(key)

    def __setattr__(self, key, value):
        if key in SRecord.__dot_accessible__:
            self[key] = value
        else:
            self.__dict__[key] = value
