#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import re


"""
http://www.uniprot.org/help/fasta-headers
"""


# extract sp|xxxxx|xxx_xxx part
reg_uniprotkb_header = re.compile(r"""
    (?P<db>\w+)
    \|(?P<UniqueIdentifier>\w+)
    \|(?P<EntryName>\w+)
    \s+
    (?P<ProteinName>[^=]+)
    (?=(?:\s+\w+=))
    """, re.VERBOSE)

reg_uniref_header = re.compile(r"""
    (?P<UniqueIdentifier>\w+)\s+
    (?P<ClusterName>[^=]+)
    (?=(?:\s+\w+=))
    """, re.VERBOSE)

reg_uniparc_header = re.compile(r"""
    (?P<UniqueIdentifier>\w+)
    (?=(?:\s+\w+=))
    """, re.VERBOSE)

reg_archived_uniprotkb_header = re.compile(r"""
    (?P<db>\w+)
    \|(?P<UniqueIdentifier>\w+)\s+
    archived\sfrom\sRelease\s
    (?P<ReleaseNumber>\S+)\s+
    (?P<ReleaseDate>\S+)
    (?=(?:\s+\w+=))
    """, re.VERBOSE)


# extract XX=<value> part
reg_uniprot_header_kv = re.compile("""
    (\w+)=                  # key: XX=
    ([^=]+?)                # value
    (?=(?:\s+\w+=))       # next XX= or EOL
    """, re.VERBOSE)

# map acronyms to human readable names
dic_uniprot_header_keys = {
        'OS':       'OrganismName',
        'GN':       'GeneName',
        'PE':       'ProteinExistence',
        'SV':       'SequenceVersion',
        'n':        'Members',
        'Tax':      'Taxon',
        'RepID':    'RepresentativeMember',
        'status':   'Status',
}


def _parse_header(cmt, regex):
    """
    The format is specified at http://www.uniprot.org/help/fasta-headers
    :param cmt: cmt field of a fasta record, i.e. header
    :return: a dict
    """
    rdic = dict()
    for k, v in reg_uniprot_header_kv.findall(cmt + ' D='):
        k = dic_uniprot_header_keys.get(k, k)
        rdic[k] = v
    mat = regex.match(cmt)
    if mat:
        rdic.update(mat.groupdict())
    return rdic


def parse_uniprotkb_header(cmt):
    return _parse_header(cmt, reg_uniprotkb_header)


def parse_uniref_header(cmt):
    return _parse_header(cmt, reg_uniref_header)


def parse_uniparc_header(cmt):
    return _parse_header(cmt, reg_uniparc_header)


def parse_archived_uniprotkb_header(cmt):
    return _parse_header(cmt, reg_archived_uniprotkb_header)
