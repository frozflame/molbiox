`io.fasta`
----------

#### Quick Start

Read a fasta file (output like `fastalength`)

    >>> from molbiox.io import fasta
    >>> for rec in fasta.read('sample.fa'):
    ...     print(len(rec.seq), rec.cmt)

Write to a fasta file

    >>> from molbiox.io import fasta
    >>> recs = [dict(cmt='rseq.1', seq='ATCG'),  dict(cmt='rseq.2', seq='TGCA')]
    >>> fasta.write('output.fa', recs)


