#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function

import six
from lxml.etree import tostring
from lxml.builder import E

from molbiox.frame.environ import get_template


default_polygon_style = {
    'stroke-width': 1,
    'fill-opacity': 0.7,
    'stroke': 'black',
    'stroke-opacity': 0.8,
    'fill': 'red',
}


default_text_style = {
    'font-size': 12,
    'font-family': 'Times New Roman',
}


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


def make_polygon(points, style=None, render=True):
    user_style = style or dict()
    style = dict(default_polygon_style)
    style.update(user_style)
    style = format_style(style)
    if not isinstance(points, six.string_types):
        points = format_points(points)
    elem = E.polygon(points=points, style=style)
    if render:
        return tostring(elem)
    else:
        return elem


def make_text(content, x, y, rx, ry, angle=0, style=None, render=True):
    user_style = style or dict()
    style = dict(default_polygon_style)
    style.update(user_style)
    attributes = {
        'x': '{}'.format(x),
        'y': '{}'.format(y),
        'transform': 'rotate({} {},{})'.format(angle, rx, ry),
        'style': format_style(style),
    }
    elem = E.text(content, **attributes)
    if render:
        return tostring(elem)
    else:
        return elem


def render_svg(**kwargs):
    tpl = get_template('d.svg_maker.xml')
    return tpl.render(**kwargs)
