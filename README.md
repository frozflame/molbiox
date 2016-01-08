molbiox
=======

Utilities for bioinformatics

Experimental stage. Very unstable yet.
Versions before 1.0.0 will be experimental and not ready for use.

Install from PyPI

    mkdir try-molbiox && cd try-molbiox
    virtualenv venv
    source venv/bin/activate
    pip install molbiox --upgrade


Install from GitHub

    mkdir try-molbiox && cd try-molbiox 
    virtualenv venv   
    source venv/bin/activate
    pip install https://github.com/frozflame/molbiox/archive/master.zip
   

Generate random sequences

    $ mbx rs
    $ mbx rs -h
    $ mbx rs -l 900 -o randseq.fa

Generate reverse complement of `randseq.fa`

    $ mbx rc randseq.fa -o randseq.rc.fa

Translate DNA to protein

    $ mbx tl randseq.fa -o randseq.faa

Read a fasta file (output like `fastalength`)

    >>> from molbiox.io import fasta
    >>> for rec in fasta.read('sample.fa'):
    ...     print(len(rec.seq), rec.cmt)



