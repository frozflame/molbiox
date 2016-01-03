#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import sys


def file_size(number, sep=" "):
    units = ["bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    for unit in units:
        if number < 10000 or unit == "YB":
            return "{}{}{}".format(int(number), sep, unit)
        else:
            number /= 1024.


