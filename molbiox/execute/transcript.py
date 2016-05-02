#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
from molbiox.frame.command import Command
from molbiox.algor.transcode import CharsMapper
from molbiox.io import fasta


class CmdRevcompl(Command):
    abbr = 'rc'
    name = 'revcompl'
    desc = 'generate reverse complements for given sequences'

    @classmethod
    def render(cls, args, outfile):
        cmapper = CharsMapper.new_mapper_revcompl_dna()
        for fn in args.filenames:
            for rec in fasta.read(fn):
                rec.cmt += '.RC'
                rec.seq = cmapper.transcode(rec.seq)
                fasta.write(outfile, rec)
