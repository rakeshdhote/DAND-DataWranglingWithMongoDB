# -*- coding: utf-8 -*-
"""
Created on Wed Jul 08 22:55:00 2015

@author: Rakesh
"""



data = []
d = { "item1": None,
     "item2": None
     }

for i in range(3):
    d["item1"] = i+1
    d["item2"] = i+2
    data.extend(d)
    print "data1 = ", d

print "data = ", data