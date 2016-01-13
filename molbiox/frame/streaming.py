#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import itertools
import sys
import six
from molbiox.frame.containers import SQueue


class FQueue(SQueue):
    def put(self, string):
        if len(string) > self.free:
            raise ValueError('string is too large to fit in this FQueue')
        for line in string.splitlines(True):
            SQueue.put(self, line)

    def read(self, size=-1, peek=False):
        size = self.check_size(size)
        if peek:
            qstring = self.peek(size)
        else:
            qstring = self.get(size)
        return qstring

    def readline(self, size=-1, peek=False):
        size = self.check_size(size)
        if self:
            line = self.queue[0]
            size = min(len(line), size)
            return self.read(size, peek)
        else:
            return self.glue

    def readlines(self, size=-1, peek=False):
        lines = []
        size = self.check_size(size)
        while self and size > 0:
            line = self.readline(size=-1, peek=peek)
            size -= len(line)
            lines.append(line)
        return lines


class FileWrapper(object):
    def __init__(self, file_, mode):
        mode = six.u(mode)
        self.mode = mode

        if 'b' in mode:
            self.stype = six.binary_type
            # self.
        else:
            self.stype = six.text_type
        self.fqueue = FQueue(size=-1, stype=self.stype)

        if isinstance(file_, six.string_types):
            if file_ == '-' and 'r' in mode:
                self.file = sys.stdin
                self.path = ''
            elif file_ == '-' and ('w' in mode) or ('a' in mode):
                self.file = sys.stdout
                self.path = ''
            else:
                self.file = open(file_, mode)
                self.path = file_
        else:
            self.file = file_
            self.path = ''

    def __enter__(self):
        return self

    def __exit__(self, typ, value, traceback):
        self.close()

    def __next__(self):
        return self.readline(size=-1, peek=False)

    def close(self):
        if self.path:
            self.file.close()

    def convert(self, string):
        """
        Convert string to correct type (str or bytes)
        :param string: a str or bytes object
        """
        if self.stype == six.text_type and isinstance(string, six.binary_type):
            return string.decode()
        if self.stype == six.binary_type and isinstance(string, six.text_type):
            return string.encode()
        return string

    def _fq_store(self, string, peek):
        if peek:
            if not (string.endswith('\n') or string.endswith('\r')):
                string += self.file.readline()
            self.fqueue.put(string)

    def write(self, string):
        string = self.convert(string)
        return self.file.write(string)

    def read(self, size=-1, peek=False):
        """
        Only read from actual file when self.squeue is exhausted.
        :param size: a non-negative integer or -1
        :param peek: boolean. If true, do not consume data
        :return:
        """
        qstring = self.fqueue.read(size, peek)
        if size != -1:
            size -= len(qstring)
        fstring = self.convert(self.file.read(size))
        self._fq_store(fstring, peek)
        return qstring + fstring

    def readline(self, size=-1, peek=False):
        string = self.fqueue.readline(size, peek)
        if not string:
            string = self.convert(self.file.readline(size))
            self._fq_store(string, peek)
        return string

    def readlines(self, size=-1, peek=False):
        lines = self.fqueue.readlines(size, peek)
        if size == -1:
            lines.extend(self.file.readlines(-1))
        else:
            length = sum(len(l) for l in lines)
            if size > length:
                xlines = self.file.readlines(size - length)
                xlines = [self.convert(l) for l in xlines]
                lines.extend(xlines)
        return lines


def chunkwise(chunksize, *args):
    # args are strings
    for i in itertools.count(0):
        r = [s[i*chunksize:(i+1)*chunksize] for s in args]
        if any(r):
            yield r
        else:
            raise StopIteration
