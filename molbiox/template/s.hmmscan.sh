#!/usr/bin/env bash

# NTHREADS="6"
NTHREADS=`mbx-env cpu-count`

DBDIR="$HOME/Public/dbxbio"
# DBDIR="/mnt/fx6300/hailong/Public/dbxbio"

DATABASE="pfam/Pfam-A.hmm"
# DATABASE="pfam/Pfam-B.hmm"

# Prepare HMM file
# gunzip ${DATABASE}.gz
# hmmpress

# EVALUE="1e-5"

for QUERY in $@; do

    hmmscan --cpu ${NTHREADS} \
            --tblout ${QUERY}.hmmscan.tbl \
            ${DBDIR}/${DATABASE} \
            ${QUERY}

done
