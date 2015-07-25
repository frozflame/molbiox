#!/usr/bin/env bash

DTRIM=/opt/sequencing/DynamicTrim.pl
LSORT=/opt/sequencing/LengthSort.pl
MERGE=/opt/sequencing/PairMerge.pl

# NTHREADS="6"
NTHREADS=`mbx-env cpu-count`

# TODO: use optimiser and use multiple cores

for DIR in $@; do

    cd ${DIR}

    # unzip the fastq
    if ls *.gz 1> /dev/null 2>&1; then gunzip *.gz; fi

    find . -iname '*.fastq' -exec ${DTRIM} {} \;
    find . -iname '*.fq'    -exec ${DTRIM} {} \;

    ${LSORT} *.trimmed
    rm -f *.trimmed

    ${MERGE} *.paired?  final.fq
    rm -f *.trimmed.*

    # velveth hv29 29 -fastq -shortPaired final.fq
    # velvetg hv29 -cov_cutoff 18
    velvetoptimiser -s 15 -e 31 -x 2 -t ${NTHREADS} \
        -f '-fastq -shortPaired final.fq' \
        -o '-cov_cutoff 10 -scaffolding yes'

    mv hv29/contigs.fa .

    cd ..

done
