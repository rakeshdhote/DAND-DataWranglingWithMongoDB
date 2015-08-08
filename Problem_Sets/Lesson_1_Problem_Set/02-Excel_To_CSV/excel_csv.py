# -*- coding: utf-8 -*-
# Find the time and value of max load for each of the regions
# COAST, EAST, FAR_WEST, NORTH, NORTH_C, SOUTHERN, SOUTH_C, WEST 1-8
# and write the result out in a csv file, using pipe character | as the delimiter.
# An example output can be seen in the "example.csv" file.

import xlrd
import os
import csv
import numpy as np

from zipfile import ZipFile

datafile = "2013_ERCOT_Hourly_Load_Data.xls"
outfile = "2013_Max_Loads.csv"


def open_zip(datafile):
    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
        myzip.extractall()


def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    data = []
    cv = []
    names = []

    # YOUR CODE HERE
    # Remember that you can use xlrd.xldate_as_tuple(sometime, 0) to convert
    # Excel date to Python tuple of (year, month, day, hour, minute, second)

    names = [sheet.cell_value(0, i) for i in range(1,9)]
    data.append(['Station','Year','Month','Day','Hour','Max Load'])
    for i in range(1,9):
        cv = sheet.col_values(i, start_rowx=1, end_rowx=None)
        maxvalue = np.max(cv)
        maxindex = cv.index(maxvalue)+1
        maxtime = sheet.cell_value(maxindex, 0)
        tt = xlrd.xldate_as_tuple(maxtime, 0)
        data.append( [names[i-1],tt[0],tt[1],tt[2],tt[3],maxvalue ])
    return data

def save_file(data, outfile):
    # YOUR CODE HERE
    with open(outfile, "wb") as csv_file:
        writer = csv.writer(csv_file, delimiter='|')
        for line in data:
            writer.writerow(line)

def test():
#    open_zip(datafile)
    data = parse_file(datafile)
    save_file(data, outfile)

    ans = {'FAR_WEST': {'Max Load': "2281.2722140000024", 'Year': "2013", "Month": "6", "Day": "26", "Hour": "17"}}

    fields = ["Year", "Month", "Day", "Hour", "Max Load"]
    with open(outfile) as of:
        csvfile = csv.DictReader(of, delimiter="|")
        for line in csvfile:
            s = line["Station"]
            if s == 'FAR_WEST':
                for field in fields:
                    assert ans[s][field] == line[field]

    print "Done"                


test()