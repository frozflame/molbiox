#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import os
import sys
import re
import itertools
import collections
from molbiox.frame.command import Command
from molbiox.io import fasta


# TODO: this command has a drawback: store everything inside memory

class CommandSel(Command):
    abbr = 'sl'
    name = 'select'
    desc = 'select sequences based on a list file'

    @classmethod
    def register(cls, subparser):
        # a dummy register for expansiion
        subparser = super(cls, cls).register(subparser)
        subparser.add_argument(
            # note: nargs=1 shoud NOT be here
            '-l', '--listfile', metavar='filename', required=True,
            help='path of the list file')
        subparser.add_argument(
            # note: nargs=1 shoud NOT be here
            '--order', action='store_true',
            help='preserve the order of sequence in list file')
        # TODO: is it posible to test existence via argparse?
        return subparser

    @staticmethod
    def render(args, outfile):
        def parse_key(l):
            regex = re.compile(r'[^>\s\n]+')
            mat = regex.search(l)
            return mat and mat.group() or None

        recgens = [fasta.read(fn, False) for fn in args.filenames]
        records = itertools.chain(*recgens)

        if not args.order:
            keys = {parse_key(l) for l in open(args.listfile)}
            for rec in records:
                cmt = rec.cmt.split()[0]
                if cmt in keys:
                    outrec = dict(cmt=cmt, seq=rec.seq) if args.concise else rec

                    fasta.write(outfile, outrec)
            return  # simple and fast

        if args.order:  # ^ in case of accidental deletion of that return
            # preserve order of keys in list file
            keys = (parse_key(l) for l in open(args.listfile))
            selection = collections.OrderedDict((k, None) for k in keys if k)

            for rec in records:
                # use title.split()[0] to be tolerent to titles with description
                cmt = rec.cmt.split()[0]
                # this consumes a lot of memory
                if cmt in selection:
                    selection[cmt] = rec
            for cmt in selection:
                rec = selection[cmt]
                outrec = dict(cmt=cmt, seq=rec.seq) if args.concise else rec
                fasta.write(outfile, outrec)
