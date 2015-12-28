#!/bin/bash

rm -f out.txt
mbx vdm -o out.txt *.fa 
wc out.txt 
rm -f out.txt 

mbx vdm *.fa | wc
