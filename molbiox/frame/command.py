#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import os
import sys
import six
from collections import defaultdict


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
        if not args.filenames:
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
        filename = filename or args.out
        if not args.rude and os.path.exists(filename):
            msg = 'error: "{}" exists already'.format(filename)
            sys.exit(msg)

    @classmethod
    def check_existence(cls, args, filenames=None):
        filenames = filenames or args.filenames
        for fn in filenames:
            if not os.path.exists(fn):
                msg = 'error: "{}" does not exist'.format(fn)
                sys.exit(msg)
            if not os.path.isfile(fn):
                msg = 'error: "{}" is not a file'.format(fn)
                sys.exit(msg)

