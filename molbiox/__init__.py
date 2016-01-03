#!/usr/bin/env python3
# coding: utf-8
import os
import re


def getversion():
    root = os.path.dirname(__file__)
    with open(os.path.join(root, 'VERSION')) as version_file:
        version = version_file.read().strip()
        regex = re.compile(r'^\d+\.\d+\.\d+$')
        if not regex.match(version):
            raise ValueError('VERSION file is corrupted')
        return version

__version__ = getversion()
