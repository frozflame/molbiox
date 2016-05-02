#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
# import sys


def parse_strand(s):
    try:
        return int(s)
    except ValueError:
        return {'+': 1, '-': -1}[s]


awt = [
    ('uid',     None),      # unique id
    ('gid',     None),      # group id
    ('strand',  parse_strand),      # + or -
    ('head',    int),       # endpoint position
    ('tail',    int),
    ('label',   None),      # mostly, name of the gene
    ('shape',   None),      # arrow, box, ...
    ('color',   None),
    ('batch',   None),
]

lwc = [
    ('label',    None),
    ('shape',   None),
    ('head',    int),
    ('tail',    int),
    ('strand',  parse_strand),
    ('color',   None),
    # sample:
    # https://github.com/frozflame/ClusterViz/blob/master/sample_input.dat
]

