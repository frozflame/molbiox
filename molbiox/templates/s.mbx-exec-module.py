#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import os
import sys
from molbiox.frame.command import Command


class CommandTerrible(Command):
    abbr = 'tr'
    name = 'terrible'
    desc = 'a terrible command'

    @classmethod
    def register(cls, subparser):
        subparser = super(CommandTerrible, cls).register(subparser)

        subparser.add_argument(
            '--stupid', action='store_true',
            help='run in stupid mode')
        return subparser

    @classmethod
    def run(cls, args):
        raise NotImplementedError

    @classmethod
    def render(cls, args, outfile):
        raise NotImplementedError

