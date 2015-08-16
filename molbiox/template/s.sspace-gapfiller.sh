#!/usr/bin/env bash

REF=$1
QR1=$2
QR2=$3


# NTHREADS="6"
NTHREADS=`mbx-env cpu-count`
EXEC="perl /opt/gapfiller/GapFiller.pl"


# base name (default standard_output)
PREFIX=${REF}.filler

rm -f .gapfiller.libs.txt
echo "lib1 bwa ${QR1} ${QR2} 450 0.35 FR" > .gapfiller.libs.txt

${EXEC} -s ${REF} -l .gapfiller.libs.txt -T ${NTHREADS} -b ${PREFIX} -d 500



# ... from README file in gapfiller 
# General Parameters:
# -l  Library file containing two mate pate files with insert size, error and orientation indication
# -s  Fasta file containing scaffold sequences used for extension
#
# Extension Parameters (default values in brackets):
# -m  Minimum number of overlapping bases with the sequences around the gap(30)
# -t  Number of bases to trim of from edges of the gap, usually containing misassemblies (10)
# -o  Minimum number of reads needed to call a base during an extension (2)
# -r  Percentage of reads that should have a single nucleotide extension in order to close a gap in a scaffold (0.7)
# -d  Maximum difference between the gapsize and the number of gapclosed nucleotides (50)
# -n  Minimum overlap required to merge adjacent sequences in a scaffold (10)
# -i  Number of iterations to fill the gaps (1)
#
# Bowtie Parameters:
# -g  Maximum number of allowed gaps during mapping with Bowtie (0) 
#   Corresponds to the -v option in Bowtie. *higher number of allowed gaps can lead to least accurate GapFiller*
#
# Additional Parameters:
# -T  Number of threads to run GapFiller (1)
# -b  Base name for your output files (standard_output)
