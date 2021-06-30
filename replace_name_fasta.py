#!/usr/bin/env python
# grabbed from BrissMiller's answer at biostars: https://www.biostars.org/p/103089/#441715

# replace specific headers from a fa file using a custom made lookup table, tab delimited. 
# Use grep "^>" fasta.fa to help generate that lookup table.
# Code based off of solution from replace fasta headers with another name in a text file

#Example lookup table line
#>old_line  >new_linegrep

import argparse
import csv

parser=argparse.ArgumentParser(description="program that replaces fasta headers")
parser.add_argument("-i", help="input fasta", type=file)
parser.add_argument("-l", help="lookup table with replacement header lines")
parser.add_argument("-o", help="output fasta")
args = parser.parse_args()

# create an output file
newfasta=open(args.o,'w') 

# load lookup table into dict format
lookup_dict = {}
with open(args.l) as lookup_handle:                                                                                          
    lookup_list = csv.reader(lookup_handle, delimiter='\t')
    for entry in lookup_list:
        lookup_dict[entry[0]] = entry[1]

# read in the fa line by line and replace the header if it is in the lookup table
for line in args.i:
    line = line.rstrip("\n")
    if line.startswith('>'):
        if str(line) in lookup_dict.keys():
            newname = lookup_dict[line]
            newfasta.write(newname+"\n")
        else:
            newfasta.write(line+"\n")
    else: 
        newfasta.write(line+"\n")

