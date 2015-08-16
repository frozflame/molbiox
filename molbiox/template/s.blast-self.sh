#!/usr/bin/env bash

# TODO: support AA also (currently for ATGC only)_

#
QRFILE=$1; DBFILE=$1; OUTPREFIX=$1
if [ x.${OUTPREFIX} = x. ]; then OUTPREFIX=${QRFILE}; fi

# NTHREADS="6"
NTHREADS=`mbx-env cpu-count`

BLASTEXE="blastn"
FMTDBEXE="makeblastdb"

# make sure 2 commands exist; otherwise exit
${BLASTEXE} -h > /dev/null; if [ $? -ne 0 ]; then exit; fi
${FMTDBEXE} -h > /dev/null; if [ $? -ne 0 ]; then exit; fi


EVALUE="1e-6"

MINFIELDS="qseqid qlen slen sseqid length pident qstart qend sstart send"

OUTNAME=${OUTPREFIX}.fmt11.${BLASTEXE}

echo -n "${FMTDBEXE} ${DBFILE} ... "

    ${FMTDBEXE} -dbtype nucl -in ${DBFILE} > /dev/null

echo Done!


echo -n "${BLASTEXE} ${QRFILE} ${DBFILE} ... "

    ${BLASTEXE}  -query ${QRFILE}  -db ${DBFILE}  -outfmt 11 \
                 -out ${OUTNAME}  -num_threads ${NTHREADS}  -evalue ${EVALUE}

    # blast_formatter -archive ${OUTNAME} -outfmt 0 > ${QUERY}.fmt0.${BLASTEXE}
    # blast_formatter -archive ${OUTNAME} -outfmt 6 > ${QUERY}.fmt6.${BLASTEXE}
    # blast_formatter -archive ${OUTNAME} -outfmt 7 > ${QUERY}.fmt7.${BLASTEXE}

    # TODO: include tabfmt to MBX
    blast_formatter -archive ${OUTNAME} -outfmt "6 ${MINFIELDS}" \
    | awk '{if($1!=$4) print $0;}' \
    | tabfmt > ${OUTPREFIX}.fmt6m.${BLASTEXE}

    # blast_formatter -archive ${OUTNAME} -outfmt "7 ${MINFIELDS}" > ${OUTPREFIX}.fmt7m.${BLASTEXE}

    # remove makeblastdb files -- nucl
    rm -f ${DBFILE}.nhr
    rm -f ${DBFILE}.nin
    rm -f ${DBFILE}.nsq

    # remove makeblastdb files -- prot
    rm -f ${DBFILE}.phr
    rm -f ${DBFILE}.pin
    rm -f ${DBFILE}.psq

    # remove fmt11
    rm -f ${OUTNAME}

echo Done!



# The NCBI BLAST family of programs includes:
#
# blastp
#   compares an amino acid query sequence against a protein sequence database
#
# blastn
#   compares a nucleotide query sequence against a nucleotide sequence database
#
# blastx
#   compares a nucleotide query sequence translated in all reading frames
#   against a protein sequence database
#
# tblast
#   compares a protein query sequence against a nucleotide sequence database
#   dynamically translated in all reading frames
#
# tblastx (nucl vs nucl but frameshifts are punished deadly)
#   compares the six-frame translations of a nucleotide query sequence against
#   the six-frame translations of a nucleotide sequence database.
#
#   Please note that tblastx program cannot be used with the nr database on the
#   BLAST Web page.

