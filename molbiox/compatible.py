#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals
import sys

# be Python 3 compatible
if sys.version.startswith('3'):
    zrange = range
    binstr = bytes
    unistr = str
else:
    zrange = xrange
    binstr = str
    unistr = unicode

