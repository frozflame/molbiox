#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import sys
import numpy as np
from molbiox.io import tabular
from molbiox.frame import interactive

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
        head = min(item['head'], item['tail'])
        tail = max(item['head'], item['tail'])
        if item['strand'] == '-':
            item['head'] = tail
            item['tail'] = head
        else:
            item['head'] = head
            item['tail'] = tail
        yield item


def make(data):
    """
    :param data: an N*8*2 array
    :return:
    """
    return data


style_polygon = {
    'stroke-width': 0,
    'fill-opacity': 1,
    'stroke': 'black',
    'stroke-opacity': 0,
    'fill': 'red',
}

style_text = {
    'font-size': 12,
    'font': 'Serif',    # Times New Roman?
}
# font-size: 12; font: Arial

data_points = [
    [(1, 2), (1, 3), (1, 4)],
    [(2, 2), (2, 3), (2, 4)],
]


def format_points(data):
    """
    :param arr: n*k*2
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


if __name__ == '__main__':
    # print(format_style(style_polygon))
    for s in format_points(data_points):
        print(s)
