#!/usr/bin/env bash


set -o nounset  # same as 'set -u'
set -o errexit  # same as 'set -e'

# someone will use spaces in filenames or commandline arguments
cat "$filename"

foo() { for i in $@; do printf "%s\n" "$i"; done };
foo bar "baz quux"
# bar
# baz
# quux

foo() { for i in "$@"; do printf "%s\n" "$i"; done };
foo bar "baz quux"
# bar
# baz quux



${#var}     # string length
