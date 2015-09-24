#!/usr/bin/env bash

if [ a.$1 == 'a.' ] || [ a.$2 == 'a.' ]; then
    echo "usage: `basename $0` query.fa database.fa prefix"; exit e
fi

QRFILE=$1; DBFILE=$2; OUTPREFIX=$3
if [ a.${OUTPREFIX} = a. ]; then OUTPREFIX=${QRFILE}; fi

# protein or nucleotides
QRT=`mbx-seq-info -a type ${QRFILE}`
DBT=`mbx-seq-info -a type ${DBFILE}`

# determine type of blast to use
if   [ ${QRT}.${DBT} == 'prot.prot' ]; then BLASTEXE='blastp';
elif [ ${QRT}.${DBT} == 'nucl.nucl' ]; then BLASTEXE='blastn';
elif [ ${QRT}.${DBT} == 'nucl.prot' ]; then BLASTEXE='blastx';
elif [ ${QRT}.${DBT} == 'prot.nucl' ]; then BLASTEXE='tblastn'; fi

# make sure 2 commands exist; otherwise exit
FMTDBEXE="makeblastdb"
${BLASTEXE} -h > /dev/null; if [ $? -ne 0 ]; then exit; fi
${FMTDBEXE} -h > /dev/null; if [ $? -ne 0 ]; then exit; fi

# number of threads
NTHR=`mbx-env cpu-count`
# NTHR="6"

# format specifiers
FMTS_MINI=`mbx-etc blast-mini`

# e-value
EVALUE="1e-5"

OPT=''
# OPT='-max_target_seqs'

# -outfmt 11
FMT11=${OUTPREFIX}.fmt11.${BLASTEXE}

echo -n "${FMTDBEXE} ${DBFILE} ... "

    ${FMTDBEXE} -dbtype ${DBT} -in ${DBFILE} > /dev/null

echo Done!


echo -n "${BLASTEXE} ${QRFILE} ${DBFILE} ... "

    ${BLASTEXE}  -query ${QRFILE}  -db ${DBFILE}  -outfmt 11 \
                 -out ${FMT11}  -num_threads ${NTHR}  -evalue ${EVALUE}

    FMTR="blast_formatter ${OPT} -archive ${FMT11}"

    # TODO: include tabfmt to MBX
      ${FMTR} -outfmt "6 ${FMTS_MINI}" ${OPT} | tabfmt > ${OUTPREFIX}.fmt6m.${BLASTEXE}
    # ${FMTR} -outfmt "7 ${FMTS_MINI}" ${OPT} > ${OUTPREFIX}.fmt7m.${BLASTEXE}

    # ${FMTR} -outfmt 0 ${OPT} > ${QUERY}.fmt0.${BLASTEXE}
    # ${FMTR} -outfmt 6 ${OPT} > ${QUERY}.fmt6.${BLASTEXE}
    # ${FMTR} -outfmt 7 ${OPT} > ${QUERY}.fmt7.${BLASTEXE}

    # remove makeblastdb files
    rm -f ${DBFILE}.{nhr,nin,nsq,phr,pin,psq}

    # remove fmt11
    rm -f ${FMT11}
    
    # remove empty results
    find . -name "${QUERY}.*.${BLASTEXE}" -type f -size 0 -delete

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

