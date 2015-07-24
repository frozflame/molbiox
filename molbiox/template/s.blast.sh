#!/usr/bin/env bash

NTHREADS="6"
BLASTEXE="blastp"
DATABASE="/home/hailong/Database/ncbi/nr"

EVALUE="1e-5"

for QUERY in $@; do

    OUTNAME=${QUERY}.fmt11.${BLASTEXE}

    ${BLASTEXE}  -query ${QUERY}  -db ${DATABASE}  -outfmt 11 \
                 -out ${OUTNAME}  -num_threads ${NTHREADS}  -evalue ${EVALUE}

    # blast_formatter -archive ${OUTNAME} -outfmt 0 > ${QUERY}.fmt0.${BLASTEXE}
    # blast_formatter -archive ${OUTNAME} -outfmt 6 > ${QUERY}.fmt6.${BLASTEXE}
    # blast_formatter -archive ${OUTNAME} -outfmt 7 > ${QUERY}.fmt7.${BLASTEXE}

done
