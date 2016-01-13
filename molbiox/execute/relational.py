#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import sys
import itertools
from molbiox.frame.command import Command
from molbiox.io import blast, tabular

"""
If your results come from more than 2 columns, use a SQL database instead.
"""

class CommandAggregate(Command):
    abbr = 'ag'
    name = 'aggregate'
    desc = 'apply an aggregation function to a tabular text file'

    @classmethod
    def register(cls, subparser):
        subparser = super(cls, cls).register(subparser)
        subparser.add_argument(
            '--subsep', metavar='character',
            help="seperator used on subject names")
        subparser.add_argument(
            '-f', '--function', metavar='string', default='count',
            choices=['count', 'list', 'set', 'avg', 'var', 'std'],
            help='name of the aggregation function')
        subparser.add_argument(
            '-k', '--key', metavar='integer', default=0,
            help='group by this column ')
        subparser.add_argument(
            '-v', '--val', metavar='integer', default=0,
            help='apply aggregation function on this column')
        subparser.add_argument(
            '--ksort', metavar='string', choices=['alpha', 'num'],
            help='sort keys alphabetically or numerically')
        subparser.add_argument(
            '--vsort', metavar='string', choices=['alpha', 'num'],
            help='sort values alphabetically or numerically')
        subparser.add_argument(
            '-m', '--limit', type=int,
            help='set max number of hits listed for each query')
        return subparser

    @classmethod
    def render(cls, args, outfile):
        recgens = [tabular.read(fn) for fn in args.filenames]
        records = itertools.chain(*recgens)
        aggregator = tabular.Aggregator(aggregator)

        if args.function == 'count':
            # groups = aggregator
            pass


    @classmethod
    def render_(cls, args, outfile):
        if args.format != '6m':
            sys.exit('currently only blast6mini')

        # TODO: decide what func to use based on -f option
        func = blast.read_fmt6m

        # a list of generators, then chain them
        recgens = [func(fn) for fn in args.filenames]
        records = itertools.chain(*recgens)
        querydic = blast.aggregate(records, subsep=args.subsep)

        if args.sort:
            pairs = ((k, querydic[k]) for k in sorted(querydic))
        else:
            pairs = ((k, querydic[k]) for k in querydic)

        if args.list:
            for k, v in pairs:
                v = sorted(v) if args.sort else v
                v = itertools.islice(v, args.limit) if args.limit else v
                subj = ' '.join(v)
                print(k, subj, sep='\t', file=outfile)
        else:
            for k, v in querydic.items():
                print(len(v), k, sep='\t', file=outfile)

    @classmethod
    def get_agg_func(cls, name):
        """
        Get a function which returns a dict-like object
        :param name:
        :return:
        """
        pass


