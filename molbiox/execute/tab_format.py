#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import sys
from molbiox.frame.command import Command
from molbiox.io.tabular import tab_format


class CmdTabFormat(Command):
    abbr = 'tabx'
    name = 'tab-format'
    desc = 'format tab/space delimited tables for viewing'

    @classmethod
    def register(cls, subparser):
        # a dummy register for expansiion
        subparser = super(cls, cls).register(subparser)
        subparser.add_argument(
            '-a', '--align', metavar='direction', default='L',
            help='path of the list file')
        return subparser

    @staticmethod
    def _align_symbol_convert(symb):
        text_align = {
            'l': '<',
            'r': '>',
            'c': '^',
            'left': '<',
            'right': '>',
            'center': '^',
            'centre': '^',
        }
        try:
            symb = symb.lower()
            return text_align[symb]
        except:
            sys.exit('unrecognized align symbol')

    @classmethod
    def render(cls, args, outfile):
        align = cls._align_symbol_convert(args.align)
        for filename in args.filenames:
            for x in tab_format(filename, ' ', align=align):
                print(x, file=outfile)
