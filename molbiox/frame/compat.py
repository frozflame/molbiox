#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals
import sys
import six

"""
Compatibility issues
"""

# be Python 3 compatible
if sys.version.startswith('3'):
    zrange = range
    binstr = bytes
    unistr = str
else:
    zrange = xrange     # use six.moves.range instead
    binstr = str        # six.binary_type
    unistr = unicode    # six.text_type


# maketrans
if sys.version.startswith('3'):
    maketrans = str.maketrans
else:
    import string
    maketrans = string.maketrans


def omni_writer(outfile, string, encoding='ascii'):
    if 'b' not in outfile.mode and isinstance(string, six.binary_type):
        return outfile.write(string.decode(encoding))
    if 'b' in outfile.mode and isinstance(string, six.text_type):
        return outfile.write(string.encode(encoding))
    return outfile.write(string)
