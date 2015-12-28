#!/usr/bin/env bash
bin/decodeanhmm.Linux_x86_64 lib/TMHMM2.0.model -f lib/TMHMM2.0.options N2377.wzy.v2.fa.faa

ARCH=`uname -m`;
TDIR=/opt/tmhmm

DECODER=${TDIR}/bin/decodeanhmm.Linux_${ARCH}
MDLFILE=${TDIR}/lib/TMHMM2.0.model
OPTFILE=${TDIR}/lib/TMHMM2.0.options


for FILENAME in $@; do

    ${DECODER} ${MDLFILE} -f ${OPTFILE} -plp ${FILENAME} > ${FILENAME}.tmh

done
