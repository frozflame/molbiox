#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals
import sys

from Bio import SeqIO
from molbiox.io import fasta

# TODO: remove dependency to Biopython

filename = sys.argv[1]

record = SeqIO.read(filename, 'gb')

seqdicts = []
for feat in record.features:
    if feat.type == 'CDS':
        seqdict = {
            'cmt': ';'.join(feat.qualifiers['locus_tag']),
            'seq': feat.qualifiers['translation'][0]
        }
        seqdicts.append(seqdict)

fasta.write(filename + '.faa', seqdicts)
