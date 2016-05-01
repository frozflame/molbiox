#!/usr/bin/env bash

if [ a.$1 == 'a.' ]; then
    echo "usage: `basename $0` sequence.fa"; exit 1
fi

QRFILE=$1; DBFILE=$1; OUTPREFIX=$1
if [ x.${OUTPREFIX} = x. ]; then OUTPREFIX=${QRFILE}; fi

# determine type of blast to use
BLASTEXE=`mbx seq-type ${QRFILE} --blastdb ${DBFILE}`
FMTDBEXE="makeblastdb"

# make sure 2 commands exist; otherwise exit
${BLASTEXE} -h > /dev/null; if [ $? -ne 0 ]; then exit; fi
${FMTDBEXE} -h > /dev/null; if [ $? -ne 0 ]; then exit; fi

# number of threads
NTHR=`mbx q nproc`
# NTHR="6"

# e-value
EVALUE="1e-5"

OPT=''
# OPT='-max_target_seqs'

# -outfmt 11
FMT11=${OUTPREFIX}.fmt11.${BLASTEXE}

echo -n "${FMTDBEXE} ${DBFILE} ... "

    ${FMTDBEXE} -dbtype $(mbx seq-type ${DBFILE}) -in ${DBFILE} > /dev/null

echo Done!


echo -n "${BLASTEXE} ${QRFILE} ${DBFILE} ... "

    ${BLASTEXE}  -query ${QRFILE}  -db ${DBFILE}  -outfmt 11 \
                 -out ${FMT11}  -num_threads ${NTHR}  -evalue ${EVALUE}

    FMTR="blast_formatter ${OPT} -archive ${FMT11}"

    # TODO: include tabfmt to MBX
    ${FMTR} -outfmt "`mbx q blast6m`" | awk '{if($1!=$4) print $0;}' \
    | tabfmt > ${OUTPREFIX}.fmt6m.${BLASTEXE}

    # ${FMTR} -outfmt "`mbx q blast7m`" > ${OUTPREFIX}.fmt7m.${BLASTEXE}

    # ${FMTR} -outfmt 0 > ${OUTPREFIX}.fmt0.${BLASTEXE}
    # ${FMTR} -outfmt 6 > ${OUTPREFIX}.fmt6.${BLASTEXE}
    # ${FMTR} -outfmt 7 > ${OUTPREFIX}.fmt7.${BLASTEXE}

    # remove makeblastdb files
    rm -f ${DBFILE}.{nhr,nin,nsq,phr,pin,psq}

    # remove fmt11
    rm -f ${FMT11}

    # remove empty results
    find . -name "${OUTPREFIX}.*.${BLASTEXE}" -type f -size 0 -delete

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

