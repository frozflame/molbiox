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
        if rec.strand == '-':
            rec.head = (tail - minpos) * 1. / scale
            rec.tail = (head - minpos) * 1. / scale
        else:
            rec.head = (head - minpos) * 1. / scale
            rec.tail = (tail - minpos) * 1. / scale
        yield rec


class TextMaker(object):
    def __init__(self, height, angle=0, style=None):
        self.angle = angle
        self.style = style
        self.height = height

    def __call__(self, record):
        c = record.label
        x = (record.head + record.tail) / 2.
        y = self.height
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


def render_vizorf(filename, scale, normalize, style, ag_params=None):
    records = tabular.read_tab_vizorf(filename, castfunc=list)
    records = rescale_tab_vizorf(records, scale, normalize)

    ag_params = new_ag_params(ag_params)
    ypos = ag_params['h2'] * 4
    arrpos = ([r.head, r.tail, ypos] for r in records)

    arrowgen = ArrowGen(**ag_params)
    arrpgs = arrowgen(arrpos)

    tm = TextMaker(ag_params['h2'], angle=-30, style=style)
    texts = [tm(r) for r in records]
    polygons = [svg_maker.make_polygon(a) for a in arrpgs]

    elements = streaming.alternate(texts, polygons)
    width = max(r.tail for r in records)
    height = ag_params['h2'] * 5
    return svg_maker.render_svg(elements=elements, height=height, width=width)
