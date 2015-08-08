#!/usr/bin/env python3
# coding: utf-8

import sys
import math

from molbiox.iofmt import blast, lenfile
from molbiox.visual.markline import Markline

__author__ = 'Hailong'

filename = sys.argv[1]

lendict = lenfile.read(filename + '.len', )


resdict = dict()
for record in blast.read_fmt7(filename):
    query = record['query.id']
    subject = record['subject.id'].split('.')[0].lower()
    if query in resdict:
        resdict[query][subject].append(record)
    else:
        resdict[query] = dict(gmhd=[], rjg=[])


for query, content in resdict.items():
    if content['gmhd'] and content['rjg']:
        gmh_positions = []
        rjg_positions = []
        all_positions = []

        for x in content['gmhd']:
            if x['identity'] < 50 or x['alignment.length'] < 100:
                continue

            gmh_mid = (x['q.start'] + x['q.end']) / 2.
            gmh_positions.append(gmh_mid)
            all_positions.append(x['q.start'])
            all_positions.append(x['q.end'])

        for x in content['rjg']:
            rjg_mid = (x['q.start'] + x['q.end']) / 2.
            rjg_positions.append(rjg_mid)
            all_positions.append(x['q.start'])
            all_positions.append(x['q.end'])

        length = lendict.get(query) # or max(all_positions)

        mline = Markline(length, math.ceil(length/1000.))

        for pos in gmh_positions:
            mline.mark(pos, 'g')
        for pos in rjg_positions:
            mline.mark(pos, 'r')

        print(filename, query[:10], mline.string)
