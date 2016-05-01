#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import itertools
import os
import sys
import six
from molbiox.frame import containers, compat, interactive


class FQueue(containers.SQueue):
    def put(self, string, split=True):
        if len(string) > self.free:
            raise ValueError('string is too large to fit in this FQueue')
        if split:
            for line in string.splitlines(True):
                containers.SQueue.put(self, line)
        else:
            containers.SQueue.put(self, string)

    def read(self, size=-1):
        size = self.check_size(size)
        return self.get(size)

    def readline(self, size=-1):
        size = self.check_size(size)
        if self:
            size = min(len(self.queue[0]), size)
            return self.read(size)
        else:
            return self.glue

    def readlines(self, size=-1):
        lines = []
        size = self.check_size(size)
        while self and size > 0:
            line = self.readline(size=-1)
            size -= len(line)
            lines.append(line)
        return lines


class FileAdapter(object):
    def __init__(self, file_, mode):
        mode = compat.u(mode)
        self.mode = mode

        if 'b' in mode:
            self.stype = six.binary_type
        else:
            self.stype = six.text_type

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

    def __iter__(self):
        return self

    def __next__(self):
        line = self.readline(size=-1)
        if line == '':
            raise StopIteration()
        return line

    def next(self):
        return self.__next__()

    @classmethod
    def new(cls, file_, mode):
        if isinstance(file_, cls):
            return file_
        else:
            return cls(file_, mode)

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

    def write(self, string):
        string = self.convert(string)
        return self.file.write(string)

    def read(self, size=-1):
        """
        :param size: a non-negative integer or -1
        :return:
        """
        return self.convert(self.file.read(size))

    def readline(self, size=-1):
        return self.convert(self.file.readline(size))

    def readlines(self, size=-1):
        lines = self.file.readlines(size)
        lines = [self.convert(l) for l in lines]
        return lines


class FilePeeker(FileAdapter):
    def __init__(self, file_, mode):
        super(self.__class__, self).__init__(file_, mode)
        self.fqueue = FQueue(size=-1, stype=self.stype)
        self._peek = False

    @property
    def peek(self):
        return self._peek

    @peek.setter
    def peek(self, value):
        value = bool(value)
        if value == self.peek:
            return

        if value and self.fqueue:
            raise ValueError('previously peeked frontier not reached')

        if not value and self.fqueue:
            string = self.fqueue.queue[-1]
            if not string.endswith(os.linesep):
                self.fqueue.queue.pop()
                string += self.file.readline()
                self.fqueue.queue.append(string)
        self._peek = value

    def close(self):
        if self.path and not self.peek:
            self.file.close()

    def read(self, size=-1):
        """
        When self.peek == False,
            only read from actual file when self.fqueue is exhausted.
        When self.peek == True,
            always read from actural file and put content into self.fqueue.
        :param size: a non-negative integer or -1
        :return:
        """
        # read from fqueue
        if not self.peek:
            qstring = self.fqueue.read(size)
            if size != -1:
                size -= len(qstring)
        else:
            qstring = self.stype()

        # read actual file if size not reached
        fstring = self.convert(self.file.read(size))

        # store peeked string to fqueue
        if self.peek and fstring:
            self.fqueue.put(fstring)
        return qstring + fstring

    def readline(self, size=-1):
        # read from fqueue
        if not self.peek:
            string = self.fqueue.readline(size)
        else:
            string = self.stype()

        # read from actual file if string is empty
        if not string:
            string = self.convert(self.file.readline(size))

        # store peeked string to fqueue
        if self.peek and string:
            self.fqueue.put(string)
        return string

    def readlines(self, size=-1):
        # read from fqueue
        if not self.peek:
            lines = self.fqueue.readlines(size)
        else:
            lines = []

        # read from actual file if size not reached
        if size == -1:
            lines.extend(self.file.readlines(-1))
        else:
            length = sum(len(l) for l in lines)
            if size > length:
                xlines = self.file.readlines(size - length)
                xlines = [self.convert(l) for l in xlines]
                lines.extend(xlines)
        # store to fqueue
        if self.peek and lines:
            for line in lines:
                self.fqueue.put(line, split=False)
        return lines


def chunkwize_parallel(chunksize, *args):
    # args are strings or lists
    chunksize = int(chunksize)
    for i in itertools.count(0):
        r = [s[i*chunksize:(i+1)*chunksize] for s in args]
        if any(r):
            yield r
        else:
            raise StopIteration


def chunkwize(chunksize, items):
    """
    :param chunksize: an integer
    :param items: an iterable
    :return: a generator
    """
    chunksize = int(chunksize)
    chunk = []
    for i in items:
        if len(chunk) >= chunksize:
            yield chunk
            chunk = []
        chunk.append(i)
    yield chunk


@interactive.castable
def alternate(*iters):
    dummy = object()
    zip_longest = six.moves.zip_longest
    alt = itertools.chain(*zip_longest(*iters, fillvalue=dummy))
    for item in alt:
        if item is not dummy:
            yield item
