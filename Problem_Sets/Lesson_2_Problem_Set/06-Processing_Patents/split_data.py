#!/usr/bin/env python
# -*- coding: utf-8 -*-
# So, the problem is that the gigantic file is actually not a valid XML, because
# it has several root elements, and XML declarations.
# It is, a matter of fact, a collection of a lot of concatenated XML documents.
# So, one solution would be to split the file into separate documents,
# so that you can process the resulting files as valid XML documents.

import xml.etree.ElementTree as ET
import re

PATENTS = 'patent.data'

def get_root(fname):
    tree = ET.parse(fname)
    return tree.getroot()


def split_file(filename):
    # we want you to split the input file into separate files
    # each containing a single patent.
    # As a hint - each patent declaration starts with the same line that was causing the error
    # The new files should be saved with filename in the following format:
    # "{}-{}".format(filename, n) where n is a counter, starting from 0.

    phrase = ".*xml version=.*"
    lines = []

    with open(filename, 'rb') as f:
        # read the file first
        reader = f.readlines()
        print "reader :", reader[2]

        #loop through each line
        for line_i in range(len(reader)):
#        for line_i, line in enumerate(reader, 1)
            line = reader[line_i]

            # check if we have a regex match with "phrase" variable
            # if so, write it the output file
            if re.match(phrase, line):
                lines.append(str(line_i+1))
        lines.append(str(len(reader)+1))
        lines[0] = 0
#        print "lines = ", lines

        for i in range(len(lines)-1):
            fo = open("{}-{}".format(filename, i), "wb")
            if i == 0:
                fo.writelines("%s" % reader[j] for j in \
                range( int(lines[i]), int(lines[i+1])-1 ))
            else:
                fo.writelines("%s" % reader[j] for j in \
                range( int(lines[i])-1, int(lines[i+1])-1 ))
            fo.close()

    pass


def test():
    split_file(PATENTS)
    for n in range(4):
        try:
            fname = "{}-{}".format(PATENTS, n)
            f = open(fname, "r")
            if not f.readline().startswith("<?xml"):
                print "You have not split the file {} in the correct boundary!".format(fname)
            f.close()
        except:
            print "Could not find file {}. Check if the filename is correct!".format(fname)


test()