#!/usr/bin/env bash

REF=$1
QR1=$2
QR2=$3

# NTHREADS="6"
NTHREADS=`mbx-env cpu-count`
TMPDIR="${REF%.*}.bwa.dir"

MISMATCH=0.04


rm -rf  ${TMPDIR}
mkdir   ${TMPDIR}
cd      ${TMPDIR}

ln -s ../${REF} ref.fa
ln -s ../${QR1} query.1.fq
ln -s ../${QR2} query.2.fq


error_message () {
   echo 'Error!'; exit 1
}

run_bwa_se (){

    set -e; echo '# ^_^ bwa-se start ... '

    bwa index ref.fa
    bwa aln -n ${MISMATCH} -t ${NTHREADS} ref.fa query.1.fq > aln.1.sai
    bwa samse ref.fa aln.1.sai query.1.fq > aln.sam

    set +e; echo '# ^_^ bwa-se done!'

}

run_bwa_pe (){

    set -e; echo '# ^_^ bwa-pe start ... '

    bwa index ref.fa
    bwa aln -n ${MISMATCH} -t ${NTHREADS} ref.fa query.1.fq > aln.1.sai
    bwa aln -n ${MISMATCH} -t ${NTHREADS} ref.fa query.2.fq > aln.2.sai
    bwa sampe ref.fa aln.{1,2}.sai query.{1,2}.fq > aln.sam

    set +e; echo '# ^_^ bwa-pe done!'

}


if [ "a.${QR2}" == "a." ]; then
    run_bwa_se
else
    run_bwa_pe
fi



echo "# ^_^ samtools start ... "

    samtools faidx ref.fa \
        >> samtools.out.log 2>> samtools.err.log \
        || error_message

    samtools import ref.fa.fai aln.sam aln.bam \
        >> samtools.out.log 2>> samtools.err.log \
        || error_message

    samtools sort aln.bam aln.sorted \
        >> samtools.out.log 2>> samtools.err.log \
        || error_message

    samtools index aln.sorted.bam \
        >> samtools.out.log 2>> samtools.err.log \
        || error_message

echo "# ^_^ samtools done!"

# avoid accidental write
chmod -w aln.sorted.bam

# remove the bulky .sam
rm aln.sam

cd ..
