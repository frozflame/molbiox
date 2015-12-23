#!/usr/bin/env bash

for name in $@; do

    echo `fastalength $name | wc -l` $name

done
