#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import sys
import numpy
import six
from lxml.builder import E, ET


def format_style(style):
    if not isinstance(style, dict):
        style = dict(style)
    return '; '.join('{}: {}'.format(k, v) for k, v in style.items())


def format_points(points):
    """
    :param points: [(x0, y0), (x1, y1), ...] or equivolent iterable
    :return:
    """
    return ' '.join('{},{}'.format(*pair) for pair in points)


def make_polygon(points, style):
    if not isinstance(points, six.string_types):
        points = format_points(points)
    if not isinstance(style, six.string_types):
        style = format_style(style)
    return E.polygon(points=points, style=style)


def make_text(content, style, x, y, rx, ry, angle=0):
    attributes = {
        'x': '{}'.format(x),
        'y': '{}'.format(y),
        'transform': 'rotate({} {},{})'.format(angle, rx, ry)
    }
    return E.text(content, **attributes)

