#!/usr/bin/env python3
# coding: utf-8

import math
import re
import six
from molbiox.frame import interactive


def overlap_size(a1, a2, b1, b2):
    """
    Calculate overlap size of intervals (a1, a2) and (b1, b2)
    """
    alen = abs(a1-a2)
    blen = abs(b1-b2)
    wide = max(a1, a2, b1, b2) - min(a1, a2, b1, b2)
    return alen + blen - wide


class Interval(object):
    def __init__(self, a, b, ainc=True, binc=False):
        self.a = a
        self.b = b
        self.ainc = ainc
        self.binc = binc
        self.standardize()

    @classmethod
    def gen(cls, string=None):
        if string is None:
            return cls(0., 0., False, False)
        regex = re.compile(r'^([\[\(])([^,]+),([^,]+)([\]\)])$')
        mat = regex.match(string.strip())
        if mat is None:
            raise ValueError('incorrect interval syntax')
        a = interactive.numb_convert(mat.group(2))
        b = interactive.numb_convert(mat.group(3))
        ainc = {'[': True, '(': False}[mat.group(1)]
        binc = {']': True, ')': False}[mat.group(4)]
        return cls(a, b, ainc, binc)

    @classmethod
    def from_gt(cls, number):
        return cls(number, float('inf'), False, False)

    @classmethod
    def from_ge(cls, number):
        return cls(number, float('inf'), True, False)

    @classmethod
    def from_lt(cls, number):
        return cls(float('-inf'), number, False, False)

    @classmethod
    def from_le(cls, number):
        return cls(float('-inf'), number, False, True)

    @classmethod
    def from_eq(cls, number):
        return cls(number, number, True, True)

    @classmethod
    def from_slice(cls, sli, size):
        idx_interval = cls(0, size, True, False)
        if not idx_interval:
            return cls.gen()
        a = 0 if sli.start is None else sli.start
        a = a if a >= 0 else a + size
        a = idx_interval.confine(a)

        b = size if sli.stop is None else sli.stop
        b = b if b >= 0 else b + size
        b = idx_interval.confine(b)
        return cls(a, b, True, False)

    def __bool__(self):
        if self.a < self.b:
            return True
        if self.a == self.b and self.ainc and self.binc:
            return True
        return False

    def __nonzero__(self):
        return self.__bool__()

    def standardize(self):
        if not self:
            self.a = 0
            self.b = 0
            self.ainc = False
            self.binc = False
            return
        if math.isinf(self.a):
            self.ainc = False
        if math.isinf(self.b):
            self.binc = False

    def __str__(self):
        return '{}{}, {}{}'.format(
            {True: '[', False: '('}[self.ainc],
            self.a,
            self.b,
            {True: ']', False: ')'}[self.binc],
        )

    def __repr__(self):
        # clspath = interactive.get_clspath(self.__class__)
        clsname = self.__class__.__name__
        return '{}.gen({})'.format(clsname, repr(self.__str__()))

    @property
    def length(self):
        return self.b - self.a

    def __contains__(self, number):
        if not self:
            return False
        if self.a < number < self.b:
            return True
        if number == self.a and self.ainc:
            return True
        if number == self.b and self.binc:
            return True
        return False

    @staticmethod
    def gapsize(intv1, intv2):
        mi = min(intv1.a, intv1.b, intv2.a, intv2.b)
        mx = max(intv1.a, intv1.b, intv2.a, intv2.b)
        return mx - mi - intv1.length - intv2.length

    @classmethod
    def overlap(cls, intv1, intv2):
        if not (intv1 and intv2):
            return cls.gen()
        if cls.gapsize(intv1, intv2) > 0:
            return cls.gen()

        endpoints = [intv1.a, intv1.b, intv2.a, intv2.b]
        endpoints.sort()
        a = endpoints[1]
        b = endpoints[2]
        ainc = a in intv1 and a in intv2
        binc = b in intv1 and b in intv2
        return cls(a, b, ainc, binc)

    def confine(self, number):
        if not self:
            return None
        if number < self.a:
            return self.a
        if number > self.b:
            return self.b
        return number

    def integers(self, step):
        start = int(math.ceil(self.a))
        if not isinstance(step, six.integer_types):
            raise TypeError('step must be an integer')
        while start in self:
            yield start
            start += step

    def integers_count(self, step):
        if not isinstance(step, six.integer_types):
            raise TypeError('step must be an integer')

        # (self.lenth < 0) or ( =0 and not inclusive on both side)
        if not self:
            return 0
        if self.length == 0:
            # if self.a is an integer
            if self.a in self:
                return 1
            else:
                return 0
        count = math.floor(self.b) - math.ceil(self.a)
        if self.ainc and float(self.a).is_integer():
            count += 1
        if self.binc and float(self.b).is_integer():
            count += 1
        return count


class IntervalSet(object):
    def __init__(self, *intervals):
        self.intervals = list(intervals)

    @classmethod
    def overlap(cls, intvs1, intvs2):
        pass


