#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function

from molbiox.algor.arrowgen import ArrowGen
from molbiox.frame.command import Command
from molbiox.io import tabular
from molbiox.visual import arrow


class CmdORFVisualize(Command):
    abbr = 'ov'
    name = 'orf-visualize'
    desc = 'plot ORFs with arrows; experimental'

    @classmethod
    def register(cls, subparser):
        super(cls, cls).register(subparser)
        subparser.add_argument(
            '-s', '--scale', metavar='number', type=int, default=16,
            help='scale factor; the larger this number, the shorter your arrows')
        subparser.add_argument(
            '--alpha', metavar='number', type=float, default=.8,
            help='alpha angle in radian')
        subparser.add_argument(
            '--beta', metavar='number', type=float, default=1.,
            help='beta angle in radian')
        subparser.add_argument(
            '--h1', metavar='number', type=float, default=5,
            help='height of the horizontal bar')
        subparser.add_argument(
            '--h2', metavar='number', type=float, default=8,
            help='height of the arrow')
        return subparser

    @classmethod
    def render(cls, args, outfile):
        calc = ArrowGen(args.alpha, args.beta, args.h1, args.h2)
        for filename in args.filenames:
            elements = tabular.read_lwctab(filename, args.scale, castfunc=list)
            # print('debug: elements', elements, file=sys.stderr)
            ypos = args.h2 * 4
            maxpos = max(max(elem['head'], elem['tail']) for elem in elements)
            arrpos = ([elem['head'], elem['tail'], ypos] for elem in elements)
            results = calc(arrpos)
            polygons = arrow.format_points(results)

            for elem, pg in zip(elements, polygons):
                elem['polygon'] = pg
                elem['text_x'] = (elem['head'] + elem['tail']) / 2.
                elem['text_y'] = args.h2 * 3
            res = arrow.render_svg(elements=elements, height=args.h2*5, width=maxpos)
            outfile.write(res)
