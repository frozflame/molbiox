#!/usr/bin/env bash


OPT_MAXHOURS="-maxhours 1"

for FILENAME in $@; do

    OUT_FAS="-fastaout ${FILENAME}.muscle.fas"
    OUT_CLW="-clwout   ${FILENAME}.muscle.clw"
    OUT_HTML="-htmlout ${FILENAME}.muscle.html"
    # OUT_PHYS="-physout ${FILENAME}.muslce.phys"
    # OUT_PHYI="-phyiout ${FILENAME}.muslce.phyi"
    # OUT_MSF="-msfout   ${FILENAME}.muscle.msf"

    muscle -in ${FILENAME} \
        ${OUT_FAS} ${OUT_CLW} ${OUT_HTML}  ${OUT_PHYS} ${OUT_PHYI} ${OUT_MSF} \
        ${OPT_MAXHOURS}


done