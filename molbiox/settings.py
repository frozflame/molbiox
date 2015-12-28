#!/usr/bin/env python3
# coding: utf-8
from __future__ import unicode_literals, print_function

all_templates = {
    # command   template
    'test':         's.mbxtest.py',
    'python':       's.script.py',
    'module-exec':  's.mbx-exec-module.py',
    'me':           's.mbx-exec-module.py',

    'seq':          's.seq.py',

    'blast':        's.blast.sh',
    'blast-norm':   's.blast.sh',
    'blast-pair':   's.blast-pair.sh',
    'blast-self':   's.blast-self.sh',
    'blast-fmt':    's.blast-fmtr.sh',


    'bwa':          's.bwa.sh',

    'sspace':       's.sspace.sh',
    'gapfiller':    's.sspace-gapfiller.sh',

    'velvet':       's.velvet.sh',
    'glimmer':      's.glimmer.sh',
    'hmmscan':      's.hmmscan.sh',
    'muscle':       's.muscle.sh',
    'tmhmm':        's.tmhmm.sh',

    'pysam':        's.pysam.py',

    'pred-sql':     'd.feat-create.sql',

    'py-decorator': 'x.decorator.py',
}

commands = all_templates
SHV_PATH = "/Users/Hailong/Documents/molbiox/shelve"
