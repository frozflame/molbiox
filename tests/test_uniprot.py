#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import sys
from molbiox.io import uniprot


def show_result(dbtype, cmt, rdic):
    import json
    print(dbtype, repr(cmt))
    print(json.dumps(rdic, indent=4))


def test_parse_uniprotkb_header():
    # uniprotkb
    s = 'sp|Q197F7|003L_IIV3 Uncharacterized protein 003L OS=Invertebrate iridescent virus 3 GN=IIV3-003L PE=4 SV=1'
    rdic = uniprot.parse_uniprotkb_header(s)
    show_result('uniprotkb', s, rdic)
    assert rdic['db'] == 'sp'
    assert rdic['UniqueIdentifier'] == 'Q197F7'
    assert rdic['EntryName'] == '003L_IIV3'
    assert rdic['ProteinName'] == 'Uncharacterized protein 003L'
    assert rdic['OrganismName'] == 'Invertebrate iridescent virus 3'
    assert rdic['GeneName'] == 'IIV3-003L'
    assert rdic['ProteinExistence'] == '4'
    assert rdic['SequenceVersion'] == '1'


def test_parse_uniref_header():
    s = 'UniRef100_A5DI11 Elongation factor 2 n=1 Tax=Pichia guilliermondii RepID=EF2_PICGU'
    rdic = uniprot.parse_uniref_header(s)
    show_result('uniref', s, rdic)
    assert rdic['UniqueIdentifier'] == 'UniRef100_A5DI11'
    assert rdic['ClusterName'] == 'Elongation factor 2'
    assert rdic['Members'] == '1'
    assert rdic['Taxon'] == 'Pichia guilliermondii'
    assert rdic['RepresentativeMember'] == 'EF2_PICGU'


def test_parse_uniparc_header():
    s = 'UPI0000000005 status=active'
    rdic = uniprot.parse_uniparc_header(s)
    show_result('uniparc', s, rdic)
    assert rdic['Status'] == 'active'
    assert rdic['UniqueIdentifier'] == 'UPI0000000005'


def test_archived_uniprotkb_header():
    s = 'sp|P05067 archived from Release 9.2/51.2 28-NOV-2006 SV=3'
    rdic = uniprot.parse_archived_uniprotkb_header(s)
    show_result('archived_uniprotkb', s, rdic)
    assert rdic['db'] == 'sp'
    assert rdic['UniqueIdentifier'] == 'P05067'
    assert rdic['ReleaseNumber'] == '9.2/51.2'
    assert rdic['ReleaseDate'] == '28-NOV-2006'
    assert rdic['SequenceVersion'] == '3'


if __name__ == '__main__':
    test_parse_uniprotkb_header()
    test_parse_uniref_header()
    test_parse_uniparc_header()
    test_archived_uniprotkb_header()


