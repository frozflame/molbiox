#!/usr/bin/env python3
# coding: utf-8
from __future__ import unicode_literals, print_function
import hashlib
from molbiox.algor.traverse import Traverser

from zlib import adler32

class CK(object):
    def __init__(self):
        self.value = None

    def consume(self, data):
        data = data.encode('ascii')
        if self.value is None:
            self.value = adler32(data)
        else:
            self.value = adler32(data, self.value)

for x in range(1000):
    ck = CK()
    # m = hashlib.md5()
    travr = Traverser(ab_strains, lambda x: None)
    # travr = Traverser(ab_strains, lambda x: m.update(x.encode('ascii')))
    travr = Traverser(ab_strains, ck.consume)
    travr.traverse()
    # hval = m.hexdigest()
# print(hval)
print(time() - t)
import sys

if __name__ == '__main__':
    pass

