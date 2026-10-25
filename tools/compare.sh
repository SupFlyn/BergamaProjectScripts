#!/bin/bash
# compare.sh <runA> <runB>: same output and log files? (run folder name, mock ids and object addresses normalised)
# Lists each differing file; for text files the first differing lines are shown.
norm() { sed -e "s|$2|RUN|g" -e "s/id='[0-9]*'/id=X/g" -e "s/0x[0-9a-f]\{6,\}/0xX/g" "$1"; }
for d in $1 $2; do A=$(realpath $d); (cd $A/Downloads/Bergama && find output logs -type f | sort | while read f; do echo "$(norm "$f" $A | md5sum | cut -c1-12) $f"; done) > $A.hashes; done
A=$(realpath $1); B=$(realpath $2)
if diff -q $A.hashes $B.hashes >/dev/null; then echo "IDENTICAL ($(wc -l < $A.hashes) files)"; exit 0; fi
diff <(cut -c14- $A.hashes) <(cut -c14- $B.hashes) | grep '^[<>]' | sed 's/^</only in A:/; s/^>/only in B:/'
join -j 2 <(sort -k2 $A.hashes) <(sort -k2 $B.hashes) | awk '$2!=$3{print $1}' | while read f; do
  echo "DIFFERS: $f"
  case "$f" in *.json|*.txt) diff <(norm $A/Downloads/Bergama/$f $A) <(norm $B/Downloads/Bergama/$f $B) | head -6;; esac
done
exit 1
