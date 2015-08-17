#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
import time

# OSMFILE = "example.osm"
OSMFILE = "toronto_canada.osm"

# Regex queries
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
starts_with = re.compile(r'^addr:')
ends_with = re.compile(r'\w+$')

street_type_post = re.compile(r'\b\S+\.?$', re.IGNORECASE)
street_type_pre = re.compile(r'^\b\S\.?', re.IGNORECASE)

postcode_pre = re.compile(r'^...')
postcode_post = re.compile(r'...$')
postcode_first = re.compile(r'^[^,]*')

# fields required in the node['address'] dictionary
CREATED = ["version", "changeset", "timestamp", "user", "uid"]

# Clean the data from the key : value pair in the mapping dictionary
mapping = {'Ave': 'Avenue',
           'Ave.': 'Avenue',
           'Alliston': '',
           'Amaranth': '',
           'Avens': 'Avens Boulevard',
           'Blvd': 'Boulevard',
           'Blvd.': 'Boulevard',
           'Boulevade': 'Boulevard',
           'Cir': 'Circle',
           'Crct': 'Crescent',
           'Cresent': 'Crescent',
           'Cressent': 'Crescent',
           'Crt.': 'Circuit',
           'Dr': 'Drive',
           'Dr.': 'Drive',
           'E': 'East',
           'E.': 'East',
           'Grv': 'Grove',
           'Ldg': 'Landing',
           'Hrbr': 'Harbour Way',
           'Manors': 'Manor',
           'N': 'North',
           'Puschlinch': 'Puslinch',
           'Rd': 'Road',
           'Rd.': 'Road',
           'S': 'South',
           'S.': 'South',
           'St': 'Street',
           'St.': 'Street',
           'Terace': 'Terrace',
           'Terraces': 'Terrace',
           'Trl': 'Trail',
           'W': 'West',
           'W.': 'West',
           'avenue': 'Avenue'
           }


# Function to audit the postcode in a format 'M4Y 1R5'
# If there are more than one postcode, the first one will be selected
def update_postcode(node, postcode):
    postcode1 = postcode_first.search(postcode).group()
    if len(postcode1) != 7:
        postcode2 = postcode_pre.search(postcode1).group() + ' ' + postcode_post.search(postcode1).group()
        node['address']['postcode'] = postcode2.upper()
    else:
        node['address']['postcode'] = postcode1.upper()


# Function to audit the street name from abbreviations at the end to the full name
# ex. Charles St. ==> Charles Street
def update_address(node, name):
    st_type = street_type_post.search(name)
    if st_type:
        mm = st_type.group()
        if mm in mapping.keys():
            node['address']['street'] = re.sub(mm, mapping[mm], name)


# Function to create a JSON file from the xml document
def shape_element(element):
    node = {'created': {}}

    if element.tag == "node" or element.tag == "way":
        # YOUR CODE HERE
        if element.tag == "node":
            node['type'] = 'node'

        if element.tag == "way":
            node['type'] = 'way'

        for tag in element.iter("tag"):
            if re.search(lower_colon, tag.attrib['k']):
                node['address'] = {}
                continue

        if ('lon' or 'lat') in element.attrib.keys():
            node['pos'] = [None, None]

        for tag in element.iter("tag"):
            attribute = tag.attrib['k']
            if re.search(problemchars, attribute):
                pass
            elif re.search(lower_colon, attribute):
                if re.search(starts_with, attribute):
                    node['address'][re.search(ends_with, attribute).group()] = tag.attrib['v']
                else:
                    node[attribute] = tag.attrib['v']

        for item in element.attrib.keys():
            if element.tag == "way":
                node['node_refs'] = []
                for tag in element.iter("nd"):
                    node['node_refs'].append(tag.attrib['ref'])

            if item in CREATED:
                node['created'][item] = element.attrib[item]
            elif item == 'lat':
                node['pos'][0] = float(element.attrib[item])
            elif item == 'lon':
                node['pos'][1] = float(element.attrib[item])
            else:
                node[item] = element.attrib[item]

        if 'address' in node.keys():
            # Audit the street name
            for tag in element.iter("tag"):
                if tag.attrib['k'] == "addr:street":
                    name = tag.attrib['v']
                    update_address(node, name)

                    # Audit the postcode in format 'M4Y 1R5'
                if tag.attrib['k'] == "addr:postcode":
                    postcode = tag.attrib['v']
                    update_postcode(node, postcode)
        else:
            pass

        return node
    else:
        return None


# Dump the xml file to the JSON file
def process_map(file_in, pretty=False):
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        fo.write('[')
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2) + "\n")
                else:
                    fo.write(json.dumps(el) + ",\n")
        fo.write(']')
    return data


if __name__ == "__main__":
    # NOTE: if you are running this code on your computer, with a larger dataset,
    # call the process_map procedure with pretty=False. The pretty=True option adds
    # additional spaces to the output, making it significantly larger.

    start = time.clock()
    data = process_map(OSMFILE, False)
    end = time.clock()
    print 'Time spent (s) : ', (end - start)

