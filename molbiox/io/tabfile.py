#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
from collections import OrderedDict


def read(handle, fields, sep=None):
    """
    Read a tab file
    """
    if hasattr(handle, 'read'):
        infile = handle
    else:
        infile = open(handle)

    for line in infile:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        values = line.split(sep)

        pairs = []
        for (key, cast), val in zip(fields, values):
            if cast:
                val = cast(val)
            pairs.append((key, val))

        yield OrderedDict(pairs)

    if infile is not handle:
        infile.close()



