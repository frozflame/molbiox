#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import sys
import time


class Timer(object):
    def __init__(self, name='anonym'):
        self.name = name

    def __enter__(self):
        self.time = time.time()
        return self

    def __exit__(self, typ, value, traceback):
        interval = time.time() - self.time
        msg = 'timer {}: {} sec'.format(self.name, interval)
        print(msg, file=sys.stderr)

