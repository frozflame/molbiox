#!/usr/bin/env bash

# NTHREADS="6"
NTHREADS=`mbx-env cpu-count`

BLASTEXE="blastp"

# DBDIR="."
# DBDIR="/mnt/fx6300/hailong/Public/dbxbio"
DBDIR="$HOME/Public/dbxbio"

DATABASE="ncbi/nr"
# DATABASE="uniprot/uniprot_sprot.named.fasta"
# DATABASE="uniprot/wzx.named.fasta"
# DATABASE="uniprot/wzy.named.fasta"
# DATABASE="uniprot/wzxy.named.fasta"
# DATABASE="uniprot/oprm.named.fasta"
# DATABASE="uniprot/oprm.named.fasta"
# DATABASE="vibrio/flanking.vibrio.fasta"

EVALUE="1e-5"

for QUERY in $@; do

    OUTNAME=${QUERY}.fmt11.${BLASTEXE}

    echo -n "${BLASTEXE} ${QUERY} ... "

    ${BLASTEXE}  -query ${QUERY}  -db ${DBDIR}/${DATABASE}  -outfmt 11 \
                 -out ${OUTNAME}  -num_threads ${NTHREADS}  -evalue ${EVALUE}

    # blast_formatter -archive ${OUTNAME} -outfmt 0 > ${QUERY}.fmt0.${BLASTEXE}
    # blast_formatter -archive ${OUTNAME} -outfmt 6 > ${QUERY}.fmt6.${BLASTEXE}
    # blast_formatter -archive ${OUTNAME} -outfmt 7 > ${QUERY}.fmt7.${BLASTEXE}

    echo Done!

done
