#!/usr/bin/python

#--- Not the most automatic script, changing csv headers depending on the file we are loading. 

import json
import csv
import time

infilename = "images.json"  

infile = open(infilename, "r")

images = []
for line in infile:
    try:
        new_image = json.loads(line)
    except:
        continue
    images.append(new_image)

csvwriter = csv.writer(open("videoLinks.csv", "w"))
csvwriter.writerow(["url", "title", "videoLink"])
for im in images:
    url = im["url"]
    title = im["title"]
    imageLinks = im["videoLinks"]
    for il in imageLinks:
        newrow = [url, title, il]
        for i in range(len(newrow)):
            if hasattr(newrow[i], 'encode'):
                newrow[i] = newrow[i].encode('utf8')
        csvwriter.writerow(newrow)

