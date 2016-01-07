#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
from functools import wraps
from itertools import islice


def castable(func):
    """
    Cast a generator function to list, set, or select n-th item, etc

        castable_func(..., castfunc=list)   <=>  list(castable_func(...))
        castable_func(..., castfunc=1)      <=>  list(castable_func(...))[1]

    Just to make interactive use of some functions easier

    :param func: a generator function
    :return:
    """
    @wraps(func)
    def _decorated_func(*args, **kwargs):
        castfunc = None
        if 'castfunc' in kwargs:
            castfunc = kwargs['castfunc']
            del kwargs['castfunc']

            # shortcut to pick up nth record
            if isinstance(castfunc, int):
                n = castfunc
                castfunc = lambda result: next(islice(result, n, None))

        result = func(*args, **kwargs)
        if castfunc:
            result = castfunc(result)
        return result
    return _decorated_func
