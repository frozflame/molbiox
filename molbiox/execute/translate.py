#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import sys
from molbiox.algor.translate import CodonTable
from molbiox.frame.command import Command
from molbiox.io import fasta
from molbiox.kb import translate


class CommandTranslate(Command):
    abbr = 'tl'
    name = 'translate'
    desc = 'translate DNA sequences into protein sequences'

    @classmethod
    def register(cls, subparser):
        subparser = super(CommandTranslate, cls).register(subparser)

        subparser.add_argument(
            '-t', '--table', type=int, default=1, metavar='integer',
            help='ncbi transl_table code')
        subparser.add_argument(
            '-s', '--skip', action='store_true',
            help='skip invalid sequneces whose lenths are not multiples of 3')

        return subparser

    @classmethod
    def render(cls, args, outfile):
        dic = translate.get_transl_table(args.table)
        tab = CodonTable(dic)
        for fn in args.filenames:
            for rec in fasta.read(fn, args.concise):
                if len(rec.seq) % 3:
                    if not args.quiet:
                        msg = 'warning: lenth of seq not a multiple of 3\n'
                        msg += '^debug:\t{}\t{}\t{}'.format(len(rec.seq), fn, rec.cmt)
                        print(msg, file=sys.stderr)
                    if args.skip:
                        continue
                    l = len(rec.seq)
                    rec.seq = rec.seq[:int(l - l % 3)]
                rec.seq = tab.translate(rec.seq)
                fasta.write(outfile, rec)
