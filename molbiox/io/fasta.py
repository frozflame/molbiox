#!/usr/bin/env python3
# encoding: utf-8

from __future__ import unicode_literals, print_function
import os
import re
import six
import itertools
from collections import deque
from molbiox.frame import interactive
from molbiox.frame.common import SRecord
from molbiox.frame.regexon import remove_whitespaces


class Buffer(object):
    def __init__(self, size):
        self._check(size)
        self.free = size
        self.size = size
        self.queue = deque()

    def get(self):
        string = ''.join(self.queue)
        self.queue.clear()
        self.free = self.size
        return string

    def put(self, string):
        if len(string) > self.free:
            retval = string[self.free:]
            self.queue.append(string[:self.free])
            self.free = 0
            return retval
        else:
            self.queue.append(string)
            self.free -= len(string)
            return ''

    @staticmethod
    def _check(size):
        if not isinstance(size, six.integer_types):
            raise TypeError("size must be an integer")
        if size < 0:
            raise ValueError("size must be a non-negative integer")


class CommentState(object):
    def __init__(self):
        self.cmt = ''
        self.anonym_count = 0

    def get(self):
        if self.cmt:
            return self.cmt
        else:
            self.anonym_count += 1
            return 'anonym.{}'.format(self.anonym_count)

    def update(self, cmtline, concise):
        """
        Update and get previous state
        :param cmtline: a string like '>Ab00129.4 len'
        :param concise: bool, remove first whitespace and following chars or not
        :return: a string, previous cmt
        """
        # prepare return value first
        retval = self.get()

        # set state
        if concise:
            parts = cmtline.split()
            if parts:
                self.cmt = parts[0]
            else:
                self.cmt = ''
        else:
            self.cmt = cmtline.lstrip()
        return retval


def iterate_chunks(fw):
    cmtreg = re.compile(r'>[^>]*?\n')
    headpos = 0
    while True:
        chunk = fw.read(2**20)
        if not chunk:
            break
        for mat in cmtreg.finditer(chunk):
            if mat.start() != headpos:
                seq = chunk[headpos:mat.start()]
                yield remove_whitespaces(seq)
            yield mat.group().strip()
            headpos = mat.end()
        seq = chunk[headpos:]
        yield remove_whitespaces(seq)


@interactive.castable
def read(infile, concise=True, limit=10**9):
    """
    Reading a FASTA file should NOT be complicated!

    :param infile: a file object or a string
    :param concise: remove chars after first whitespace in cmt field
    :param limit: max seq length per record
    :return: a generator of SRecord objects

    Say we have

        >ORF00024
        ATCTGTCCTACTCCCGTC...TC
        >ORF00025
        GTCTGTCCTACTCCCGTC...TC

    Then we will get something equivolent to (but in generator form)

        [
            {
                'cmt': 'ORF00024',
                'seq': 'ATCTGTCCTACTCCCGTC...TC'
            },
            {
                'cmt': 'ORF00025',
                'seq': 'GTCTGTCCTACTCCCGTC...TC'
            }
        ]

    Nothing frustrates you. If you want to iterate through a multi-seq FASTA
    file a second time, `itertools.tee` may help you:

        recgen = fasta.read('contigs.fas')
        reciter, reciter1 = itertools.tee(recgen)

        for rec in reciter:
            print(rec.cmt, rec.seq)

        for rec in reciter1:
            print(rec.cmt, rec.seq)
    """
    fw = interactive.FileWrapper(infile, 'r')

    beg = '>'

    # fw_lines = (l.strip() for l in fw.file)  # the slow version
    fw_lines = iterate_chunks(fw)
    fw_lines = itertools.chain(fw_lines, ['>epilogue'])

    if limit < 1:
        limit = 10**9

    offset = 0
    buffer = Buffer(limit)
    cstate = CommentState()

    for line in fw_lines:
        # print('debug fasta.read: outter for loop')
        if line.startswith(beg):
            seq = buffer.get()
            cmt = cstate.update(line[1:], concise)
            # yield previous rec; discard if no seq
            if seq:
                yield SRecord(cmt=cmt, seq=seq, offset=offset)
            offset = 0

        else:
            remainder = buffer.put(line)
            while remainder:
                # print('debug fasta.read: inner while loop')
                seq = buffer.get()
                cmt = cstate.get()
                yield SRecord(cmt=cmt, seq=seq, offset=offset)
                offset += limit
                remainder = buffer.put(remainder)


def readone(infile, concise=True, limit=10 ** 9):
    return read(infile, concise, limit, castfunc=0)


def readseq(infile, concise=True, limit=10**9):
    return read(infile, concise, limit, castfunc=0)['seq']


def write(outfile, records, concise=False, linesep=os.linesep, linewidth=60):
    """
    Reverse of `fasta.read`.

    :param outfile: a file-like object or path to the output FASTA file
    :param records: an iterable like [{'cmt': 'SEQ1', 'seq': 'ATCTC...T'}, ...]
    :param concise: remove chars after first whitespace in cmt field
    :param linesep: newline symbol
    :param linewidth: default 60
    :return: a generator
    """
    # TODO: open mode `w` or `wb`?
    # TODO: use binary project wide
    fw = interactive.FileWrapper(outfile, 'wb')

    # accept a single record
    if isinstance(records, dict):
        records = [records]

    cstate = CommentState()
    offset_expected = 0

    # first rec: cmt != cstate.get() always true even cmt == 'anonym.xx'
    cstate.cmt = 1

    for rec in records:
        cmt = rec.get('cmt')  # if empty, cstate will provide one
        seq = rec.get('seq')  # if empty, skip
        offset = rec.get('offset')
        if not seq:
            continue
        # after set offset to 0, always treat rec as offseted
        if cmt != cstate.get():
            offset_expected = 0
            cstate.update(cmt, concise)
        if offset is not None and offset != offset_expected:
            raise ValueError('bad offset, your data might be corrupted')
        if offset_expected == 0:
            cmtline = '>{}{}'.format(cstate.get(), linesep)
            fw.write(cmtline)

        offset_expected += len(seq)
        for i in six.moves.range(0, len(seq), linewidth):
            fw.write(seq[i:i+linewidth])
            fw.write(linesep)
    fw.close()


def pack(cmt, chunks):
    offset = 0
    for chunk in chunks:
        yield SRecord(cmt=cmt, seq=chunk, offset=offset)
        offset += len(chunk)


def fix_comment(cmt, prefix='', suffix=''):
    """
    Fix seqrecord comment

        >(prefix)Key(suffix) other_descriptions
        ATTCGGGGGTCTGGCTAG...
    """
    regex_key = re.compile(r'^\S+')
    return regex_key.sub(prefix + r'\g<0>' + suffix, cmt)


def fix_filename(name, prefix='', suffix=''):
    """
    Remove common fasta extensions and join with prefix & suffix

        (prefix)N2700.contigs<.fa>(suffix)
    """
    regex_ext = re.compile(r'\.(fa|fas|fasta|fna|ffn|faa|frn)$')
    return prefix + regex_ext.sub('', name) + suffix


def match_contig_name(names, keyword):
    keyword = re.escape(keyword)
    regex = re.compile(r'^(.*[^a-zA-Z0-9]+)?' + keyword + '([^a-zA-Z0-9]+.*)?$', re.I)
    for name in names:
        if regex.match(name):
            return name
