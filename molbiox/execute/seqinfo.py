#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function

import sys
from molbiox.algor import statis
from molbiox.io import fasta
from molbiox.frame.command import Command


class CommandInf(Command):
    __trackable__ = False

    @classmethod
    def register(cls, subparser):
        subparser = super(CommandInf, cls).register(subparser)
        subparser.add_argument(
            '--header', action='store_true',
            help='output headers showing filenames')
        subparser.add_argument(
            '--mode', choices=['normal', 'brief'], default='normal',
            help='mode ...')
        return subparser

    @classmethod
    def render(cls, args, outfile):
        for filename in args.filenames:
            if args.header:
                line = '# file: {}\n'.format(filename)
                outfile.write(line)
            cls.process(args, outfile, filename)


class InfLen(CommandInf):
    abbr = 'l'
    name = 'length'
    desc = 'get lengths of each sequence'

    @classmethod
    def process(cls, args, outfile, filename):
        seqrecords = fasta.read(filename)
        for rec in seqrecords:
            line = '{}\t{}\n'.format(len(rec.seq), rec.cmt)
            outfile.write(line)


class InfCount(CommandInf):
    abbr = 'c'
    name = 'count'
    desc = 'count number of sequences'

    # TODO: this one not right
    @classmethod
    def process(cls, args, outfile, filename):
        seqrecords = fasta.read(filename)
        for rec in seqrecords:
            line = '{}\t{}\n'.format(len(rec.seq), rec.cmt)
            outfile.write(line)


class InfGC(CommandInf):
    abbr = 'gc'
    name = 'gc-content'
    desc = 'calculate gc ratios'

    @classmethod
    def process(cls, args, outfile, filename):
        seqrecords = fasta.read(filename)
        for rec in seqrecords:
            gc = statis.calc_gc_content(rec['seq'])
            if args.percent:
                gc *= 100
            line = '{0:.{1}f}\t{2}\n'.format(gc, args.precision, rec['cmt'])
            outfile.write(line)

    @classmethod
    def register(cls, subparser):
        subparser = super(InfGC, cls).register(subparser)
        subparser.add_argument(
            '--precision', default=2, type=int,
            help='decimal precision (number of digits after decimal point)')
        subparser.add_argument(
            '--percent', action='store_true',
            help='as percentage (100 for GCCGGG intead of 1)')
        return subparser

