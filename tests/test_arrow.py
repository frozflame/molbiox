#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import sys
from math import sqrt
import numpy as np

import molbiox
from molbiox.io import arrows
from molbiox.algor.arrows import ArrowCalc
from molbiox.frame.locate import locate_tests

pi = np.pi

dataset1 = {
    'config': dict(alpha=pi / 4, beta=pi / 2, height1=1, height2=2),
    'lengths': [4],
    'results': np.array([[
        [0,  0], [2,  2], [2,  1], [4,  1],
        [4, -1], [2, -1], [2, -2], [0,  0]
    ]])
}

dataset2 = {
    'config': dict(alpha=pi / 4, beta=pi / 3, height1=1, height2=2),
    'lengths': [2 - sqrt(3)/2],
    'results': np.array([[
        [0,  0], [2,  2],
        [2 - sqrt(3)/2,  1./2], [2-sqrt(3)/2,  1./2],
        [2 - sqrt(3)/2, -1./2], [2-sqrt(3)/2, -1./2],
        [2, -2], [0, 0]
    ]])
}

dataset3 = {
    'config': dict(alpha=pi / 4, beta=pi / 3, height1=1, height2=2),
    'lengths': [.6],
    'results': np.array([[
        [0,  0], [2,  2], [.6, 0], [.6, 0],
        [.6, 0], [.6, 0], [2, -2], [0,  0]
    ]])
}


def arr_eq(arr1, arr2, precision=.001):
    return np.abs(arr1 - arr2).reshape(-1).max() < precision


def test_read_lwcfile():
    path = 'data/sample_lwcfile.txt'
    table = arrows.read_lwcfile(path, castfunc=list)
    for x in table:
        print(x)


def test_arrow_calc():
    for ds in [dataset1, dataset2, dataset3]:
        ac = ArrowCalc(**ds['config'])
        # result = calc.prototype(400).astype(np.int)
        results = ac.calc(ds['lengths'])
        assert arr_eq(results, ds['results'], .001)
        resultp = ac.prototype(ds['lengths'][0])
        assert arr_eq(resultp, ds['results'][0], .001)
        # assert 1 == 2

        for l in np.arange(10, step=.01):
            resultp = ac.prototype(l)
            results = ac.calc([l])
            assert arr_eq(results[0], resultp, .001)
            assert arr_eq(results[:, 0, :], 0, .001)
            assert arr_eq(results[:, 7, :], 0, .001)
            assert arr_eq(results[:, 1, 1], ds['config']['height2'], .001)
            assert arr_eq(results[:, 2, 1], results[:, 3, 1])
            assert arr_eq(results[:, 2, 1], -results[:, 4, 1])
            assert arr_eq(results[:, 2, 1], -results[:, 5, 1])
            assert arr_eq(results[:, 6, 1], -ds['config']['height2'])


def _test_arrow_factory():
    path = 'data/sample_lwcfile.txt'
    tab = arrows.read_lwcfile(path, castfunc=list)
    arrfactory = ArrowCalc()
    data = arrfactory.calc(arr)


def test_plot():
    ac = ArrowCalc(**dataset1['config'])
    data = ac.calc([[6, 9, 0], [9, 6, 9]]) * 20
    elements = [dict(polygon=pts) for pts in arrows.format_points(data)]
    print(data, file=sys.stderr)
    print(elements, file=sys.stderr)

    kwargs = arrows.get_defaults()
    kwargs['elements'] = elements
    res = arrows.render_svg(**kwargs)
    print(res)


def test():
    path = locate_tests('data/lwcsample.tsv')
    elements = molbiox.io.arrows.read_lwcfile(path, castfunc=list)

    arr = ([elem['head'], elem['tail'], 1000] for elem in elements)
    results = ArrowCalc().calc(arr) / 20

    polygons = arrows.format_points(results)

    for elem, pg in zip(elements, polygons):
        elem['polygon'] = pg
        elem['text_x'] = (elem['head'] + elem['tail']) / 2. / 20
        elem['text_y'] = 920 / 20
        print(elem, file=sys.stderr)

    res = arrows.render_svg(elements=elements)
    print(res)


if __name__ == '__main__':
    # test_read_lwcfile()
    # test_arrow_calc()
    test()