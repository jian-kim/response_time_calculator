#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-

import googlemaps
import cgi
from datetime import datetime
import json
import numpy
import csv
import sys
import time
import math
# destination0 = "Hospital near " + origin
# destination1 = "Fire station near " + origin
# destination2 = "Police station near " + origin
# d0 = gmaps.directions(origin, destination0)
# pprint.pprint(d0)
# d1 = gmaps.directions(origin, destination1)
# d2 = gmaps.directions(origin, destination2)
# print d0[0]["legs"][0]["duration"]["text"]
# print d1[0]["legs"][0]["duration"]["text"]
# print d2[0]["legs"][0]["duration"]["text"]
gmaps = googlemaps.Client(key='AIzaSyCkbU_btpIR24iaWodK6Mb8a-317-sWZhs')
modu = 1000
def closestHospital(origin):
    reader = csv.reader(open("Hospital_General_Information.csv", "rb"), delimiter=",")
    zips = {}
    start = time.time()
    for i,v in enumerate(reader):
        if i == 0:
            continue
        if v[5][:5] not in zips.keys():
            zips[v[5][:5]] = [v]
        else:
            zips[v[5][:5]].append(v)
 #   print "Zip preprocess",time.time() - start
    start = time.time()
    ss = []
    if origin[-5:] in zips.keys():
        for iteration in range(int(math.ceil(len(zips[origin[-5:]]) * 1.0 / modu))):
	    addresses = ""
            info = []
            for ind, i in enumerate(zips[origin[-5:]][modu * iteration:modu * (iteration + 1)]):
		address = i[2] + ", " + i[3] + ", " + i[4] + ", " + i[5]
                addresses += address + "|"
                info.append(i)
            s = gmaps.distance_matrix(origin,addresses[:-1])["rows"][0]["elements"]
            for i, v in enumerate(s):
                if v["status"] != "OK":
                    continue
                ss.append((v["duration"]["value"], v, info[i]))
	ss.sort() 
#	print ss[0][1], ss[0][2]   
        return ss[0][1], ss[0][2]
    else:
        reader = csv.reader(open("Hospital_General_Information.csv", "rb"), delimiter=",")
        states = {}
        start = time.time()
        for i,v in enumerate(reader):
            if i == 0:
                continue
            if v[4] not in states.keys():
                states[v[4]] = [v]
            else:
                states[v[4]].append(v)
#         print "State preprocess",time.time() - start
        ss = []
        for iteration in range(int(math.ceil(len(states[origin[-9:-7]]) * 1.0 / modu))):
            addresses = ""
            info = []
            for ind, i in enumerate(states[origin[-9:-7]][modu * iteration:modu * (iteration + 1)]):
                address = i[2] + ", " + i[3] + ", " + i[4] + ", " + i[5]
                addresses += address + "|"
                info.append(i)
            s = gmaps.distance_matrix(origin,addresses[:-1])["rows"][0]["elements"]
            for i, v in enumerate(s):
                if v["status"] != "OK":
                    continue
                ss.append((v["duration"]["value"], v, info[i]))
        ss.sort()
#	print ss[0][1], ss[0][2]    
        return ss[0][1], ss[0][2]
#     print "Total",time.time() - start  
    
    
def closestFireStation(origin):
    reader = csv.reader(open("usfa-registry-national.txt", "rb"), delimiter=",")
    zips = {}
    start = time.time()
    for i,v in enumerate(reader):
        if i == 0:
            continue
        if v[6][:5] not in zips.keys():
            zips[v[6][:5]] = [v]
        else:
            zips[v[6][:5]].append(v)
#     print "Zip preprocess",time.time() - start
    start = time.time()
    ss = []
    if origin[-5:] in zips.keys():
        for iteration in range(int(math.ceil(len(zips[origin[-5:]]) * 1.0 / modu))):
            addresses = ""
            info = []
            for ind, i in enumerate(zips[origin[-5:]][modu * iteration:modu * (iteration + 1)]):
                if i[3] == "":
                    address = i[2] + ", " + i[4] + ", " + i[5]
                else:
                    address = i[2] + ", " + i[3] + ", " + i[4] + ", " + i[5]
                addresses += address + "|"
                info.append(i)
            s = gmaps.distance_matrix(origin,addresses[:-1])["rows"][0]["elements"]
            for i, v in enumerate(s):
                if v["status"] != "OK":
                    continue
                ss.append((v["duration"]["value"], v, info[i]))
        ss.sort()
#	print ss[0][1], ss[0][2]    
        return ss[0][1], ss[0][2]
    else:
        reader = csv.reader(open("usfa-registry-national.txt", "rb"), delimiter=",")
        states = {}
        start = time.time()
        for i,v in enumerate(reader):
            if i == 0:
                continue
            if v[5] not in states.keys():
                states[v[5]] = [v]
            else:
                states[v[5]].append(v)
#         print "State preprocess",time.time() - start
        ss = []
        for iteration in range(int(math.ceil(len(states[origin[-9:-7]]) * 1.0 / modu))):
            addresses = ""
            info = []
            for ind, i in enumerate(states[origin[-9:-7]][modu * iteration:modu * (iteration + 1)]):
                if i[3] == "":
                    address = i[2] + ", " + i[4] + ", " + i[5]
                else:
                    address = i[2] + ", " + i[3] + ", " + i[4] + ", " + i[5]
                addresses += address + "|"
                info.append(i)
            s = gmaps.distance_matrix(origin,addresses[:-1])["rows"][0]["elements"]
            for i, v in enumerate(s):
                if v["status"] != "OK":
                    continue
                ss.append((v["duration"]["value"], v, info[i]))
        ss.sort()   
#	print ss[0][1], ss[0][2]
        return ss[0][1], ss[0][2]
#     print "Total",time.time() - start         
form = cgi.FieldStorage()
print 'Content-type: text/html'
print

strt = form.getvalue('strt')
city = form.getvalue('city')
state = form.getvalue('state')
zip1 = form.getvalue('zip')
json1, row1 = closestHospital(strt + ", " + city + ", " + state + ", " + zip1)
json2, row2 = closestFireStation(strt + ", " + city + ", " + state + ", " + zip1)
print '''<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Response Time Calculator</title>
  <meta name="description" content="Response Time Calculator">
  <meta name="author" content="SitePoint">

  <link rel="stylesheet" href="index.css">
</head>

<body>
  <div style='position:absolute;z-index:-1;left:0;top:0;width:100%;height:100%'>
  <img src='../images/background.jpg' style='width:100%;height:100%' alt='[]' />
  </div>
  <div style="margin-top: 2%; margin-left: 4.5%; float: left; width:45%;height:500px;border:1px solid #FFFFFF;">
      <p style="color:white; margin-left:2%;font-size:15px;font:Lucida Console, Monaco, monospace">Nearest Hospital: ''' +row1[1]+'''</p>
      <p style="color:white; margin-left:2%;font-size:15px;font:Lucida Console, Monaco, monospace"> Hospital Response Time:''' + json1["duration"]["text"] + '''</p>
      <p style="color:white; margin-left:2%;font-size:15px;font:Lucida Console, Monaco, monospace"> Nearest Firefighter Station:'''+ row2[1] +'''</p>
      <p style="color:white; margin-left:2%;font-size:15px;font:Lucida Console, Monaco, monospace"> Firefighter Station Response Time:''' + json2["duration"]["text"] + '''</p>
  </div>
  <div style="margin-top: 2%; margin-left: 0.5%; float: left; width:45%;height:500px;border:1px solid #FFFFFF;">
    <iframe src="https://www.google.com/maps/embed?pb=!1m14!1m12!1m3!1d94568.32752522979!2d-73.32915399999999!3d42.20888240000001!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!5e0!3m2!1sen!2sus!4v1492887346021" width="100%" height="100%" frameborder="0" style="border:0" allowfullscreen></iframe>
  </div>
</body>
</html>'''#%("t","s","s","t")# % (json1["duration"]["text"], row1[1], json2["duration"]["text"], row2[1])
