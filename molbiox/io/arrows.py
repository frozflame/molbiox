#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import sys
import six
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
        'font-size': 12,
        'font-family': 'Times New Roman',
    }

    if 'polygon_style' in kwargs:
        polygon_style.update(kwargs['polygon_style'])
    if 'text_style' in kwargs:
        text_style.update(kwargs['text_style'])

    return {
        'polygon_style': format_style(polygon_style),
        'text_style': format_style(text_style),
        'text_transform': 'rotate(30 20,40)',
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
def read_lwcfile(infile):
    for item in tabular.read(infile, LWC_TABLE):
        element = get_defaults(polygon_style=dict(fill=item['color']))
        # print(element, file=sys.stderr)
        head = min(item['head'], item['tail'])
        tail = max(item['head'], item['tail'])
        if item['strand'] == '-':
            element['head'] = tail
            element['tail'] = head
        else:
            element['head'] = head
            element['tail'] = tail
        # element['']
        element['text'] = item['name']
        yield element


def render_svg(**kwargs):
    # font-size: 12; font: Arial
    tpl_path = locate_template('d.arrows.xml')
    tpl = open(tpl_path).read()
    tpl = Template(tpl)
    return tpl.render(**kwargs)
