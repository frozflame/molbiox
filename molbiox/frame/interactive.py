#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import sys
import shelve
from functools import wraps
import six
from molbiox import settings
from molbiox.tolerant import pick_nth


class KVStore(shelve.DbfilenameShelf):
    @classmethod
    def open(cls, filename=settings, flag='c', protocol=None, writeback=False):
        return cls(filename, flag, protocol, writeback)

    @property
    def k(self):
        return list(self.keys())

    @property
    def v(self):
        return list(self.values())

    @property
    def p(self):
        return list(self.items())


def connect(dbname='microbe'):
    import dataset
    url = 'postgresql://Hailong:lyzn@localhost:5432/{}'.format(dbname)
    return dataset.connect(url)


def intersect(container1, container2):
    return set(container1) & set(container2)


def union(container1, container2):
    return set(container1) | set(container2)


def castable(func):
    """
    Cast a generator function to list, set, or select n-th item, etc

        castable_func(..., castfunc=list)   <=>  list(castable_func(...))
        castable_func(..., castfunc=1)      <=>  list(castable_func(...))[1]

    Just to make interactive use of some functions easier

    :param func: a generator function
    :return:
    """
    @wraps(func)
    def _decorated_func(*args, **kwargs):
        castfunc = None
        if 'castfunc' in kwargs:
            castfunc = kwargs['castfunc']
            del kwargs['castfunc']

            # shortcut to pick up nth record
            if isinstance(castfunc, int):
                number = castfunc
                castfunc = lambda result: pick_nth(result, number)

        result = func(*args, **kwargs)
        if castfunc:
            result = castfunc(result)
        return result
    return _decorated_func


class FileWrapper(object):
    def __init__(self, file_, mode):
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

    def close(self):
        if self.path:
            self.file.close()

    def write(self, string):
        if 'b' not in self.file.mode and isinstance(string, six.binary_type):
            return self.file.write(string.decode())
        if 'b' in self.file.mode and isinstance(string, six.text_type):
            return self.file.write(string.encode())
        return self.file.write(string)

    def read(self, size):
        string = self.file.read(size)
        if 'b' not in self.file.mode and isinstance(string, six.binary_type):
            return string.decode()
        if 'b' in self.file.mode and isinstance(string, six.text_type):
            return string.encode()
        return string


def array(data):
    import numpy as np
    if isinstance(data, np.ndarray):
        arr = data
    elif isinstance(data, (list, int, float)):
        arr = np.array(data)
    else:
        arr = np.array(list(data))
    if arr.ndim == 0:
        arr.shape = -1
    return arr



