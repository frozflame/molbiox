#!/usr/bin/env python3
# coding: utf-8
from __future__ import unicode_literals, print_function
import hashlib
from molbiox.algor.traverse import Traverser

from zlib import adler32

ab_strains = {
    'N2733': 'O32', 'N2735': 'O34', 'N2742': 'O44', 'N2744': 'O46',
    'N2745': 'O47', 'N2747': 'O49', 'N2748': 'O50', 'N2749': 'O51'}


class CK(object):
    def __init__(self):
        self.value = None

    def consume(self, data):
        data = data.encode('ascii')
        if self.value is None:
            self.value = adler32(data)
        else:
            self.value = adler32(data, self.value)


def test_traverse():
    for x in range(1000):
        ck = CK()
        # m = hashlib.md5()
        # travr = Traverser(ab_strains, lambda x: None)
        # travr = Traverser(ab_strains, lambda x: m.update(x.encode('ascii')))
        travr = Traverser(ab_strains, ck.consume)
        travr.traverse()


if __name__ == '__main__':
    test_traverse()

