#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import sys
import six


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
        mode = getattr(self.file, 'mode', '')
        if 'b' not in mode and isinstance(string, six.binary_type):
            return self.file.write(string.decode())
        if 'b' in mode and isinstance(string, six.text_type):
            return self.file.write(string.encode())
        return self.file.write(string)

    def read(self, size):
        mode = getattr(self.file, 'mode', '')
        string = self.file.read(size)
        if 'b' not in mode and isinstance(string, six.binary_type):
            return string.decode()
        if 'b' in mode and isinstance(string, six.text_type):
            return string.encode()
        return string

    def __enter__(self):
        return self

    def __exit__(self, typ, value, traceback):
        self.close()


def make_array(data):
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


def safe_bracket(container, key, default=None, cast=None):
    try:
        val = container[key]
    except LookupError:
        return default

    if cast:
        return cast(val)
    else:
        return val