#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function


def safe_bracket(container, key, default=None, cast=None):
    try:
        val = container[key]
    except LookupError:
        return default

    if cast:
        return cast(val)
    else:
        return val


def pick_nth(items, n):
    # avoid dead loop
    if not isinstance(n, int):
        return None

    for i, x in enumerate(items):
        if i == n:
            return x
        elif i < n:
            continue
        else:
            return None
