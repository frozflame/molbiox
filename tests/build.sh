#!/bin/bash

cd ~/Cloud/Nutstore/devel/molbiox/molbiox/algor/align
gcc-5 -O -o alignlib.so -shared alignlib.c
