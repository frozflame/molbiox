
Notes on `MCL`
=======

Install `MCL` on ubuntu

    sudo apt-get install mcl

Simple usage of `MCL`

    mcl input.abc --abc -o groups.out

`MCL` accept input file in `ABC` format, which looks like

    hat cat 0.3
    cat sat 0.9
    ....

-------

#### Important options ####

`-I`

`-I 5.0` will tend to result in fine-grained clusterings, and `-I 1.2` will tend to result in very coarse grained clusterings. 



-------

A few things to note. 

First, MCL will symmetrize any arrow it finds. If it sees

    bat cat 1.0 

it will act as if it also saw 

    cat bat 1.0

You can explicitly specify `cat bat 1.0`, mcl will in the first
parse stage simply end up with duplicate entries. 

Second, MCL deduplicates repeated edges by taking the one with the
**maximum** value. 


