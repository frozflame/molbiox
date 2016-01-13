#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function


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