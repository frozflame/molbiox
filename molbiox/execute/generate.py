#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import os
import sys
import stat
import re
from molbiox.frame.command import Command
from molbiox.frame.environ import locate_template
from molbiox.frame import environ
from molbiox.settings import all_templates


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
        return subparser

    @classmethod
    def run(cls, args):
        args.template = all_templates.get(args.template, args.template)
        default_filename = re.sub(r'^s\.', 'run-', args.template)

        if args.out == '-':
            cls.render(args, sys.stdout)
        else:
            filename = args.out or default_filename
            cls.check_overwrite(args, [filename])
            with open(filename, 'w') as outfile:
                cls.render(args, outfile)
            # chmod +x
            st = os.stat(filename)
            os.chmod(filename, st.st_mode | stat.S_IEXEC)

    @classmethod
    def render(cls, args, outfile):
        template = environ.get_template(args.template)
        outfile.write(template.render())

