#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import os
import sys
from molbiox.frame.command import Command


directories = [
    'rawdata',
    'test',
    'tmp',
]

files = [
    'readme.md',
]


class CommandDir(Command):
    abbr = 'mkdir'
    name = 'make-project-dir'
    desc = 'create a mbx standard direcitory structure'

    @classmethod
    def register(cls, subparser):
        subparser.add_argument(
            '--rude', action='store_true',
            help='overwriting existing files if needed')

        subparser.add_argument(
            '--test', action='store_true',
            help='include a test dir')

        subparser.add_argument(
            'name', metavar='name',
            help='name of project')

        return subparser

    @classmethod
    def run(cls, args):
        cls.check_overwrite(args, args.name)
        os.mkdir(args.name)
        for dir_ in directories:
            dir_ = os.path.join(args.name, dir_)
            os.makedirs(dir_, exist_ok=True)
        for fn in files:
            fn = os.path.join(args.name, fn)
            open(fn, 'a').close()

    @classmethod
    def render(cls, args, outfile):
        raise NotImplementedError

