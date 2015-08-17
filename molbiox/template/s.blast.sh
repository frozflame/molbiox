#!/usr/bin/env bash


DBDIR="$HOME/Public/dbxbio"
# DBDIR="."

DBT=prot; DB="ncbi/nr"
# DBT=prot; DB="uniprot/uniprot_sprot.named.fasta"
# DBT=prot; DB="uniprot/wzx.named.fasta"
# DBT=prot; DB="uniprot/wzy.named.fasta"
# DBT=prot; DB="uniprot/wzxy.named.fasta"
# DBT=prot; DB="uniprot/oprm.named.fasta"
# DBT=prot; DB="vibrio/flanking.vibrio.fasta"

# number of threads
NTHR=`mbx-env cpu-count`
# NTHR="6"

# format specifiers
FMTS_MIN=`mbx-etc blast-mini`

# e-value
EVALUE="1e-5"


for QUERY in $@; do


    # detect query seq-type
    QRT=`mbx-seq-type ${QUERY}`

    # determine type of blast to use
    if   [ ${QRT}.${DBT} == 'prot.prot' ]; then BLASTEXE='blastp';
    elif [ ${QRT}.${DBT} == 'nucl.nucl' ]; then BLASTEXE='blastn';
    elif [ ${QRT}.${DBT} == 'nucl.prot' ]; then BLASTEXE='blastx';
    elif [ ${QRT}.${DBT} == 'prot.nucl' ]; then BLASTEXE='tblastn'; fi

    FMT11=${QUERY}.fmt11.${BLASTEXE}

    echo -n "${BLASTEXE} ${QUERY} ... "

    ${BLASTEXE}  -query ${QUERY}  -db ${DBDIR}/${DB}  -outfmt 11 \
                 -out ${FMT11}  -num_threads ${NTHR}  -evalue ${EVALUE}

      blast_formatter -archive ${FMT11} -outfmt "6 ${FMTS_MIN}" > ${QUERY}.fmt6m.${BLASTEXE}
    # blast_formatter -archive ${FMT11} -outfmt "7 ${FMTS_MIN}" > ${QUERY}.fmt7m.${BLASTEXE}
    # blast_formatter -archive ${FMT11} -outfmt "6 ${FMTS_ALL}" > ${QUERY}.fmt6a.${BLASTEXE}
    # blast_formatter -archive ${FMT11} -outfmt "7 ${FMTS_ALL}" > ${QUERY}.fmt7a.${BLASTEXE}

    # blast_formatter -archive ${FMT11} -outfmt 0 > ${QUERY}.fmt0.${BLASTEXE}

    echo Done!

    # rm ${FMT11}

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

