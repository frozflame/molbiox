#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import re
import zlib
import hashlib
from molbiox.algor.traverse import Traverser


class Hasher(object):
    """
    Common interface for hashlib & zlib hash functions
    """
    __hfuncs__ = {
        'adler32':  zlib.adler32,
        'crc32':    zlib.crc32,
        'md5':      hashlib.md5,
        'sha1':     hashlib.sha1,
        'sha224':   hashlib.sha224,
        'sha256':   hashlib.sha256,
        'sha384':   hashlib.sha384,
        'sha512':   hashlib.sha512,
    }

    __hlens__ = {
        32: 'md5',
        40: 'sha1',
        56: 'sha224',
        64: 'sha256',
        96: 'sha384',
        128: 'sha512',
    }

    def __init__(self, name):
        if name not in self.__hfuncs__:
            raise ValueError("'{}' is not a supported hash function".format(name))
        if name in {'adl32', 'crc32'}:
            self.hash = getattr(zlib, name)     # a checksum function
            self.emulate = True
            self.im = self.hash(b'')    # intermediate result
        else:
            self.hash = getattr(hashlib, name)()    # a hash object
            self.emulate = False
            self.im = 0  # not used for hashlib functions

    def update(self, data):
        # hashlib.md* / hashlib.sha*
        if not self.emulate:
            self.hash.update(data)
            return
        # zlib.adler32 / zlib.crc32
        if self.im is None:
            self.im = self.hash(data)
        else:
            self.im = self.hash(data, self.im)

    def hexdigest(self):
        # hashlib.md* / hashlib.sha*
        if not self.emulate:
            return self.hash.hexdigest()
        # zlib.adler32 / zlib.crc32
        return hex(self.im & 0xffffffff).replace('0x', '')

    @classmethod
    def from_signature(cls, signature):
        name = signature.split(':')[0].lower()
        if name not in cls.__hfuncs__:
            name = cls.__hlens__.get(len(signature), 'md5')
        return cls(name)


class SigDictionary(dict):
    """
    A dict with signature (main class in this module)
    """

    def __init__(self, *args, **kwargs):
        super(SigDictionary, self).__init__(*args, **kwargs)
        self._signature = ''

    def sign(self, signature):
        self._signature = signature.lower()

    def inspect(self):
        """
        Inspect integrity of a dict object
        :raise ValueError: if fail
        :return: self
        """
        if not self._signature:
            return

        hasher = Hasher.from_signature(self._signature)
        hvalue = re.sub(r'^[a-z0-9]+:', '', self._signature)
        if hvalue != self.calc(hasher):
            raise ValueError('object is corrupted')

    def calc(self, hasher):
        """
        :param hasher: a Hasher object
        :return: a string (signature)
        """
        travs = Traverser(self, lambda x: hasher.update(x.encode('ascii')))
        travs.traverse()
        return hasher.hexdigest()

    def build(self):
        hasher = Hasher('md5')
        hvalue = self.calc(hasher)
        signature = 'md5:{}'.format(hvalue)
        self.sign(signature)
        return signature

    def format(self):
        pairs = ((repr(k), repr(v)) for k, v in self.items())
        body = ''.join('\t{}:\t{},\n'.format(*p) for p in pairs)
        body = '{\n' + body + '}'
        if self._signature:
            self.inspect()  # always make sure of the integrity
            return body + " + Sig('{}')".format(self._signature)
        else:
            return body

    def print_(self, *args, **kwargs):
        print(self.format(), *args, **kwargs)


class Sig(object):
    def __init__(self, signature, cheat=False):
        self.signature = signature
        self.cheat = cheat

    def __add__(self, other):
        if not isinstance(other, SigDictionary):
            other = SigDictionary(other)
        if self.cheat:
            return other
        other.sign(self.signature)
        return other

    def __radd__(self, other):
        return self + other

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.signature)

    def __str__(self):
        return self.signature

