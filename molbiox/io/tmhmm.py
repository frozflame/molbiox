#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals, print_function
import re
from molbiox.frame import streaming, interactive
from molbiox.frame.containers import SRecord


@interactive.castable
def read(infile):
    """
    Parse file generated by TMHMM (decodeanhmm)

    :param infile: a file-like object or path
    :return: None
    """

    record = None
    fw = streaming.FileWrapper(infile, 'r')

    for line in fw.file:
        line = line.rstrip()

        # a new protein (new record)
        if line.startswith('>'):
            if record:
                yield build_tmhmm_record(record)
            record = build_tmhmm_record()
            continue

        if not line or not record:
            continue

        if line.startswith('?0'):
            record['tm.seq'] += line.split()[1]
            continue

        if line.startswith(' ' * 3):
            record['seq'] += line.strip()

    # last record (no '>' to mark end)
    if record:
        yield build_tmhmm_record(record)

    fw.close()


def build_tmhmm_record(record=None):
    if not record:
        record = SRecord(cmt='protein.A', seq='')
        record['tm.seq'] = ''
        return record

    tmseq = record['tm.seq']
    record['tm.m.spans'] = [mat.span() for mat in re.finditer(r'M+', tmseq)]
    record['tm.i.spans'] = [mat.span() for mat in re.finditer(r'i+', tmseq)]
    record['tm.o.spans'] = [mat.span() for mat in re.finditer(r'o+', tmseq)]


# >orf00009.wls-n2360_oprM
# %len 653
# %lett A:50 C:10 D:27 E:35 F:27 G:44 H:13 I:45 K:22 L:88 M:19 N:13 P:32 Q:36 R:40 S:42 T:23 V:64 W:6 Y:17
# %score BG 2704.709591 (4.141975 per character)
# %score FW 2716.609262 (4.160198 per character)
# %score NB(0) 2721.780465 (4.168117 per character)
# %score LO(0) -17.070874 (-0.026142 per character)
# %pred NB(0): i 1 11, M 12 34, o 35 48, M 49 68, i 69 79, M 80 102, o 103 111, M 112 129, i 130 653
#    MLTSFLAIPRVYKRVISICADLLLLTLAFWGSYWVRLDANIPLQSVQHWQMLALLLPITIVIFMRLGLYRAV
# ?0 iiiiiiiiiiiMMMMMMMMMMMMMMMMMMMMMMMooooooooooooooMMMMMMMMMMMMMMMMMMMMiiii
#
#    LRYVGFKVLWTVSLGVLLSTMSLVILAFFMAVPLPRTVSVIYFAFSVLLIGGVRLFFRALVQRSGQQRVAVL
# ?0 iiiiiiiMMMMMMMMMMMMMMMMMMMMMMMoooooooooMMMMMMMMMMMMMMMMMMiiiiiiiiiiiiiii
#
#    IYGAGSSGRQLQLALNQGQEYLPVAFVDDDPVLVKAVIQGVSVYSPDDIEALIERFDIKKILLAMPSASRSV
# ?0 iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
#
#    RQAVINRLEQYPCEVLSIPGMADLLKGYAHIDELKEVSIEDLLGRDAVAPLPELINANISGKRVMVTGAGGS
# ?0 iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
#
#    IGSELCRQIIRCEPVQLVLFELSEYGLYAIDKELQELSQQEGLQVEIVPLLGSVQRQHRLQAVMSSFRIQTV
# ?0 iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
#
#    YHAAAYKHVPLVEYNVVEGVRNNVFGTLYCAQAAIRAKVETFVLISTDKAVRPTNTMGTTKRLAELVLQSLA
# ?0 iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
#
#    AAQRQTRFCMVRFGNVLGSSGSVVPLFRKQIRDGGPLTVTHPDIIRYFMTIPEASQLVIQAGAMGQGGDVFV
# ?0 iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
#
#    LDMGEPVKIIDLAHRMIRLSGLKLKSDKHPAGDIEVKITGLRPGEKLFEELLIGEQVEGTAHPRIMKASELM
# ?0 iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
#
#    LPWPQLRAFLAELDSACFRFDHEQIRSLLLSMPTGFNPTDGICDLVWQAKNSLPHEPCLSVVEDIDFLNSEC
# ?0 iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
#
#    HQPMH
# ?0 iiiii
