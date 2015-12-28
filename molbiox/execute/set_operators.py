#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import sys
from molbiox.frame.command import Command


class CommandSetOp(Command):
    # not a command
    __trackable__ = False

    @classmethod
    def register(cls, subparser):
        # a dummy register for expansiion
        subparser = super(CommandSetOp, cls).register(subparser)
        return subparser

    @staticmethod
    def parse_input(filename, sep=None):
        """ Parse a text file as a set """
        # TODO: implement sep
        return set(l.strip() for l in open(filename))

    @classmethod
    def render(cls, args, outfile):
        """
        :param outfile:
        :param rset: a set object
        :return:
        """
        sets = (cls.parse_input(fn) for fn in args.filenames)
        operator = cls.__dict__.get('__operatoR__', None)
        rset = cls.calculate(operator, sets)
        for item in rset:
            outfile.write(str(item))
            outfile.write('\n')

    @staticmethod
    def calculate(op, sets):
        """
        :param op: operator, one of ('minus', 'union', 'intersect')
        :param sets: an iterable of sets
        :return: a set object
        """
        sets = iter(sets)
        # get the first set
        try:
            result = next(sets)
        except StopIteration:
            return set()

        for set_ in sets:
            if op == '-':
                result -= set_
            elif op == 'u':
                result |= set_
            elif op == 'n':
                result &= set_
            else:
                raise ValueError('op not supported: {}'.format(op))
        return result

    @classmethod
    def run(cls, args):
        if args.out:
            cls.check_overwrite(args)
            with open(args.out, 'w') as outfile:
                cls.render(args, outfile)
        else:
            cls.render(args, sys.stdout)


class CommandSetMinus(CommandSetOp):
    abbr = 'set-'
    name = 'set-minus'
    desc = 'calculate set operation set1 - set2 - ...'
    __operatoR__ = '-'


class CommandSetUnion(CommandSetOp):
    abbr = 'setu'
    name = 'set-union'
    desc = 'calculate set operation set1 U set2 U ...'
    __operatoR__ = 'u'


class CommandSetIntersect(CommandSetOp):
    abbr = 'setn'
    name = 'set-intersect'
    desc = 'calculate set operation set1 n set2 n ...'
    __operatoR__ = 'n'
