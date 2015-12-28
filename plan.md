+ exit -> sys.exit
+ mbx gen me -k Dir
+ Command: avoid name collision!
+ sql create for table formats

+ use mbx translation in run-glimmer script
+ template for commandline tests
+ database file converters (uniprot, NR)
+ etc/info command, guess type

+ what if abbr == name? in help text

+ timer!? for test/ tune preformance

------------

```
$ mbx guess sample.fa
fasta:nucl

$ mbx gu sample.fa
fasta:nucl

$ mbx gu --blastdb dbase.fa sample.fa
blastn

```


    istring = 'LMAKSKILKNTLVLYFRQVLIVLITLYSMRVVLNELGVDDFGIYSVVAGFVTLMMLAFLPGSMASAQQRFFTS'
    jstring = 'LMAKSKILKNTLVLYFRQVLIVLITLYSMRVVLNELGVDDFGIYSVVAGFVTLLAFLPGSMASATQRFFS'