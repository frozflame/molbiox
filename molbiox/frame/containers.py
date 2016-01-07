#!/usr/bin/env python3
# coding: utf-8
from __future__ import unicode_literals, print_function
import itertools


class SDict(dict):

    def __init__(self, *args, **kwargs):
        super(SDict, self).__init__(*args, **kwargs)
        self.__dict__['attributes'] = set()
        self.__dict__['invisibles'] = set()

    def __repr__(self):
        def fmt(s, length=32):
            # always use str.format to support non-string type s
            if len(s) <= length:
                return '{}'.format(repr(s))
            else:
                return '{}~{}'.format(repr(s[:length]), len(s))
        pairs = ((k, self[k]) for k in sorted(self) if k not in self.invisibles)
        parts = ('{}: {}'.format(fmt(k), fmt(v)) for k, v in pairs)
        return '{{{}}}'.format(', '.join(parts))

    # TODO: provide a __str__ method

    def __getattr__(self, key):
        try:
            return self.__getattribute__(key)
        except AttributeError:
            if key in self.attributes:
                return self.get(key, None)
            else:
                raise

    def __setattr__(self, key, value):
        if key in self.attributes:
            self[key] = value
        else:
            self.__dict__[key] = value


class SRecord(SDict):
    """
    Friendly with interactive Python shell
    better displayed if it contains long string

    example:

        {'cmt': 'randSEQ', 'seq': 'TGCTTGGGGAATGTCT'~1000}:@5000

    where 5000 is the offset value
    """
    def __init__(self, *args, **kwargs):
        super(SRecord, self).__init__(*args, **kwargs)
        self.attributes.update({'cmt', 'seq', 'offset'})
        self.invisibles.add('offset')

    def __repr__(self):
        repr_ = super(SRecord, self).__repr__()
        if self.offset:
            repr_ += ':@{}'.format(self.offset)
        return repr_

    def divide(self, limit):
        for offset in itertools.count(0, limit):
            seq = self.seq[offset: offset+limit]
            yield SRecord(cmt=self.cmt, seq=seq, offset=offset)

