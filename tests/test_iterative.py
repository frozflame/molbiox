#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import sys
from string import digits

import molbiox.frame.containers


def test_cycle_string():
    cycstring = molbiox.frame.containers.CycleString(digits)
    for i in range(101):
        s = cycstring[:i]
        assert len(s) == i
