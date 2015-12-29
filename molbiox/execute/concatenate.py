#!/usr/bin/env python3
# coding: utf-8
from __future__ import unicode_literals, print_function
import sys
import re
from molbiox.io import fasta
from molbiox.frame.command import Command
from molbiox.frame.regexon import Regexon


class CommandCat(Command):
    abbr = 'cat'
    name = 'concatenate'
    desc = 'concatenate fasta files'

    # TODO: symbols in regex:
    # $$ -> filename firstpart
    # $$[:-1] -> filename firstpart
    # $$[:] -> filename all
    # $$[1:2] -> filename second part

    @classmethod
    def filter_velvet_concise(cls, recs):
        reg = re.compile(r'^NODE_(\d+)_length')
        for rec in recs:
            mat = reg.match(rec.cmt)
            rec.cmt = 'node_' + mat.groups()[0].zfill(5)
            yield rec

    @classmethod
    def filter_insert_filename(cls, recs, filename, position):
        name = filename.split('.')[0]
        regs = {
            'head': r's/^([^\s]+)/{}.\1/'.format(name),
            'tail': r's/^([^\s]+)/\1.{}/'.format(name),
        }
        regexon = Regexon.perl(regs[position])
        return cls.filter_regex(recs, regexon)

    @classmethod
    def filter_regex(cls, recs, regexon):
        if regexon.xtype == 0:
            for rec in recs:
                rec.cmt = regexon.sub(rec.cmt)
                yield rec
        else:
            for rec in recs:
                if regexon.match(rec.cmt):
                    yield rec

    @classmethod
    def register(cls, subparser):
        # a dummy register for expansiion
        subparser = super(cls, cls).register(subparser)
        subparser.add_argument(
            '-f', '--insert-filename', metavar='position', choices=['head', 'tail'],
            help='add filefile in the cmt field of output')

        subparser.add_argument(
            '-w', '--width', type=int, default=60,
            help='line width of the seq')

        subparser.add_argument(
            '-x', '--regex', metavar='string',
            help="apply regex on cmt: 'm/reg/, 'x/reg/', 's/reg/repl/'")

        subparser.add_argument(
            '--velvet', action='store_true',
            help='simplify velvet cmt NODE_xx_length_xx_cov.. to node_000xx')
        return subparser

    @classmethod
    def render(cls, args, outfile):
        if args.regex and args.regex[0] not in 'exs':
            msg = """
            possible regex forms:
            1. 'm/pattern/modifiers'    - select matching ones
            2. 'x/pattern/modifiers'    - select non-matching ones
            3. 's/pattern/repl/modifiers'   - apply replacement on cmt
            """
            print(msg, file=sys.stderr)
            sys.exit('error: invalid regex')

        for fn in args.filenames:
            recs = fasta.read(fn, args.concise)
            if args.velvet:
                recs = cls.filter_velvet_concise(recs)
            if args.insert_filename:
                ifn = args.insert_filename
                recs = cls.filter_insert_filename(recs, fn, ifn)

            if args.regex:
                try:
                    regexon = Regexon.perl(args.regex)
                except ValueError as e:
                    sys.exit(e)
                recs = cls.filter_regex(recs, regexon)

            fasta.write(outfile, recs, linewidth=args.width)


class CommandNNJoin(Command):
    abbr = 'nnj'
    name = 'nn-join'
    desc = 'join sequences with Ns'
    __trackable__ = False


class CommandNNSplit(Command):
    abbr = 'nns'
    name = 'nn-split'
    desc = 'split sequences where N appears'
    __trackable__ = False


