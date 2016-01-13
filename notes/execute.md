
execute
-------

General form of commandline interfaces

    $ mbx CMD INPUT1 INPUT2 ... -o OUTPUT OTHER_OPTIONS

Each mbx command has 2 equivolent `CMD`: an abbrievation and a full-name. For example

    $ mbx rs -l 900 -o randseq.fa
    $ mbx random-seq -l 900 -o randseq.fa

are exactly the same. The abbrievation form is more convinient to type when used at
shell prompt, while the full-name form is encouraged when writting shell scripts because
it is more easily understood by people who nerver used _molbiox_.


