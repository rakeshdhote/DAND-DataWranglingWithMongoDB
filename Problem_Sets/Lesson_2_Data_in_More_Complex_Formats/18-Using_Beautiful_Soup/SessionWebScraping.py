# -*- coding: utf-8 -*-
"""
Created on Tue Jul 07 10:39:57 2015

@author: Rakesh
"""

address = "http://www.transtats.bts.gov/Data_Elements.aspx?Data=2"
from bs4 import BeautifulSoup
import requests

s = requests.Session()

r = s.get(address)
soup = BeautifulSoup(r.text)
viewstate_element = soup.find(id="__VIEWSTATE")
viewstate = viewstate_element["value"]
eventvalidation_element = soup.find(id="__EVENTVALIDATION")
eventvalidation = viewstate_element["value"]

r = s.post(address,
           data={'AirportList':'BOS',
                 'CarrierList':'VX',
                 'Submit': 'Submit',
                 '_EVENTTARGET':'',
                 '_EVENTARGUMENT':'',
                 '_EVENTVALIDATION': eventvalidation,
                 '_VIEWSTATE': viewstate})

f = open('Virgin and logan airport.html','w')
f.write(r.text)