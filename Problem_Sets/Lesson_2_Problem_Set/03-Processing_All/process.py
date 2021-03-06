#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Let's assume that you combined the code from the previous 2 exercises
# with code from the lesson on how to build requests, and downloaded all the data locally.
# The files are in a directory "data", named after the carrier and airport:
# "{}-{}.html".format(carrier, airport), for example "FL-ATL.html".
# The table with flight info has a table class="dataTDRight".
# There are couple of helper functions to deal with the data files.
# Please do not change them for grading purposes.
# All your changes should be in the 'process_file' function

from bs4 import BeautifulSoup
from zipfile import ZipFile
import os

datadir = "data"

def open_zip(datadir):
    with ZipFile('{0}.zip'.format(datadir), 'r') as myzip:
        myzip.extractall()


def process_all(datadir):
    files = os.listdir(datadir)
#    print "files == ", files
    return files


def process_file(f):
    # This is example of the datastructure you should return
    # Each item in the list should be a dictionary containing all the relevant data
    # Note - year, month, and the flight data should be integers
    # You should skip the rows that contain the TOTAL data for a year
    # data = [{"courier": "FL",
    #         "airport": "ATL",
    #         "year": 2012,
    #         "month": 12,
    #         "flights": {"domestic": 100,
    #                     "international": 100}
    #         },
    #         {"courier": "..."}
    # ]
    data = []
    info = {}
    tempdata = {"courier": None,
             "airport": None,
             "year": None,
             "month": None,
             "flights": {"domestic": None,
                         "international": None}}

    info["courier"], info["airport"] = f[:6].split("-")

    with open("{}/{}".format(datadir, f), "r") as html:

        soup = BeautifulSoup(html)
        g_data = soup.find_all(id='DataGrid1')
        print 'gdata = ', len(g_data)

        for item in g_data:
            g = item.find("tr",{'class':"dataTDRight"})
            print 'g = ', g

            tempdata["courier"] = str(info["courier"])
            tempdata["airport"] = info["airport"]
            tempdata["year"] = g.td.text
            tempdata["month"] = g.td.next_sibling.text
            tempdata["flights"]["domestic"] = g.td.next_sibling.next_sibling.text
            tempdata["flights"]["international"] = g.td.next_sibling.next_sibling.next_sibling.text

            data.append(tempdata)

        print "data = ", data
        return data


def test():
#    print "Running a simple test..."
    open_zip(datadir)
    files = process_all(datadir)
    data = []
    for f in files:
        data += process_file(f)
#    assert len(data) == 3
#    for entry in data[:3]:
#        assert type(entry["year"]) == int
#        assert type(entry["flights"]["domestic"]) == int
#        assert len(entry["airport"]) == 3
#        assert len(entry["courier"]) == 2
#    print "... success!"

if __name__ == "__main__":
    test()