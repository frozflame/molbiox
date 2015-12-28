#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import sys
import sys
import itertools
from molbiox.frame.command import Command
from molbiox.io import fasta, blast


class CommandHitAggregate(Command):
    abbr = 'ha'
    name = 'hit-aggregate'
    desc = 'aggregate database search results'

    @classmethod
    def register(cls, subparser):
        # a dummy register for expansiion
        subparser = super(CommandHitAggregate, cls).register(subparser)
        subparser.add_argument(
            # note: nargs=1 shoud NOT be here
            '--subsep', metavar='character',
            help="seperator used on subject names")
        subparser.add_argument(
            # note: nargs=1 shoud NOT be here
            '-f', '--format', metavar='string', default='6m',
            help='currently only blast6mini')
        subparser.add_argument(
            '-l', '--list', action='store_true',
            help='list subject names instead of count')
        subparser.add_argument(
            '-s', '--sort', action='store_true',
            help='sort output alphabetically')
        subparser.add_argument(
            '-m', '--limit', type=int,
            help='set max number of hits listed for each query')
        return subparser

    @classmethod
    def render(cls, args, outfile):
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
