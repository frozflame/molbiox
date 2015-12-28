#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function

import importlib
import os
import re
import sys
import six
from collections import defaultdict
import molbiox.execute
import argparse
import signal


class Tracked(type):
    """Track subclasses"""
    def __init__(cls, name, bases, dic):
        # look only the class itself for __trackable__
        # cls.__dict__['__trackable__'] == False: cls is not exposed as a command
        if not cls.__dict__.get('__trackable__', True):
            super(Tracked, cls).__init__(name, bases, dic)
            return

        # do NOT track base classes bearing a not-None __trackdict__
        errmsg = 'a Command subclass must have its own {}: {}'
        if 'name' not in cls.__dict__:
            raise NotImplementedError(errmsg.format('name', cls.__name__))
        if 'abbr' not in cls.__dict__:
            raise NotImplementedError(errmsg.format('abbr', cls.__name__))

        # __trackdict__ not in cls.__dict__: cls is not tracked base class
        if '__trackdict__' not in cls.__dict__:
            # traverse inheritance tree to find __trackdict__
            trackdict = getattr(cls, '__trackdict__', None)
            if trackdict is not None:
                if cls.abbr in trackdict['abbr']:
                    raise ValueError('duplicating command abbr: {}'.format(cls.abbr))
                if cls.name in trackdict['abbr']:
                    raise ValueError('duplicating command name: {}'.format(cls.name))
                trackdict['abbr'][cls.abbr] = cls
                trackdict['name'][cls.name] = cls
                # print('subclass found', cls)
        super(Tracked, cls).__init__(name, bases, dic)


@six.add_metaclass(Tracked)
class Command(object):
    # do NOT provide this in sub-classes
    __trackdict__ = defaultdict(dict)

    abbr = 'cmd'
    name = 'command'
    desc = 'a generic command'

    @classmethod
    def register(cls, subparser):
        """
        Most frequent style: generate 1 report file from multiple input files
        :param subparser: argparse.ArgumentParser(..).add_subparsers(..)
        :return: the same subparser with arguments added
        """
        subparser.add_argument(
            '--rude', action='store_true',
            help='overwriting existing files if needed')

        subparser.add_argument(
            '-o', '--out', metavar='filename',
            help='output filename')

        subparser.add_argument(
            '-v', '--verbose', action='store_true',
            help='level up verbosity')

        subparser.add_argument(
            'filenames', metavar='filename', nargs='*',
            help='input filenames; if empty, stdin is used')
        return subparser

    @classmethod
    def run(cls, args):
        """
        Entry point for executing this command
        :param args: parser.parse_args()
        :return: None
        """
        cls.check_existence(args)
        # if args has no attr filename, skip
        if getattr(args, 'filenames', 1):
            args.filenames = ['-']
        if args.out:
            cls.check_overwrite(args)
            with open(args.out, 'w') as outfile:
                cls.render(args, outfile)
                outfile.close()
        else:
            cls.render(args, sys.stdout)

    @classmethod
    def render(cls, args, outfile):
        pass

    @classmethod
    def check_overwrite(cls, args, filename=None):
        """
        Check if overwriting a file without `--rude`, print error and exit if so
        :param args: parser.parse_args()
        :param filename: if not None, check this file instead of `args.out`
        :return: None
        """
        if not filename and not hasattr(args, 'out'):
            return
        filename = filename or args.out
        if not args.rude and os.path.exists(filename):
            msg = 'error: "{}" exists already'.format(filename)
            sys.exit(msg)

    @classmethod
    def check_existence(cls, args, filenames=None):
        if not filenames and not hasattr(args, 'filenames'):
            return
        filenames = filenames or args.filenames
        for fn in filenames:
            if not os.path.exists(fn):
                msg = 'error: "{}" does not exist'.format(fn)
                sys.exit(msg)
            if not os.path.isfile(fn):
                msg = 'error: "{}" is not a file'.format(fn)
                sys.exit(msg)


class Executor(object):
    @staticmethod
    def load_commands():
        # subset of a valid module name
        regex = re.compile(r'^([a-z][_a-z0-9]*)\.py$')
        dirpath = os.path.dirname(molbiox.execute.__file__)
        for filename in os.listdir(dirpath):
            mat = regex.match(filename)
            if mat:
                modname = 'molbiox.execute.' + mat.groups()[0]
                importlib.import_module(modname)

    @staticmethod
    def parse_arguments():
        desc = 'Molbiox Project'
        parser = argparse.ArgumentParser(description=desc)
        subparsers = parser.add_subparsers(dest='subcmd', help='mbx <subcommand>')
        subparsers.add_parser('help')

        for cls in Command.__trackdict__['abbr'].values():
            subparser = subparsers.add_parser(cls.name, aliases=[cls.abbr], help=cls.desc)
            cls.register(subparser)
        return parser.parse_args()

    @staticmethod
    def register_signal_handers():
        def sigpipe_handler(signum, frame):
            sys.exit('@mbx: pipe broken ~')
        signal.signal(signal.SIGPIPE, sigpipe_handler)

        def sigint_handler(signum, frame):
            sys.exit('@mbx: user terminated ~')
        signal.signal(signal.SIGINT, sigint_handler)

    @classmethod
    def run(cls):
        cls.register_signal_handers()
        cls.load_commands()
        args = cls.parse_arguments()

        try:
            if args.subcmd in Command.__trackdict__['abbr']:
                Command.__trackdict__['abbr'][args.subcmd].run(args)
            elif args.subcmd in Command.__trackdict__['name']:
                Command.__trackdict__['name'][args.subcmd].run(args)
            else:
                print('@mbx: command not found', file=sys.stderr)
        except KeyboardInterrupt:
            print('@mbx: user terminated', file=sys.stderr)
        except BrokenPipeError:
            print('@mbx: pipe broken', file=sys.stderr)
