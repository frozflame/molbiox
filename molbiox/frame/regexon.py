#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import re
import six
from string import whitespace


class Regexon(object):
    """
    Commonly used regular expressions with syntax sugar
    """

    def __init__(self, recompiled, repl=None):
        if not isinstance(repl, six.string_types) and repl is not None:
            raise TypeError("'repl' should be a string or None")

        if repl is None:
            self.xtype = 1
            repl = ''
        else:
            self.xtype = 0

        # recompiled: re compile() -ed
        self.recompiled = recompiled
        self.repl = repl

    def __ror__(self, other):
        """
        Use pipe operator
        :param other:
        :return:
        """
        return self.sub(other)

    def __contains__(self, s):
        """
        Test matching with 'in' operator. A regex is a set of strings.
        :param s: a string
        :return: True or False
        """
        return self.match(s)

    def __str__(self):
        if self.xtype == 0:
            # TODO: include midifiers
            return 's/{}/{}/'.format(self.recompiled.pattern, self.repl)
        elif self.xtype == 1:
            return 'm/{}/'.format(self.recompiled.pattern)
        else:
            return 'x/{}/'.format(self.recompiled.pattern)

    def __repr__(self):
        clsname = self.__class__.__name__
        return "{}.perl(r'{}')".format(clsname, self)

    def match(self, s):
        if self.xtype == 0:
            msg = 'a substition regexon does not support matching operation'
            raise ValueError(msg)
        if self.xtype > 0:
            return bool(self.recompiled.match(s))
        if self.xtype < 0:
            return not bool(self.recompiled.match(s))

    def sub(self, s):
        if self.xtype != 0:
            msg = 'a matching regexon does not support substitution operation'
        return self.recompiled.sub(self.repl, s)

    def negate(self):
        self.xtype = - self.xtype
        return self

    @classmethod
    def new(cls, pattern, replacement=None):
        recompiled = re.compile(pattern)
        return cls(recompiled, replacement)

    @classmethod
    def perl(cls, expr):
        if expr.startswith('m'):
            reg = re.compile(r'^m(.)(?P<reg>.*)\1(?P<modif>[a-zA-Z]*)$')
        if expr.startswith('x'):
            reg = re.compile(r'^x(.)(?P<reg>.*)\1(?P<modif>[a-zA-Z]*)$')
        else:
            reg = re.compile(r'^s(.)(?P<reg>.*)\1(?P<repl>.*)\1(?P<modif>[a-zA-Z]*)$')

        mat = reg.match(expr)
        if not mat:
            raise ValueError('invalid substitution expression')
        dic = mat.groupdict()
        flags = cls.perl_modifiers_to_flags(dic['modif'])
        regexon = cls(re.compile(dic['reg'], flags=flags), dic.get('repl'))
        if expr.startswith('x'):
            regexon.negate()
        return regexon

    @staticmethod
    def perl_modifiers_to_flags(modifiers):
        supported_modifiers = {
            'i': re.IGNORECASE,
            'x': re.VERBOSE,
            'm': re.MULTILINE,
            's': re.DOTALL,
            'g': 0,
        }
        bad_modifiers = set(modifiers) - set(supported_modifiers)
        if bad_modifiers:
            errmsg = 'unsupported modifier(s): {}'.format(''.join(bad_modifiers))
            raise ValueError(errmsg)
        flags = 0
        for m in modifiers.lower():
            flags |= supported_modifiers[m]
        return flags

    @classmethod
    def whitespaces_remover(cls):
        return cls.new(r'\s+', '')

    @classmethod
    def alpha(cls):
        return cls.new(r'[^a-zA-Z]', '')

    @classmethod
    def alphanum(cls):
        return cls.new(r'[^a-zA-Z0-9]', '')

    @classmethod
    def tab_delimited(cls):
        """Replace all whitepaces with tab"""
        return cls.new(r'\s+', '\t')

    @classmethod
    def space_delimited(cls):
        """Replace all whitepaces with tab"""
        return cls.new(r'\s+', ' ')


def remove_whitespaces(string):
    """
    Efficiently remove all whitespaces from string
    :param string: bytes or unicode
    :return:
    """
    if isinstance(string, six.text_type):
        return six.text_type().join(string.split())
    if isinstance(string, six.binary_type):
        return string.translate(None, six.b(whitespace))
