#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals

import os
import re
import textwrap

import molbiox.frame.interactive
from molbiox import tolerant
from molbiox.frame.compat import zrange
from molbiox.frame.locate import locate_template


class MetaParser(object):
    def feed(self, line):
        keyword = line[:12].strip()
        if keyword:
            # save current and start a new
            if self.current:
                self.metadata.append(self.current)

            # sub keyword
            if line.startswith(' '):
                keyword = '{}__{}'.format(self.current_top, keyword)
            # top keyword
            else:
                self.current_top = keyword

            # set current (k, v)
            self.current = (keyword, line[12:])

        else:
            self.current = (self.current[0], self.current[1] + line.lstrip())

    def harvest(self):
        metadata = self.metadata
        self.metadata = []
        return metadata

    def __init__(self):
        self.metadata = []
        self.current = tuple()

        # current top keyword
        self.current_top = ''


class FeatParser(object):
    def feed(self, line):
        feattype = line[:21].strip()
        if feattype:
            # save current feature
            if 'feattype' in self.current:
                self.features.append(self.current)
            # begine a new current feature
            location = line[21:].strip()
            self.current = dict(
                feattype=feattype, location=location, quallines=[])
            return
        qualline = line.lstrip()
        if qualline.startswith('/'):
            self.current['quallines'].append(qualline[1:-1])
        else:
            self.current['quallines'][-1] += qualline[:-1]

    def harvest(self):
        features = self.features
        self.features = []
        return features

    def __init__(self):
        self.features = []
        self.current = dict(quallines=[])


class SeqzParser(object):
    def feed(self, line):
        fragments = line.strip().split()[1:]
        self.seqfragments.extend(fragments)

    def harvest(self):
        seqfragments = self.seqfragments
        self.seqfragments = []
        return ''.join(seqfragments)

    def __init__(self):
        self.seqfragments = []

@molbiox.frame.interactive.castable
def read(handle):
    # `handle` is either a file object or a string
    if hasattr(handle, 'read'):
        infile = handle
    else:
        infile = open(handle, 'r')

    # possible modes:
    #   meta
    #   feature
    #   sequence

    mode, gbdict = 'meta', dict()
    metaparser = MetaParser()
    featparser = FeatParser()
    seqzparser = SeqzParser()

    for line in infile:

        # end of a sequence: yield dict
        # mode change to 'keyword'
        if line.startswith('//'):
            gbdict['metadata'] = metaparser.harvest()
            gbdict['features'] = featparser.harvest()
            gbdict['sequence'] = seqzparser.harvest()
            yield gbdict

            mode, gbdict = 'meta', dict()
            continue

        # mode change to 'feature'
        if line.startswith('FEATURES'):
            mode = 'feature'
            continue

        # mode change to 'sequence'
        if line.startswith('ORIGIN'):
            mode = 'sequence'
            continue

        if mode == 'meta':
            metaparser.feed(line)

        if mode == 'feature':
            featparser.feed(line)

        if mode == 'sequence':
            seqzparser.feed(line)

    if infile is not handle:
        infile.close()


@molbiox.frame.interactive.castable
def read_sequences(handle):
    """
    Read a GenBank file and get sequences as seqdicts
    """
    # `handle` is either a file object or a string
    if hasattr(handle, 'read'):
        infile = handle
    else:
        infile = open(handle, 'r')

    seqregion = False
    cmt, seqslices = ('a.SEQ', [])
    for line in infile:
        # do NOT strip!
        # line = line.strip()

        # collect current sequence slices
        if seqregion:
            # end of current sequence/contig, yield the seqdict
            if line.startswith('//'):
                seqregion = False
                yield {
                    'cmt': cmt,
                    'seq': ''.join(seqslices).upper()}
            else:
                items = line.split()
                seqslices.extend(items[1:])
            continue

        # a new sequence/contig: reset cmt and seqslices
        if line.startswith('LOCUS'):
            cmt = re.sub(r'^LOCUS', '', line).strip()
            seqslices = []
            continue
        if line.startswith('ORIGIN'):
            seqregion = True
            continue
    if infile is not handle:
        infile.close()


def write(handle, gbdicts, linesep=os.linesep):
    """
    Support for GenBank format is far from complete...
    """

    if hasattr(handle, 'write'):
        outfile = handle
    else:
        outfile = open(handle, 'w')

    s = ' '

    for gbdict in gbdicts:
        metadata = gbdict['metadata']
        features = gbdict['features']
        sequence = gbdict['sequence']

        # TODO: metadata

        l = "FEATURES{}Location/Qualifiers".format(s*12)
        outfile.write(l + linesep)

        for feat in features:
            feattype = feat['feattype']
            location = feat['location']
            quallines = feat['quallines']

            # feattype & location
            l = s * 5 + feattype + s * (16 - len(feattype)) + location
            outfile.write(l + linesep)

            # quallines
            for qualline in quallines:
                for subqualline in textwrap.wrap('/' + qualline, 58):
                    l = s * 21 + subqualline
                    outfile.write(l + linesep)

        outfile.write(b"ORIGIN" + linesep)

        for i in zrange(0, len(sequence), 60):
            l = '{0:>9}'.format(i + 1) + s.join(textwrap.wrap(sequence[i:i+60], 10))
            outfile.write(l + linesep)

        outfile.write("//" + linesep)

    if outfile is not handle:
        outfile.close()


def test_read_seq(name):
    return list(read_sequences(name))


def test_read(name):
    return list(read(name))


def test_j2(gbdict):
    import jinja2
    tmpl = jinja2.Template(open(locate_template('d.genbank.tpl')).read())
    res = tmpl.render(gbdict=gbdict, wrap=textwrap.wrap)
    return res
