#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
from functools import wraps

def safe_bracket(container, key, default=None, cast=None):
    try:
        val = container[key]
    except LookupError:
        return default

    if cast:
        return cast(val)
    else:
        return val


def castable(func):

    @wraps(func)
    def _decorated_func(*args, **kwargs):
        castfunc = None
        if 'castfunc' in kwargs:
            castfunc = kwargs['castfunc']
            del kwargs['castfunc']

            print(kwargs)

        result = func(*args, **kwargs)
        if castfunc:
            result = castfunc(result)
        return result

    return _decorated_func

