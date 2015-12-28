#!/usr/bin/env bash

# format specifiers
FMTS_MINI=`mbx-etc blast-mini`
FMTS_FULL=`mbx-etc blast-full`

OPT=''
# OPT='-max_target_seqs 1'

for NAME in $@; do

    echo -n "blast_formatter for ${NAME} ... "

    FMTR="blast_formatter ${OPT} -archive ${NAME}"

    NAME=${NAME//.fmt11./.}

    # ${FMTR} -outfmt 0 ${OPT} > ${NAME}.fmt0
    # ${FMTR} -outfmt 6 ${OPT} > ${NAME}.fmt6
    # ${FMTR} -outfmt 7 ${OPT} > ${NAME}.fmt7

    ${FMTR} -outfmt "6 ${FMTS_MINI}" > ${NAME}.fmt6m
    ${FMTR} -outfmt "7 ${FMTS_MINI}" > ${NAME}.fmt7m

    # ${FMTR} -outfmt "6 ${FMTS_FULL}" > ${NAME}.fmt6a
    # ${FMTR} -outfmt "7 ${FMTS_FULL}" > ${NAME}.fmt7a

    echo Done!

done


#   Taken from `blastp -help`
#
#   alignment view options:
#
#     0 = pairwise,
#     1 = query-anchored showing identities,
#     2 = query-anchored no identities,
#     3 = flat query-anchored, show identities,
#     4 = flat query-anchored, no identities,
#     5 = XML Blast output,
#     6 = tabular,                          -- customizable
#     7 = tabular with comment lines,       -- customizable
#     8 = Text ASN.1,
#     9 = Binary ASN.1,
#    10 = Comma-separated values,           -- customizable
#    11 = BLAST archive format (ASN.1)
#    12 = JSON Seqalign output
#
#    Options 6, 7, and 10 can be additionally configured to produce
#    a custom format specified by space delimited format specifiers.
#    The supported format specifiers are:
#
#    	    qseqid means Query Seq-id
#    	       qgi means Query GI
#    	      qacc means Query accesion
#    	   qaccver means Query accesion.version
#    	      qlen means Query sequence length
#    	    sseqid means Subject Seq-id
#    	 sallseqid means All subject Seq-id(s), separated by a ';'
#    	       sgi means Subject GI
#    	    sallgi means All subject GIs
#    	      sacc means Subject accession
#    	   saccver means Subject accession.version
#    	   sallacc means All subject accessions
#    	      slen means Subject sequence length
#    	    qstart means Start of alignment in query
#    	      qend means End of alignment in query
#    	    sstart means Start of alignment in subject
#    	      send means End of alignment in subject
#    	      qseq means Aligned part of query sequence
#    	      sseq means Aligned part of subject sequence
#    	    evalue means Expect value
#    	  bitscore means Bit score
#    	     score means Raw score
#    	    length means Alignment length
#    	    pident means Percentage of identical matches
#    	    nident means Number of identical matches
#    	  mismatch means Number of mismatches
#    	  positive means Number of positive-scoring matches
#    	   gapopen means Number of gap openings
#    	      gaps means Total number of gaps
#    	      ppos means Percentage of positive-scoring matches
#    	    frames means Query and subject frames separated by a '/'
#    	    qframe means Query frame
#    	    sframe means Subject frame
#    	      btop means Blast traceback operations (BTOP)
#    	   staxids means unique Subject Taxonomy ID(s), separated by a ';' (in numerical order)
#    	 sscinames means unique Subject Scientific Name(s), separated by a ';'
#    	 scomnames means unique Subject Common Name(s), separated by a ';'
#    	sblastnames means unique Subject Blast Name(s), separated by a ';' (in alphabetical order)
#    	sskingdoms means unique Subject Super Kingdom(s), separated by a ';' (in alphabetical order)
#    	    stitle means Subject Title
#    	salltitles means All Subject Title(s), separated by a '<>'
#    	   sstrand means Subject Strand
#    	     qcovs means Query Coverage Per Subject
#    	   qcovhsp means Query Coverage Per HSP
#
#    When not provided, the default value is:
#    'qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore'

