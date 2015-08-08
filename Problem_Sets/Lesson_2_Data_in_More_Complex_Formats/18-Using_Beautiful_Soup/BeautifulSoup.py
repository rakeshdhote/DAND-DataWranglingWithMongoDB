# -*- coding: utf-8 -*-
"""
Created on Tue Jul 07 00:30:51 2015

@author: Rakesh
"""

from bs4 import BeautifulSoup

def options(soup, id):
    option_values = []
    carrier_list = soup.find(id=id)
    for option in carrier_list.find_all('option'):
        option_values.append(option['value'])
    return option_values

def print_list(label, codes):
    print "\n%s : " % label
    for c in codes:
        print c

def test():
    soup = BeautifulSoup(open("page_source.html"))

    codes = options(soup, 'CarrierList')
    print_list("Carriers", codes)

    codes = options(soup, 'AirportList')
    print_list("Airport", codes)

test()