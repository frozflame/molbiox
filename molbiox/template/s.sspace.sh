#!/usr/bin/env bash

REF=$1
QR1=$2
QR2=$3

EXEC="perl /opt/sspace/SSPACE_Standard_v3.0.pl"

# number of threads
NTHR=`mbx-env cpu-count`
# NTHR="6"

# base name (default standard_output)
PREFIX=${REF%.*}.ss

rm -f .gapfiller.libs.txt
echo "lib1 bwa ${QR1} ${QR2} 450 0.35 FR" > .gapfiller.libs.txt

${EXEC} -s ${REF} -l .gapfiller.libs.txt -T ${NTHR} -b ${PREFIX} -d 500


# ... from README file in sspace (default values in parentheses)
#
# Required parameters:
# -l  Library file containing two paired read files with insert size, error and orientation (see Manual for more info)
#   Also possible to insert .tab files with pairing information
# -s  Fasta file containing contig sequences used for extension
#   Inserted paired reads are mapped to extended and non-extended contigs
#
# Extension parameters:
# -m  Minimum number of overlapping bases with the seed/contig during overhang consensus build up (32)
# -o  Minimum number of reads needed to call a base during an extension (20)
# -r  Minimum base ratio used to accept a overhang consensus base (0.9)
#
# Parameters below only considered for scaffolding and are all optional:
# -k  Minimum number of links (read pairs) to compute scaffold (5)
# -a  Maximum link ratio between two best contig pairs. higher values lead to least accurate scaffolding (0.70)
# -n  Minimum overlap required between contigs to merge adjacent contigs in a scaffold (15)
# -z  Minimum contig size used for scaffold. Filters out contigs below this size. (0, no filtering)
#
# Bowtie parameters;
# -g  Maximum number of allowed gaps during mapping with Bowtie. Corresponds to the -v option in Bowtie (0)
#
# Additional options;
# -T  Specify the number of threads to run SSPACE, used both for reading the input readfiles and mapping the reads against the contigs (1)
#   For reading in the files, multiple files are read-in simultaneously
#   With read-mapping, the readmapper is called multiple times with 1 million reads per calls
# -S  Skip the processing of the reads. Meaning that SSPACE was already run,
#   but user now wants to use different extension/scaffold parameters (-S 1=yes, -S 0=no; default 0)
# -x  Indicate whether to extend the contigs of -s using paired reads in -l (-x 1=extension, -x 0=no extension; default 0)
# -v  Runs the scaffolding process in verbose mode (-v 1=yes, -v 0=no; default 0)
# -b  Base name for your output files (standard_output)
# -p  Make .dot file for visualisation (-p 1=yes, -p 0=no; defualt 0)

