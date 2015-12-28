#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
from functools import wraps
from time import time

def decorator3(func):

    @wraps(func)
    def _decorated_func(*args, **kwargs):

        print("<function call begin>")
        print("<function name: {}>".format(func.__name__))

        t = time.time()

        func(*args, **kwargs)

        t = time.time() - t

        print("<function call end>[timecosts: {}s]".format(t))

    return _decorated_func

