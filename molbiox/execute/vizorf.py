#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function

from molbiox.frame.command import Command
from molbiox.visual.vizorf import render_vizorf


class CmdVizORF(Command):
    abbr = 'vo'
    name = 'visualize-orf'
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
        ag_params = {
            'alpha': args.alpha,
            'beta': args.beta,
            'height1': args.h1,
            'height2': args.h2,
        }
        for filename in args.filenames:
            res = render_vizorf(
                filename, scale=args.scale, normalize=True, ag_params=ag_params)
            outfile.write(res)
