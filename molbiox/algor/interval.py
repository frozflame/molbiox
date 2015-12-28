#!/usr/bin/env python3
# coding: utf-8

import math


def overlap_size(a1, a2, b1, b2):
    """
    Calculate overlap size of intervals (a1, a2) and (b1, b2)
    """
    alen = abs(a1-a2)
    blen = abs(b1-b2)
    wide = max(a1, a2, b1, b2) - min(a1, a2, b1, b2)
    return alen + blen - wide


def overlap(a1, a2, b1, b2):
    pass


def group_by_overlap(intervals):
    pass
