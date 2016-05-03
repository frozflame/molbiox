#!/usr/bin/env python3
# coding: utf-8

from __future__ import division, unicode_literals, print_function

from molbiox.algor.arrowgen import ArrowGen
from molbiox.frame import interactive, streaming
from molbiox.frame.environ import from_default
from molbiox.io import tabular
from molbiox.visual import svg_maker


@interactive.castable
def rescale_tab_vizorf(records, scale, normalize=True):
    """
    Cannot handle very large file
    :param records: an iterable of TabRecord objects
    :param normalize: boolean. If true, shift to make leftmost point 0
    :param scale: a number. All head and tail values will be divided by this num
    :return:
    """
    if normalize:
        records = records if isinstance(records, list) else list(records)
        minpos = min(r.head for r in records)
    else:
        minpos = 0.

    for rec in records:
        # element = get_defaults(polygon_style=dict(fill=rec['color']))
        # print(element, file=sys.stderr)
        head = rec.head
        tail = rec.tail
        if rec.strand < 0:
            rec.head = (tail - minpos) * 1. / scale
            rec.tail = (head - minpos) * 1. / scale
        else:
            rec.head = (head - minpos) * 1. / scale
            rec.tail = (tail - minpos) * 1. / scale
        yield rec


class TextMaker(object):
    def __init__(self, ypos, angle=0, style=None):
        self.angle = angle
        self.style = style
        self.ypos = ypos

    def __call__(self, record):
        c = record.label
        x = record.head * .6 + record.tail * .4
        y = self.ypos
        a = self.angle
        s = self.style
        return svg_maker.make_text(c, x=x, y=y, rx=x, ry=y, angle=a, style=s)


def new_ag_params(ag_params):
    default = {
        'alpha': .7,
        'beta': 1.,
        'height1': 16,
        'height2': 32,
    }
    return from_default(default, ag_params)


def render_vizorf(records, scale, normalize=True, ag_params=None, style=None):
    records = rescale_tab_vizorf(records, scale, normalize)
    records = list(records)

    ag_params = new_ag_params(ag_params)

    height = ag_params['height2'] * 8
    ypos_tx = ag_params['height2'] * 5
    ypos_pg = ag_params['height2'] * 7

    arrowgen = ArrowGen(**ag_params)
    array_pg = arrowgen([r.head, r.tail, ypos_pg] for r in records)

    textmaker = TextMaker(ypos_tx, angle=-60, style=style)
    elements = []
    for r, points in zip(records, array_pg):
        text = textmaker(r)
        pstyle = dict(fill=r.color)
        polygon = svg_maker.make_polygon(points, pstyle)
        elements.extend([text, polygon])

    width = max(r.tail for r in records)
    return svg_maker.render_svg(elements=elements, height=height, width=width)


def _d_format_points(data):
    """
    deprecated for reference only
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

