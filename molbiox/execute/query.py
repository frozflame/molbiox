#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import sys
from molbiox.frame.command import Command


class CmdQuery(Command):
    abbr = 'q'
    name = 'query'
    desc = 'query about configurations and standards'

    @classmethod
    def register(cls, subparser):
        subparser.add_argument(
            'subject', help='what do you want to ask')
        return subparser

    @classmethod
    def run(cls, args):
        query = args.subject
        func = getattr(cls, 'q_' + query, None)
        if func is None:
            sys.exit('error: invalid query "{}"'.format(query))
        return func()

    @classmethod
    def q_nproc(cls):
        import multiprocessing
        nproc = multiprocessing.cpu_count()
        print(nproc)

    @classmethod
    def _blasttab(cls, name):
        from molbiox.kb import blast
        fieldlist = getattr(blast, name, None)
        return blast.make_ncbi_spec(fieldlist)

    @classmethod
    def q_blast6m(cls):
        print('6 ' + cls._blasttab('fmtmini'))

    @classmethod
    def q_blast6a(cls):
        print('6 ' + cls._blasttab('fmtall'))

    @classmethod
    def q_blast7m(cls):
        print('7 ' + cls._blasttab('fmtmini'))

    @classmethod
    def q_blast7a(cls):
        print('7 ' + cls._blasttab('fmtall'))

    @classmethod
    def q_blast10m(cls):
        print('10 ' + cls._blasttab('fmtmini'))

    @classmethod
    def q_blast10a(cls):
        print('10 ' + cls._blasttab('fmtall'))
