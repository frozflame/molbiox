#!/usr/bin/env bash

# NTHREADS="6"
NTHREADS=`mbx-env cpu-count`

BLASTEXE="blastp"

# DBDIR="."
# DBDIR="/mnt/fx6300/hailong/Public/dbxbio"
DBDIR="$HOME/Public/dbxbio"

DATABASE="ncbi/nr"
# DATABASE="uniprot/uniprot_sprot.named.fasta"
# DATABASE="uniprot/wzx.named.fasta"
# DATABASE="uniprot/wzy.named.fasta"
# DATABASE="uniprot/wzxy.named.fasta"
# DATABASE="uniprot/oprm.named.fasta"
# DATABASE="vibrio/flanking.vibrio.fasta"

EVALUE="1e-5"


# ALLFIELDS="qseqid qgi qacc qaccver qlen sseqid sallseqid sgi sallgi sacc"
# ALLFIELDS="${ALLFIELDS} saccver sallacc slen qstart qend sstart send qseq"
# ALLFIELDS="${ALLFIELDS} sseq evalue bitscore score length pident nident"
# ALLFIELDS="${ALLFIELDS} mismatch positive gapopen gaps ppos frames qframe"
# ALLFIELDS="${ALLFIELDS} sframe btop staxids sscinames scomnames sblastnames "
# ALLFIELDS="${ALLFIELDS} sskingdoms stitle salltitles sstrand qcovs qcovhsp"



for QUERY in $@; do

    OUTNAME=${QUERY}.fmt11.${BLASTEXE}

    echo -n "${BLASTEXE} ${QUERY} ... "

    ${BLASTEXE}  -query ${QUERY}  -db ${DBDIR}/${DATABASE}  -outfmt 11 \
                 -out ${OUTNAME}  -num_threads ${NTHREADS}  -evalue ${EVALUE}

    # blast_formatter -archive ${OUTNAME} -outfmt 0 > ${QUERY}.fmt0.${BLASTEXE}
    blast_formatter -archive ${OUTNAME} -outfmt 6 > ${QUERY}.fmt6.${BLASTEXE}
    # blast_formatter -archive ${OUTNAME} -outfmt 7 > ${QUERY}.fmt7.${BLASTEXE}

    # blast_formatter -archive ${OUTNAME} -outfmt "6 ${ALLFIELDS}" > ${QUERY}.fmt6a.${BLASTEXE}
    # blast_formatter -archive ${OUTNAME} -outfmt "7 ${ALLFIELDS}" > ${QUERY}.fmt7a.${BLASTEXE}

    echo Done!

    # rm ${OUTNAME}

done


# The NCBI BLAST family of programs includes:
#
# blastp
#   compares an amino acid query sequence against a protein sequence database
#
# blastn
#   compares a nucleotide query sequence against a nucleotide sequence database
#
# blastx
#   compares a nucleotide query sequence translated in all reading frames
#   against a protein sequence database
#
# tblast
#   compares a protein query sequence against a nucleotide sequence database
#   dynamically translated in all reading frames
#
# tblastx (nucl vs nucl but frameshifts are punished deadly)
#   compares the six-frame translations of a nucleotide query sequence against
#   the six-frame translations of a nucleotide sequence database.
#
#   Please note that tblastx program cannot be used with the nr database on the
#   BLAST Web page.

