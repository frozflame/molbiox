#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals
import os, sys, re

import molbiox as mbx
from molbiox.io import (fasta, genbank, glimmer, lenfile)

pyfile_regex = re.compile(r'.*\.py[cdxi]?')

filenames = [x for x in os.listdir() if not pyfile_regex.match(x)]

if filenames:
    filename = filenames[0]
