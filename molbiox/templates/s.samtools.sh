#!/usr/bin/env bash


# NTHREADS=6
NTHREADS=`mbx-env cpu-count`

PREFIX=$1
FILENAME_REF=$2
FILENAME_READS=$3


bowtie-build ${FILENAME_REF} ${FILENAME_REF}

bowtie -S -p ${NTHREADS} ${FILENAME_REF} ${FILENAME_READS} ${PREFIX}.sam

samtools faidx ${FILENAME_REF}

samtools import ${FILENAME_REF}.fai ${PREFIX}.sam ${PREFIX}.bam

samtools sort ${PREFIX}.bam ${PREFIX}.sorted

samtools index ${PREFIX}.sorted.bam

echo "You probably want view the alignment:"
echo
echo "    samtools tview ${PREFIX}.sorted.bam ${FILENAME_REF}"
echo



