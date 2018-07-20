#!/usr/bin/env python
import urllib2
import csv
import json
import sys
import re

"""
'myvipclubs.com', 'phishing', 'openphish.com', '20180202'
"""

tmp = []

t = dict()
response = urllib2.urlopen('https://urlhaus.abuse.ch/downloads/csv/')
for line in response.readlines():
        if  not line.startswith('#'):
                #l = line.re.strip().split('\",\"')
                l = re.compile('\",\"').split(line)
                try:
                        id = l[0]
                        dateadded = l[1]
                        url = l[2]
                        urlstatus = l[3]
                        threat = l[4]
                        tags = l[5]
                        urlhaus_link = l[6]
                except Exception as err:
                        print ('Error while unpacking')
                finally:
                        #print id, dateadded, url, urlstatus, threat, tags, urlhaus_link

                        t[url] = {'id':id, 'dateadded':dateadded, 'url':url, 'urlstatus':urlstatus, 'threat':threat, 'tags':tags, 'urlhaus_link':urlhaus_link}
#tmp.append(t)

#print json.dumps(tmp, indent=2)

filename = sys.argv[1]
with open(filename,'w') as f:
        f.write(json.dumps(t, indent=2))
