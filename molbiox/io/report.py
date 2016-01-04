#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import sys
import math


def file_size(number, sep=" "):
    units = ["bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    for unit in units:
        if number < 10000 or unit == "YB":
            return "{}{}{}".format(int(number), sep, unit)
        else:
            number /= 1024.


def prefix(num):
    if num >= 1000:
        for v, p in enumerate('kMGTPEZY'):
            num /= 1000.
            if num <= 1000:
                return num, p, v
        return num, p, v
    if num <= .001:
        for v, p in enumerate('munp'):
            num *= 1000.
            if num >= 1:
                return num, p, v
        return num, p, v
    return num, '', 0


if __name__ == '__main__':
    res = prefix(float(sys.argv[1]))
    print(res)

