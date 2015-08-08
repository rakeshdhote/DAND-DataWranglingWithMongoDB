import os
import pprint
import csv

DATADIR = ""
DATAFILE = "beatles-diskography.csv"

def parse_csv(datafile):
    data = [] 
    with open(datafile, "rb") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

if __name__ == '__main__':
    datafile = os.path.join(DATADIR, DATAFILE)
    parse_csv(datafile)
    d = parse_csv(datafile)
    pprint.pprint(d)
    