#!/bin/bash
# compare.sh <runA> <runB>: hash every output/log file, run folder name normalised
for d in $1 $2; do A=$(realpath $d); (cd $A/Downloads/Bergama && find output logs -type f | sort | while read f; do echo "$(sed "s|$A|RUN|g" "$f" | md5sum | cut -c1-12) $f"; done) > $A.hashes; done
diff $(realpath $1).hashes $(realpath $2).hashes && echo "IDENTICAL ($(wc -l < $(realpath $1).hashes) files)"
