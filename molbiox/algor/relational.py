#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function

import operator
from collections import OrderedDict

"""
Functionalities resembling  a relational database
"""


def select_top_records(records, groupby, orderby=None, compare=operator.gt):
    """
    Select top records, `select gb, max(ob) group by gb`

    :param records: a list of (or an iterable iterates) dicts
    :param groupby: group by this field
    :param orderby: order by this field. If None, assume ordered already
    :param compare: compare(a, b) == True means a is better than b
    :return:
    """
    hitdict = OrderedDict()
    for rec in records:
        key = rec[groupby]
        if key in hitdict:
            if orderby and compare(rec[orderby], hitdict[key][orderby]) > 0:
                hitdict[key] = rec
        else:
            hitdict[key] = rec
    return hitdict


