#!/usr/bin/env bash

if [ a.$1 == 'a.' ]; then
    echo "usage: `basename $0` seq1.fa seq2.fa seq3.fa ..."
    echo ".....: edit the script to change database"
    exit 1
fi


DBDIR="$HOME/Public/dbxbio"
# DBDIR="."

DBT=prot; DB="ncbi/nr"
# DBT=prot; DB="uniprot/uniprot_sprot.named.fasta"
# DBT=prot; DB="uniprot1/wzx.named.fasta"
# DBT=prot; DB="uniprot1/wzy.named.fasta"
# DBT=prot; DB="uniprot1/wzxy.named.fasta"
# DBT=prot; DB="uniprot1/oprm.named.fasta"
# DBT=prot; DB="vibrio/flanking.vibrio.fasta"

# number of threads
NTHR=`mbx-env cpu-count`
# NTHR="6"

# format specifiers
FMTS_MINI=`mbx-etc blast-mini`
FMTS_FULL=`mbx-etc blast-full`

# e-value
EVALUE="1e-5"

OPT=''
# OPT='-max_target_seqs 1'


for QUERY in $@; do


    # detect query seq-type
    QRT=`mbx-seq-info -a type ${QUERY}`

    # determine type of blast to use
    if   [ ${QRT}.${DBT} == 'prot.prot' ]; then BLASTEXE='blastp';
    elif [ ${QRT}.${DBT} == 'nucl.nucl' ]; then BLASTEXE='blastn';
    elif [ ${QRT}.${DBT} == 'nucl.prot' ]; then BLASTEXE='blastx';
    elif [ ${QRT}.${DBT} == 'prot.nucl' ]; then BLASTEXE='tblastn'; fi

    FMT11=${QUERY}.fmt11.${BLASTEXE}

    echo -n "${BLASTEXE} ${QUERY} ... "

    ${BLASTEXE}  -query ${QUERY}  -db ${DBDIR}/${DB}  -outfmt 11 \
                 -out ${FMT11}  -num_threads ${NTHR}  -evalue ${EVALUE}

    FMTR="blast_formatter ${OPT} -archive ${FMT11}"

      ${FMTR} -outfmt "6 ${FMTS_MINI}" > ${QUERY}.fmt6m.${BLASTEXE}
    # ${FMTR} -outfmt "7 ${FMTS_MINI}" > ${QUERY}.fmt7m.${BLASTEXE}
    # ${FMTR} -outfmt "6 ${FMTS_FULL}" > ${QUERY}.fmt6a.${BLASTEXE}
    # ${FMTR} -outfmt "7 ${FMTS_FULL}" > ${QUERY}.fmt7a.${BLASTEXE}

    # ${FMTR} -outfmt 0 > ${QUERY}.fmt0.${BLASTEXE}

    echo Done!

    # remove fmt11 output rm11
    # rm ${FMT11}

    # remove empty results
    find . -name "${QUERY}.*.${BLASTEXE}" -type f -size 0 -delete

done


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
# tblastn
#   compares a protein query sequence against a nucleotide sequence database
#   dynamically translated in all reading frames
#
# tblastx (nucl vs nucl but frameshifts are punished deadly)
#   compares the six-frame translations of a nucleotide query sequence against
#   the six-frame translations of a nucleotide sequence database.
#
#   Please note that tblastx program cannot be used with the nr database on the
#   BLAST Web page.

