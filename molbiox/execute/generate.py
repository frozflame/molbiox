#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import os
import sys
import stat
from molbiox.frame.command import Command
from molbiox.frame.locate import locate_template


class CommandGen(Command):
    abbr = 'gen'
    name = 'generate'
    desc = 'generate scripts'

    @classmethod
    def register(cls, subparser):
        subparser.add_argument(
            '--rude', action='store_true',
            help='overwriting existing files if needed')

        subparser.add_argument(
            'template', default='test',
            help='name of template to start from')

        subparser.add_argument(
            'out', nargs='?',
            help='path to the output file, otherwise stdout')

    @classmethod
    def run(cls, args):
        tpl_path = locate_template(args.template, new=False)
        tpl = open(tpl_path).read()

        # TODO: render from a template
        output = tpl

        if args.out == '-':
            sys.stdout.write(tpl)
        else:
            filename = args.out or locate_template(args.template, new=True)
            cls.check_overwrite(args, filename)

            with open(filename, 'w') as outfile:
                outfile.write(output)

            # chmod +x
            st = os.stat(filename)
            os.chmod(filename, st.st_mode | stat.S_IEXEC)
