#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with cities infobox data, audit it, come up with a cleaning idea and then clean it up.
In the first exercise we want you to audit the datatypes that can be found in some particular fields in the dataset.
The possible types of values can be:
- 'None' if the value is a string "NULL" or an empty string ""
- 'list', if the value starts with "{"
- 'int', if the value can be cast to int
- 'float', if the value can be cast to float, but is not an int
   For example, '3.23e+07' should be considered a float because it can be cast
   as float but int('3.23e+07') will throw a ValueError
- 'str', for all other values

The audit_file function should return a dictionary containing fieldnames and a
SET of the types that can be found in the field. e.g.
{"field1: set([float, int, str]),
 "field2: set([str]),
  ....
}

All the data initially is a string, so you have to do some checks on the values first.

"""
#%%
import codecs
import csv
import json
import pprint

CITIES = 'cities.csv'

FIELDS = ["name", "timeZone_label", "utcOffset", "homepage", "governmentType_label", "isPartOf_label", "areaCode", "populationTotal",
          "elevation", "maximumElevation", "minimumElevation", "populationDensity", "wgs84_pos#lat", "wgs84_pos#long",
          "areaLand", "areaMetro", "areaUrban"]
#%%
def skip_lines(reader,skip):
    for i in range(skip):
        reader.next()
    return reader
#%%
def is_number_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
#%%
def is_number_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
#%%
def num_type(s):
    numtype = ''
    num = s
    numint = int(num)
    if num == numint:
        numtype = 'int'
    else:
        numtype = 'float'
    return numtype
#%%
def add_to_set(dictionary, key,value):
    if value in dictionary[key]:
        pass
    else:
        dictionary[key].add(value)
    return dictionary

#%%
def audit_file(filename, fields):
    fieldtypes = {}

    # YOUR CODE HERE
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        skip_lines(reader,3)
        i = 0
        for row in reader:
            i += 1
            if i == 1:
                for item in fields:
                    fieldtypes[item] = set()

            for item in fields:
                if (row[item] == "" or  row[item] == 'NULL'):
                    row[item] = None
                    fieldtypes = add_to_set(fieldtypes, item, type(None))#row[item])

                elif (str(row[item]).startswith('{')):
                    fieldtypes = add_to_set(fieldtypes, item, type([]))

                elif (is_number_float(str(row[item]))):#(isinstance(row[item], float)):
                    fieldtypes = add_to_set(fieldtypes, item, type(1.0))

                elif is_number_int(str(row[item])):
                    fieldtypes = add_to_set(fieldtypes, item, type(1))

                else:
                    fieldtypes = add_to_set(fieldtypes, item, type(None))

#    pprint.pprint(fieldtypes)

    return fieldtypes

#%%
def test():
    fieldtypes = audit_file(CITIES, FIELDS)

    pprint.pprint(fieldtypes)
    assert fieldtypes["areaLand"] == set([type(1.1), type([]), type(None)])
    assert fieldtypes['areaMetro'] == set([type(1.1), type(None)])
#%%
if __name__ == "__main__":
    test()
