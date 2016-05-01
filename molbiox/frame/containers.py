#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function

import collections
import itertools
import math
import sys

import six

from molbiox.algor.interval import Interval


class SDict(dict):
    def __init__(self, *args, **kwargs):
        super(SDict, self).__init__(*args, **kwargs)
        self.__dict__['attributes'] = set()
        self.__dict__['invisibles'] = set()

    def __repr__(self):
        def fmt(s, length=32):
            # always use str.format to support non-string type s
            if len(repr(s)) <= length:
                return '{}'.format(repr(s))
            else:
                return '{}~{}'.format(repr(s[:length]), len(s))
        pairs = ((k, self[k]) for k in sorted(self) if k not in self.invisibles)
        parts = ('{}: {}'.format(fmt(k), fmt(v)) for k, v in pairs)
        return '{{{}}}'.format(', '.join(parts))

    # TODO: provide a __str__ method

    def __getattr__(self, key):
        if key in self.attributes:
            return self.get(key, None)
        else:
            # just to raise proper error
            return self.__getattribute__(key)

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
        SDict.__init__(self, *args, **kwargs)
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


class TabRecord(collections.OrderedDict):
    def __getattr__(self, key):
        try:
            return self[key]
        except LookupError:
            # just to raise proper error
            return self.__getattribute__(key)

    def __setattr__(self, key, value):
        if key in self:
            self[key] = value
        else:
            self.__dict__[key] = value


class DefaultOrderedDict(collections.OrderedDict):
    # Source: http://stackoverflow.com/a/6190500/562769
    def __init__(self, default_factory=None, *a, **kw):
        if (default_factory is not None and
           not isinstance(default_factory, collections.Callable)):
            raise TypeError('first argument must be callable')
        collections.OrderedDict.__init__(self, *a, **kw)
        self.default_factory = default_factory

    def __getitem__(self, key):
        try:
            return collections.OrderedDict.__getitem__(self, key)
        except KeyError:
            return self.__missing__(key)

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        self[key] = value = self.default_factory()
        return value

    def __reduce__(self):
        if self.default_factory is None:
            args = tuple()
        else:
            args = self.default_factory,
        return type(self), args, None, None, self.items()


class SQueue(object):
    def __init__(self, size=-1, stype=six.text_type):
        size = self.check_size(size)
        self.check_size(size)
        self.free = size
        self.size = size
        self.queue = collections.deque()
        self.stype = stype

    def __len__(self):
        return self.size - self.free

    def __bool__(self):
        return self.__len__() > 0

    def __nonzero__(self):
        return self.__bool__()

    def __iter__(self):
        return iter(self.queue)

    @property
    def glue(self):
        return self.stype()

    @classmethod
    def check_size(cls, size):
        errmsg = "size must be a non-negative integer or -1"
        if not isinstance(size, six.integer_types):
            raise ValueError(errmsg)
        if size < -1:
            raise ValueError(errmsg)
        if size == -1:
            return sys.maxsize
        else:
            return size

    def get(self, size=-1):
        size = self.check_size(size)
        # get all
        if size >= len(self):
            string = self.glue.join(self.queue)
            self.queue.clear()
            self.free = self.size
            return string
        # get a string of requested length
        else:
            substring = self.glue
            substrings = []
            # loop until self.queue exhausted or length reached
            # while self.queue and size > 0:
            #  -- when queue exhausted, size must be 0 or negative
            while size > 0:
                substring = self.queue.popleft()
                substrings.append(substring[:size])
                size -= len(substring)
            if size < 0:
                self.queue.appendleft(substring[size:])
            string = self.glue.join(substrings)
            self.free += len(string)
            return string

    def peek(self, size=-1):
        size = self.check_size(size)
        if size >= len(self):
            return self.glue.join(self.queue)
        else:
            ique = iter(self.queue)
            substrings = []
            while size > 0:
                substring = next(ique)[:size]
                substrings.append(substring)
                size -= len(substring)
            return self.glue.join(substrings)

    def put(self, string):
        """
        Add ``string[:self.free]`` to the queue.
        :param string:
        :return: string[self.free:]
        """
        if len(string) > self.free:
            retval = string[self.free:]
            self.queue.append(string[:self.free])
            self.free = 0
            return retval
        elif len(string) > 0:
            self.queue.append(string)
            self.free -= len(string)
        return self.glue


class CycleString(object):
    def __init__(self, string):
        """
        :param string: a non-empty string. unicode or str for python2; str for python3
        """
        if not isinstance(string, six.string_types):
            msg = 's must be of type {}, got {}'.format(
                ' or '.join(six.string_types), type(string))
            raise TypeError(msg)
        if len(string) < 1:
            raise ValueError('s cannot be an empty string')
        self.chars = itertools.cycle(string)

    def __getitem__(self, key):
        if isinstance(key, six.integer_types):
            return itertools.islice(self, key, key + 1)
        elif isinstance(key, slice):
            step = 1 if key.step is None else key.step
            intv = Interval.from_slice(key, float('inf'))
            if math.isinf(intv.integers_count(step)):
                raise ValueError('resulting string of infinite length')
            chars = itertools.islice(self.chars, key.start, key.stop, key.step)
            return ''.join(chars)