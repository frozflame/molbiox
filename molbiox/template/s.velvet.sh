#!/usr/bin/env bash

FQ1=$1
FQ2=$2

if [ a.$3 == a. ]; then DIR="velvet.run.dir"; else DIR=$3; fi

set -e

DTRIM=/opt/sequencing/DynamicTrim.pl
LSORT=/opt/sequencing/LengthSort.pl
MERGE=/opt/sequencing/PairMerge.pl

assert_avail() {
    if which $1 > /dev/null;  then true; else
        >&2 echo "$1 not found. exit."; exit 1; fi
}

assert_exist() {
    if [ ! -f $1 ]; then
        >&2 echo "$1 not found. exit."; exit 1; fi
}

# test availability of essential programs
assert_avail velvetg
assert_avail velveth

assert_exist ${DTRIM}
assert_exist ${LSORT}
assert_exist ${MERGE}

# use pigz if available otherwise gzip
if which pigz; then GZIP=pigz; else GZIP=gzip; fi


NTHR=`mbx-env cpu-count`
# NTHR="6"

rm -rf ${DIR}
mkdir  ${DIR}

# unzip if FQ? are gzipped otherwise symlink
case ${FQ1} in
    *.gz)   ${GZIP} -dc ${FQ1} > ${DIR}/r1.fq;;
    *)      ln -s ${DIR}/r1.fq ${FQ1};;
esac
case ${FQ2} in
    *.gz)   ${GZIP} -dc ${FQ2} > ${DIR}/r2.fq;;
    *)      ln -s ${DIR}/r2.fq ${FQ2};;
esac

# work in $DIR afterwards
cd ${DIR}

${DTRIM} r1.fq
${DTRIM} r2.fq
${LSORT} *.trimmed
${MERGE} *.paired?  rxm.fq

# velveth hv29 29 -fastq -shortPaired final.fq
# velvetg hv29 -cov_cutoff 18
velvetoptimiser -s 25 -e 31 -x 2 -t ${NTHR} \
    -f '-fastq -shortPaired rxm.fq' \
    -o '-ins_length 400 -scaffolding yes'

cd ..


# velvetoptimiser
#   -s  start
#   -e  end
#   -x  step
#   -t  number of threads
#   -f  velveth options (input files)
#   -o  velvetg options (output files)
