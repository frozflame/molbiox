#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import sys
import itertools

from molbiox.frame.command import Command
from molbiox.io import fasta, primer


class CmdPrimer3Pre(Command):
    abbr = 'pr3a'
    name = 'primer3-prepare'

    @classmethod
    def render(cls, args, outfile):
        recgens = [fasta.read(fn) for fn in args.filenames]
        records = itertools.chain(*recgens)
        for r in records:
            text = primer.render_primer3_input(rec=r)
            if not text.endswith('\n'):
                text += '\n'
            outfile.write(text)


class CmdPrimer3Post(Command):
    abbr = 'pr3b'
    name = 'primer3-format'

    @classmethod
    def register(cls, subparser):
        super(cls, cls).register(subparser)
        subparser.add_argument(
            '--header', action='store_true',
            help='add a header in the output')
        return subparser

    @classmethod
    def render(cls, args, outfile):
        recgens = [primer.read_boulder(fn) for fn in args.filenames]
        records = itertools.chain(*recgens)
        if args.header:
            records = itertools.chain([primer.table_header], records)
        lines = primer.format_table(records)
        for l in lines:
            print(l, file=outfile)


class CmdPrimer3Cook(Command):
    abbr = 'pr3c'
    name = 'primer3-cook'

    text = """
    $ mbx pr3a genes.fa | primer3_core > genes.pr3out
    $ mbx pr3b genes.pr3out > genes.primers.txt
    """

    @classmethod
    def register(cls, subparser):
        return subparser

    @classmethod
    def run(cls, args):
        print(cls.text)


