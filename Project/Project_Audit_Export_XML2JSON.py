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

# Clean the street data from the key : value pair in the mapping dictionary
mappingstreet = {'Ave': 'Avenue',
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

# Clean the city data from the key : value pair in the mapping dictionary
mappingcity = {'Ajax, Ontario': 'Ajax',
               'caledon': 'Caledon',
               'City of Brampton': 'Brampton',
               'City of Burlington': 'Burlington',
               'City of Hamilton': 'Hamilton',
               'City of Kawartha Lakes': 'Kawartha Lakes',
               'City of Oshawa': 'Oshawa',
               'City of Pickering': 'Pickering',
               'City of St. Catharines': 'St. Catharines',
               'City of Toronto': 'Toronto',
               'City of Vaughan': 'Vaughan',
               'Etobicoke, Toronto': 'Etobicoke',
               'Missisauga': 'Mississauga',
               'King': 'King City',
               'Municipality of Clarington': 'Clarington',
               'markham': 'Markham',
               'toronto': 'Toronto',
               'vaughan': 'Vaughan',
               'Town of Ajax': 'Ajax',
               'Town of Aurora': 'Aurora',
               'Town of Bradford West Gwillimbury': 'Bradford West Gwillimbury',
               'Town of Caledon': 'Caledon',
               'Town of East Gwillimbury': 'East Gwillimbury',
               'Town of Erin': 'Erin',
               'Town of Grimsby': 'Grimsby',
               'Town of Halton Hills': 'Halton Hills',
               'Town of Innisfil': 'Innisfil',
               'Town of Markham': 'Markham',
               'Town of Milton': 'Milton',
               'Town of Mono': 'Mono',
               'Town of New Tecumseth': 'New Tecumseth',
               'Town of Newmarket': 'Newmarket',
               'Town of Niagara-On-The-Lake': 'Niagara-on-the-lake',
               'Town of Whitby': 'Whitby',
               'Town of Whitchurch-Stouffville': 'Whitchurch-Stouffville',
               'Township of Adjala-Tosorontio': 'Adjala-Tosorontio',
               'Township of Amaranth': 'Amaranth',
               'Township of East Garafraxa': 'East Garafraxa',
               'Township of Essa': 'Essa',
               'Township of Guelph/Eramosa': 'Guelph/Eramosa',
               'Township of King': 'King City',
               'Township of Mulmur': 'Mulmur',
               'Township of Puslinch': 'Puslinch',
               'Township of Scugog': 'Scugog',
               'Township of Uxbridge': 'Uxbridge'
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
    return node


# Function to audit the street name from abbreviations at the end to the full name
# ex. Charles St. ==> Charles Street
def update_street(node, name):
    m = street_type_post.search(name)
    if m:
        mm = m.group()
        if mm in mappingstreet.keys():
            node['address']['street'] = re.sub(mm, mappingstreet[mm], name)
            print mm, ' ==> ', node['address']['street']
    return node


# Function to audit the street name from abbreviations at the end to the full name
# ex. Charles St. ==> Charles Street
def update_city(node, name):
    if name in mappingcity.keys():
        node['address']['city'] = re.sub(name, mappingcity[name], name)
        print name, ' ==> ', node['address']['city']
    return node


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

            for tag in element.iter("tag"):
                # Audit the street name
                if tag.attrib['k'] == "addr:street":
                    name = tag.attrib['v']
                    node = update_street(node, name)

                # Audit the city name
                if tag.attrib['k'] == "addr:city":
                    name = tag.attrib['v']
                    node = update_city(node, name)

                    # Audit the postcode in the format 'M4Y 1R5'
                if tag.attrib['k'] == "addr:postcode":
                    postcode = tag.attrib['v']
                    node = update_postcode(node, postcode)
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
