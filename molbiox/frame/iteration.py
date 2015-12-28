#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import sys
import itertools


# def grouper(iterable, chunksize):
#     """Collect data into fixed-length chunks or blocks"""
#     for i in itertools.count(0):
#         yield itertools.islice(iterable, i*chunksize, (i+1)*chunksize)


def chunkwise(chunksize, *args):
    # args are strings
    for i in itertools.count(0):
        r = [s[i*chunksize:(i+1)*chunksize] for s in args]
        if any(r):
            yield r
        else:
            raise StopIteration
