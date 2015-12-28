#!/bin/bash

TMPPATH="/tmp/.tmp-vpmr"
OUTNAME="vibrio.primers.P2-40.csv"
COLUMNS="serogroup, strain, pmrl, pmrr, pmri, posl, posr, posi, prod, cmt"
HEADERS="serogroup,strain,left-primer,right-primer,INTERNAL-oligo,left-pos,right-pos,INTERNAL-pos,product-length,comment"

SQL="select ${COLUMNS} from primers where batch = 'P2' order by serogroup"

rm -f ${TMPPATH} ${OUTNAME}
echo "copy (${SQL})to '${TMPPATH}' DELIMITER ',' CSV;" | psql microbe

echo ${HEADERS} > ${OUTNAME}
cat ${TMPPATH} >> ${OUTNAME}
rm -f ${TMPPATH}

read -p "Open it? " ans
case ${ans} in
    [Yy]*)  open ${OUTNAME} -a 'Microsoft Excel';;
    *)      exit;;
esac

# tip:
