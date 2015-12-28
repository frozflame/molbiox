#!/bin/bash

CMDLINE='mbx sl dummy.fa --list dummy.list'


echo
echo    '~~~~~~~~~~ Molbiox commandline test ~~~~~~~~~~'
echo    DIRECTORY: `basename $PWD`
echo
echo    FILES:
ls
echo

echo    'dummy.list:'
cat     'dummy.list'
echo
echo

echo    COMMAND LINE:
echo    '$' $CMDLINE
echo
echo    OUTPUT:
echo    $CMDLINE | sh
echo


