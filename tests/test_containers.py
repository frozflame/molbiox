#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
# import sys
import unittest
from copy import deepcopy
from string import digits

import molbiox.frame.containers
from molbiox.frame import containers


cycstring = molbiox.frame.containers.CycleString(digits)


def _sq_assert(squeue):
    squeue = deepcopy(squeue)
    length = len(squeue)
    assert squeue.free + length == squeue.size
    assert squeue.put('') == ''

    string = squeue.get()
    assert squeue.free == squeue.size
    assert len(string) == length
    assert len(squeue) == 0


class TestSQueue(unittest.TestCase):
    def setUp(self):
        pass


def test_squeue():
    maxnum = 20
    for l in range(maxnum):
        # unlimited size
        squeue = containers.SQueue()
        _sq_assert(squeue)

        squeue = containers.SQueue(maxnum)
        string = cycstring[:l]
        assert squeue.put(string) == ''

        squeue = containers.SQueue(l)
        string = cycstring[:maxnum]
        assert len(squeue.put(string)) + l == maxnum


