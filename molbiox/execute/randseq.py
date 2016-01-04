#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import sys
import six
from numpy.random import binomial
from molbiox.algor.mutate import MutSimulator
from molbiox.frame.command import Command
from molbiox.io import fasta


class CommandRandseq(Command):
    # TODO: add length variation
    abbr = 'rs'
    name = 'random-seq'
    desc = 'generate random sequences'

    @classmethod
    def register(cls, subparser):
        """
        :param subparser: argparse.ArgumentParser(..).add_subparsers(..)
        :return: None
        """
        subparser.add_argument(
            '--rude', action='store_true',
            help='overwriting existing files if needed')

        subparser.add_argument(
            '-o', '--out', metavar='output-file',
            help='output filenam')

        subparser.add_argument(
            '-n', '--num', metavar='integer', type=int, default=1,
            help='number of sequences in the generated file')

        subparser.add_argument(
            '-l', '--len', metavar='integer', type=int, default=1000,
            help='length of each sequence in the generated file')

        subparser.add_argument(
            '--sigma', metavar='float', type=float, default=0,
            help='standard deviation of a binomial distribution')

        return subparser

    @classmethod
    def render(cls, args, outfile):
        if args.sigma:
            p = 1 - args.sigma ** 2. / args.len
            if p < 0:
                errmsg = 'sigma should be smaller then sqrt(len)'
                sys.exit(errmsg)
            lengths = (binomial(args.len, p) for _ in six.moves.range(args.num))
        else:
            lengths = (args.len for _ in six.moves.range(args.num))
        for i, l in enumerate(lengths):
            cmt = 'randseq.{}'.format(i)
            seq = MutSimulator.gen_randseq(l).decode('ascii')
            fasta.write(outfile, dict(cmt=cmt, seq=seq))

