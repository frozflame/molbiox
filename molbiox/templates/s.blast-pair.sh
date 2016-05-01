#!/usr/bin/env bash

if [ a.$1 == 'a.' ] || [ a.$2 == 'a.' ]; then
    echo "usage: `basename $0` query.fa database.fa prefix"; exit e
fi

QRFILE=$1; DBFILE=$2; OUTPREFIX=$3
if [ a.${OUTPREFIX} = a. ]; then OUTPREFIX=${QRFILE}; fi

# determine type of blast to use
BLASTEXE=`mbx seq-type ${QRFILE} --blastdb ${DBFILE}`
FMTDBEXE="makeblastdb"

# make sure 2 commands exist; otherwise exit
${BLASTEXE} -h > /dev/null; if [ $? -ne 0 ]; then exit; fi
${FMTDBEXE} -h > /dev/null; if [ $? -ne 0 ]; then exit; fi

# number of threads
NTHR=`mbx etc nproc`
# NTHR="6"

# e-value
EVALUE="1e-5"

OPT=''
# OPT='-max_target_seqs'

# -outfmt 11
FILENAME_FMT11=${OUTPREFIX}.fmt11.${BLASTEXE}

echo -n "${FMTDBEXE} ${DBFILE} ... "

    ${FMTDBEXE} -dbtype `mbx seq-type ${DBFILE}` -in ${DBFILE} > /dev/null

echo Done!


echo -n "${BLASTEXE} ${QRFILE} ${DBFILE} ... "

    ${BLASTEXE}  -query ${QRFILE}  -db ${DBFILE}  -outfmt 11 \
                 -out ${FILENAME_FMT11}  -num_threads ${NTHR}  -evalue ${EVALUE}

    FMTR="blast_formatter ${OPT} -archive ${FILENAME_FMT11}"

    # TODO: include tabfmt to MBX
      ${FMTR} -outfmt "$(mbx etc blast6m)" ${OPT} > ${OUTPREFIX}.fmt6m.${BLASTEXE}
    # ${FMTR} -outfmt "$(mbx etc blast7m)" ${OPT} > ${OUTPREFIX}.fmt7m.${BLASTEXE}

    # ${FMTR} -outfmt 0 ${OPT} > ${QUERY}.fmt0.${BLASTEXE}
    # ${FMTR} -outfmt 6 ${OPT} > ${QUERY}.fmt6.${BLASTEXE}
    # ${FMTR} -outfmt 7 ${OPT} > ${QUERY}.fmt7.${BLASTEXE}

    # remove makeblastdb files
    rm -f ${DBFILE}.{nhr,nin,nsq,phr,pin,psq}

    # remove fmt11
    rm -f ${FILENAME_FMT11}
    
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

