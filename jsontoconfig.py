""" Python program to convert json to config/ini """

import sys
import tempfile
import os
import json
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-i", "--Input", help = "Input file", required = False)

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

j=json.load(in_file)

for k in j:
    print("[%s]" % (k))
    for i in j[k]:
        print("%s = %s" % (i,j[k][i]))
