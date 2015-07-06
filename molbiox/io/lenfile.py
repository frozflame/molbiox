#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals

__author__ = 'Hailong'


def read(handle, verbose=False):
    """
    Parse file format like `wc` or `fastalength` output

    Say we have

        264531 2045177 65877908 google.chrome.dmg
        181167 1408149 48452451 picasa.mac.39.dmg
        ...

    Then we will get

        {
            'google.chrome.dmg': 264531,
            'picasa.mac.39.dmg': 181167,
        }

    Or if `tupl` is True

        {
            'google.chrome.dmg': (264531, 2045177, 65877908),
            'picasa.mac.39.dmg': (181167, 1408149, 48452451),
        }
    """
    if hasattr(handle, 'read'):
        infile = handle
    else:
        infile = open(handle)

    resdict = dict()
    for line in infile:
        line = line.strip()

        # skip empty line or comment
        if not line or line.startswith('#'):
            continue

        itemlist = line.split()
        key = itemlist[-1]

        if verbose:
            val = tuple(int(x) for x in itemlist[:-1])
        else:
            val = int(itemlist[0])
        resdict[key] = val

    if infile is not handle:
        infile.close()

    return resdict


