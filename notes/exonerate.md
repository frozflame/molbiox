
Notes on `exonerate`
=======

`exonerate` is a suite for investigating DNA 
and RNA sequence similarities

    $ fasta* --help # for more information
    $ man fastalength  # for a list


尚不了解的：
fastasoftmask
fastahardmask
fastaclip


-------

Get reverse complement 

    $ fastarevcomp sample.seq > sampleRC.seq 

-------

Get lengths of each sequence

    $ fastalength 454AllContigs.fna

--------

Split a multi-seq fasta-file into multiple single-seq fasta-files

    $ fastaexplode 454AllContigs.fna

-------

Get positions of each `>` character

    $ fastaindex sample.seq sample.index

`sample.index` must be a non-existing file

--------

Sort sequences in a fasta-file

    $ fastasort -k len -r true sample.seq

    `-k`: id/len/seq (key, default: id)
    `-r`: true/false (reverse, default: false)

-------

Slice (get subseq of) a single-seq fasta-file

    $ fastasubseq sample.seq 0 100 > sample_0-100.seq

Synopsis:
    $ fastasubseq FILENAME START LENGTH

Note:
    * Zero-base index 
    * If multi-seq is given, only the first seq is considered


--------

Replace all ambiguous bases with N  
把所有模糊碱基换成N

    $ fastaclean -a true sample.seq > sample.clean

-------

Split a fasta-file into 10 pieces, preserving integrity of each seq  
将一个序列文件分割成10块，每块上都是完整的一条或若干条序列

    $ fastasplit -c 10 sample.seq sample.chunks

`sample.chunks` is an existing directory  
`sample.chunks` 是一个已经存在的文件夹  

-------

Translate DNA sequence into peptide sequence  
将DNA序列翻译成氨基酸序列

    $ fastatranslate -F 1 sample.seq > sample.pep
    `-F`: 0/1/2/3 (frame, default: 0 for all frames)

An alternative utility
    
    $ transeq sample.seq sample.pep

------

Count occurrence of each letter:

    $ fastacomposition sample.seq

-------
