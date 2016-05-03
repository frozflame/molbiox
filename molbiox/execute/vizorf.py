#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function

import sys

import dataset

from molbiox.frame.containers import TabRecord
from molbiox.frame.command import Command
from molbiox.io import tabular
from molbiox.visual.vizorf import render_vizorf


class CmdVizORF(Command):
    abbr = 'vo'
    name = 'visualize-orf'
    desc = 'plot ORFs with arrows; experimental'

    @classmethod
    def register(cls, subparser):
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
        subparser.add_argument(
            '--rude', action='store_true',
            help='overwriting existing files if needed')
        subparser.add_argument(
            '-o', '--out', metavar='filename',
            help='output filename')
        subparser.add_argument(
            '-e', '--engine-url', help='database url')
        subparser.add_argument(
            'table', help='input filename, or table if engine-url provided')
        return subparser

    @classmethod
    def render(cls, args, outfile):
        ag_params = {
            'alpha': args.alpha,
            'beta': args.beta,
            'height1': args.h1,
            'height2': args.h2,
        }
        if args.engine_url:
            db = dataset.connect(args.engine_url)
            records = [TabRecord(r) for r in db[args.table]]
            records = tabular.prepare_vizorftab(records)
        else:
            records = tabular.read_vizorftab(args.table)
        res = render_vizorf(records, scale=args.scale, normalize=True, ag_params=ag_params)
        outfile.write(res)

    @classmethod
    def run(cls, args):
        """
        Entry point for executing this command
        :param args: parser.parse_args()
        :return: None
        """
        cls.check_overwrite(args)
        if args.engine_url is None:
            cls.check_existence(args, [args.table])
            if not args.table:
                args.table = '-'
        if args.out:
            with open(args.out, 'w') as outfile:
                cls.render(args, outfile)
                outfile.close()
        else:
            cls.render(args, sys.stdout)
