#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import sys
import re

# extract sp|xxxxx|xxx_xxx part
reg_uniprotkb_header = re.compile(r"""
    ^
    (?P<db>\w{2})           # db; sp or tr
    \|(?P<uid>\w+)          # uid for UniqueIdentifier or IsoformName, eg. P27748
    \|(?P<entry>\w+)        # entry for EntryName; eg. ACOX_RALEH
    (?=(?:\s+\w+=|$))       # XX= or EOL
    """, re.VERBOSE)

# extract XX=<value> part
reg_uniprotkb_header_kv = re.compile("""

    (\w+)=                  # key: XX=
    ([^=]+?)                # value
    (?=(?:\s+\w+=|$))       # next XX= or EOL
    """, re.VERBOSE)

# map acronyms to human readable names
dic_uniprotkb_header_keys = {
        'OS':   'organism',
        'GN':   'gene',
        'PE':   'existence',
        'SV':   'version',
}


def parse_uniprotkb_header(cmt):
    """
    The format is specified at http://www.uniprot.org/help/fasta-headers
    :param cmt: cmt field of a fasta record, i.e. header
    :return: a dict
    """
    rdic = dict()
    for k, v in reg_uniprotkb_header_kv.findall(cmt):
        k = dic_uniprotkb_header_keys.get(k, k)
        rdic[k] = v
    mat = reg_uniprotkb_header.match(cmt)
    if mat:
        rdic.update(mat.groupdict())
    return rdic


def test():
    s = 'sp|Q197F7|003L_IIV3 Uncharacterized protein 003L OS='\
        'Invertebrate iridescent virus 3 GN=IIV3-003L PE=4 SV=1'
    rdic = parse_uniprotkb_header(s)
    print(repr(s))
    print(rdic)
