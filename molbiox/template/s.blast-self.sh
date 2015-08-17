#!/usr/bin/env bash

# TODO: support AA also (currently for ATGC only)_

#
QRFILE=$1; DBFILE=$1; OUTPREFIX=$1
if [ x.${OUTPREFIX} = x. ]; then OUTPREFIX=${QRFILE}; fi

# protein or nucleotides
QRT=`mbx-seq-type ${QRFILE}`
DBT=`mbx-seq-type ${DBFILE}`

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
FMTS_MIN=`mbx-etc blast-mini`

# e-value
EVALUE="1e-5"

# -outfmt 11
FMT11=${OUTPREFIX}.fmt11.${BLASTEXE}
echo $FMT11

echo -n "${FMTDBEXE} ${DBFILE} ... "

    ${FMTDBEXE} -dbtype ${DBT} -in ${DBFILE} > /dev/null

echo Done!


echo -n "${BLASTEXE} ${QRFILE} ${DBFILE} ... "

    ${BLASTEXE}  -query ${QRFILE}  -db ${DBFILE}  -outfmt 11 \
                 -out ${FMT11}  -num_threads ${NTHR}  -evalue ${EVALUE}


    # TODO: include tabfmt to MBX
    blast_formatter -archive ${FMT11} -outfmt "6 ${FMTS_MIN}" \
    | awk '{if($1!=$4) print $0;}' \
    | tabfmt > ${OUTPREFIX}.fmt6m.${BLASTEXE}

    # blast_formatter -archive ${OUTNAME} -outfmt "7 ${FMTS_MIN}" > ${OUTPREFIX}.fmt7m.${BLASTEXE}

    # blast_formatter -archive ${FMT11} -outfmt 0 > ${QUERY}.fmt0.${BLASTEXE}
    # blast_formatter -archive ${FMT11} -outfmt 6 > ${QUERY}.fmt6.${BLASTEXE}
    # blast_formatter -archive ${FMT11} -outfmt 7 > ${QUERY}.fmt7.${BLASTEXE}

    # remove makeblastdb files
    rm -f ${DBFILE}.{nhr,nin,nsq,phr,pin,psq}

    # remove fmt11
    rm -f ${FMT11}

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

