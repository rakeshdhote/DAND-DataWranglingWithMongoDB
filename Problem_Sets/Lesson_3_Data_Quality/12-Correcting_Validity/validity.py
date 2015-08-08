"""
Your task is to check the "productionStartYear" of the DBPedia autos datafile for valid values.
The following things should be done:
- check if the field "productionStartYear" contains a year
- check if the year is in range 1886-2014
- convert the value of the field to be just a year (not full datetime)
- the rest of the fields and values should stay the same
- if the value of the field is a valid year in range, as described above,
  write that line to the output_good file
- if the value of the field is not a valid year,
  write that line to the output_bad file
- discard rows (neither write to good nor bad) if the URI is not from dbpedia.org
- you should use the provided way of reading and writing data (DictReader and DictWriter)
  They will take care of dealing with the header.

You can write helper functions for checking the data and writing the files, but we will call only the
'process_file' with 3 arguments (inputfile, output_good, output_bad).
"""
import csv
import pprint
import datetime
import re

INPUT_FILE = 'autos.csv'
OUTPUT_GOOD = 'autos-valid.csv'
OUTPUT_BAD = 'FIXME-autos.csv'

def process_file(input_file, output_good, output_bad):

    with open(input_file, "r") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames

        #COMPLETE THIS FUNCTION
        data = []
        invalid = []
        valid = []
        pattern1 = ".*dbpedia.*"    #"?<!(http://dbpedia.org.*)"
        #"^http://dbpedia.org.*" (?!/http://dbpedia.org)
        pattern2 = "\D"

        for row in reader:
            data.append(row)

        ndata = len(data)

        for i in range(ndata):

            if re.match(pattern1, data[i]['URI']):
                if re.match(pattern2, data[i]['productionStartYear']):
                    invalid.append(data[i])
                else:
                    temp = data[i]['productionStartYear'][:19]
                    data[i]['productionStartYear'] = \
                    datetime.datetime.strptime(temp, "%Y-%m-%dT%H:%M:%S").year

                    if data[i]['productionStartYear'] >= 1886 and \
                    data[i]['productionStartYear'] <= 2014:
                        valid.append(data[i])
                    else:
                        invalid.append(data[i])

        writefile(output_good,header,valid)
        writefile(output_bad,header,invalid)


def writefile(file,header,data):
    with open(file, "w") as g:
        writer = csv.DictWriter(g, delimiter=",", fieldnames= header, lineterminator='\n')
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def test():

    process_file(INPUT_FILE, OUTPUT_GOOD, OUTPUT_BAD)


if __name__ == "__main__":
    test()