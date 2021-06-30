#!/bin/bash
set -e
if [ -z ${var+x} ]; then echo "error: specify input fasta" & exit 1 ; fi

# 01 grab number of lines
file=$1
grep ">" $file | perl -pe "s/\>//" > ${file}.col1
# 02 grab num elements, parse that info
numevents=`wc -l ${file}.col1 | cut -d ' ' -f1`
numdigits=`echo "${#numevents}"`
# 03 grab species name code
speciesnames=${1##*/}
speciesnames=${speciesnames%.fa}
echo "Dataset $1 has $numevents sequences."
# 04 awk generate dictionary
awk -v var1=$speciesnames -v var2=$numdigits 'BEGIN {S=var1} {D=var2} {OFS="\t"} { print $0, ">"S"_"} {printf "%05d\n",NR }' ${file}.col1 | paste - - | perl -pe "s/_\t/_/" | perl -pe "s/^/\>/" > ${speciesnames}_dictionary.dct
echo "Dictionary of dataset $1 has been created."
# 05 call python script for replacement
echo "Replacing sequence names..."
python ./replace_name_fasta.py -i $1 -l ${speciesnames}_dictionary.dct -o ${speciesnames}_ok.fa
echo "Done. Sequence names changed  according to dictionary ${specienasmes}_dictionary.dct."
echo "Sequences have been deposited in ${speciesnames}_ok.fa"
