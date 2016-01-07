#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import numpy as np
from jinja2 import Template

from molbiox.io import tabular
from molbiox.frame import interactive
from molbiox.frame.locate import locate_template


def format_points(data):
    """
    :param data: n*k*2
    :return:
    """
    if not isinstance(data, np.ndarray):
        arr = np.array(data)
    else:
        arr = data
    if arr.ndim != 3 or arr.shape[-1] != 2:
        raise ValueError("'arr' should be of shape (n, k, 2)")
    for elem in arr:
        string = ' '.join('{},{}'.format(*pair) for pair in elem)
        yield string


def format_style(dic):
    return '; '.join('{}: {}'.format(k, v) for k, v in dic.items())


def get_defaults(**kwargs):
    polygon_style = {
        'stroke-width': 0,
        'fill-opacity': 1,
        'stroke': 'black',
        'stroke-opacity': 0,
        'fill': 'red',
    }
    text_style = {
        'font-size': 9,
        'font-family': 'Times New Roman',
    }

    if 'polygon_style' in kwargs:
        polygon_style.update(kwargs['polygon_style'])
    if 'text_style' in kwargs:
        text_style.update(kwargs['text_style'])

    return {
        'polygon_style': format_style(polygon_style),
        'text_style': format_style(text_style),
        # 'text_angle': -60,
    }


LWC_TABLE = [
    ('name',    None),
    ('shape',   None),
    ('head',    int),
    ('tail',    int),
    ('strand',  None),
    ('color',   None),
    # sample:
    # https://github.com/frozflame/ClusterViz/blob/master/sample_input.dat
]


@interactive.castable
def read_lwcfile(infile, scale, normalize=True):
    """
    Cannot handle very large file
    :param infile: a string for path, or file object
    :param normalize: boolean. If true, shift to make leftmost point 0
    :param scale: a number. All head and tail values will be divided by this num
    :return:
    """
    items = tabular.read(infile, LWC_TABLE, castfunc=list)

    if normalize:
        minpos = min(min(item['head'], item['tail']) for item in items)
    else:
        minpos = 0.

    for item in items:
        element = get_defaults(polygon_style=dict(fill=item['color']))
        # print(element, file=sys.stderr)
        head = min(item['head'], item['tail'])
        tail = max(item['head'], item['tail'])
        if item['strand'] == '-':
            element['head'] = (tail - minpos) * 1. / scale
            element['tail'] = (head - minpos) * 1. / scale
        else:
            element['head'] = (head - minpos) * 1. / scale
            element['tail'] = (tail - minpos) * 1. / scale
        # element['']
        element['text'] = item['name']
        yield element


def render_svg(**kwargs):
    # font-size: 12; font: Arial
    tpl_path = locate_template('d.arrows.xml')
    tpl = open(tpl_path).read()
    tpl = Template(tpl)
    return tpl.render(**kwargs)
