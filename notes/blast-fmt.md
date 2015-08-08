
NCBI BLAST+ FORMATS
===================

#### Blast Formatter ####

`blast_formatter` need `-outfmt 11`

    $ echo 1786181 | blastn -db ecoli -outfmt 11 -out out.1786181.asn
    $ blast_formatter -archive out.1786181.asn -outfmt 7 > out.1786181.fmt7.bsn
    
#### Formats ####

From `blastp -help`:

     -outfmt <String>
       alignment view options:
         0 = pairwise,
         1 = query-anchored showing identities,
         2 = query-anchored no identities,
         3 = flat query-anchored, show identities,
         4 = flat query-anchored, no identities,
         5 = XML Blast output,
         6 = tabular,
         7 = tabular with comment lines,
         8 = Text ASN.1,
         9 = Binary ASN.1,
        10 = Comma-separated values,
        11 = BLAST archive format (ASN.1)
        12 = JSON Seqalign output
