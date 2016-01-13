#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import six


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


def u(string):
    """
    Convert a string to text_type
    unicode in Python 2; str in Python 3

    :param string: a string containing only ascii characters
    :return: a unicode object
    """
    if isinstance(string, six.text_type):
        return string
    elif isinstance(string, six.binary_type):
        return string.decode('ascii')
    else:
        tt = six.text_type
        bt = six.binary_type
        errmsg = 'string must be of type {} or {}'.format(tt, bt)
        raise TypeError(errmsg)


def b(string):
    """
    Convert a string to text_type
    unicode in Python 2; str in Python 3

    :param string: a string containing only ascii characters
    :return: a unicode object
    """
    if isinstance(string, six.binary_type):
        return string
    elif isinstance(string, six.text_type):
        return string.encode('ascii')
    else:
        tt = six.text_type
        bt = six.binary_type
        errmsg = 'string must be of type {} or {}'.format(tt, bt)
        raise TypeError(errmsg)
