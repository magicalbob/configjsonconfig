""" Python program to update json key value """

import sys
import tempfile
import os
import json
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-i", "--Input", help = "Input file", required = False)
parser.add_argument("-s", "--Section", help = "Section name", required = True)
parser.add_argument("-k", "--Key", help = "Key name", required = True)
parser.add_argument("-v", "--Value", help = "Key's value", required = True)

args = parser.parse_args()

if args.Input:
    try:
        in_file = open(args.Input,"r")
    except:
        # error opening input file, complain
        print("Unable to open input file given")
        exit(2)
else:
    in_file = sys.stdin

temp=tempfile.NamedTemporaryFile(mode='w')

j=json.load(in_file)

for k in j:
    if args.Section == k:
        for i in j[k]:
            if args.Key == i:
                j[k][i] = args.Value


outfile=[]

outfile.append('{')
first_section = " "
for k in j:
    outfile.append("%s  \"%s\": {" % (first_section,k))
    first_section=","
    first_comma=" "
    for i in j[k]:
        outfile.append("%s    \"%s\": \"%s\"" % (first_comma,i,j[k][i]))
        first_comma = ","
    outfile.append("  }")
outfile.append("}")

for l in outfile:
    temp.write(l)

temp.seek(0)

os.system("cat %s|jq ." % (temp.name))
