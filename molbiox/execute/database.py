#!/usr/bin/env python3
# coding: utf-8

from __future__ import division, unicode_literals, print_function

import datetime

from molbiox.io import tabular
from molbiox.frame.command import Command


class CmdDBPersist(Command):
    abbr = 'per'
    name = 'persist'
    desc = 'persist to a SQL database'

    @classmethod
    def register(cls, subparser):
        super(cls, cls).register(subparser)
        subparser.add_argument(
            '-e', '--engine-url', help='database url')
        subparser.add_argument(
            '-t', '--tblname', help='table name')
        return subparser

    @staticmethod
    def _tblname():
        now = datetime.datetime.now()
        return now.strftime('t_%m%d_%H%M%S')

    @classmethod
    def render(cls, args, outfile):
        tblname = args.tblname or cls._tblname()
        url = args.engine_url or 'postgresql://localhost/vibrio'
        structure = tabular.DummyStructure('c', [int, float])
        for fn in args.filenames:
            records = tabular.read(fn, structure)
            tabular.persist(url, tblname, records)
        print(tblname)

