#!/usr/bin/env bash

G3I="g3-iterated.csh"

EXTRACT="/usr/local/Cellar/glimmer3/3.02b/libexec/multi-extract"
# EXTRACT="/usr/bin/tigr-glimmer multi-extract"

predfile () {

    if [ -e $1.predict ]; then
        echo $1.predict
    else
        echo $1.run1.predict
    fi

}


for name in $@; do

    mkdir -p ${name}.dir

    cd ${name}.dir

    ln -s ../${name} && echo "ini ${name}"

    ${G3I} ${name} ${name} > g3i.log 2>&1

    mbx-tab-g3mcoordz `predfile ${name}` ${name}.mcoordz

    ${EXTRACT} ${name} ${name}.mcoordz > ${name}.ffa

    # fastatranslate -F 1 ${name}.ffa | sed -e 's:\[translate\(1\)\]::' > ${name}.faa
    mbx-seq-translate ${name}.ffa > ${name}.faa

    cd .. && echo "fin ${name}"

done
