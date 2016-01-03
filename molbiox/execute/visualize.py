#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import sys
from molbiox.algor.arrows import ArrowCalc
from molbiox.frame.command import Command
from molbiox.frame.locate import locate_tests
from molbiox.io import arrows


class CommandArrowplot(Command):
    abbr = 'ap'
    name = 'arrow-plot'
    desc = 'plot genes with arrows'

    @classmethod
    def render(cls, args, outfile):
        path = locate_tests('data/lwcsample.tsv')
        elements = arrows.read_lwcfile(path, castfunc=list)

        arr = ([elem['head'], elem['tail'], 1000] for elem in elements)
        results = ArrowCalc().calc(arr) / 20

        polygons = arrows.format_points(results)

        for elem, pg in zip(elements, polygons):
            elem['polygon'] = pg
            elem['text_x'] = (elem['head'] + elem['tail']) / 2. / 20
            elem['text_y'] = 920 / 20
            print(elem, file=sys.stderr)
        res = arrows.render_svg(elements=elements)
        outfile.write(res)

