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

