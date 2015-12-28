#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function

import os, sys, re

import molbiox as mbx
from molbiox.io import (fasta, genbank, glimmer, tmhmm)

pyfile_regex = re.compile(r'.*\.py[cdxi]?')

names = [x for x in os.listdir() if not pyfile_regex.match(x)]

if names:
    n = names[0]
