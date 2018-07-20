#!/usr/bin/env python
import urllib2
import csv
import json
import sys

"""
Timestamp of Listing (UTC),Referencing Sample (MD5),Destination IP,Destination Port,SSL certificate SHA1 Fingerprint,Listing reason
"""

tmp = []

t = dict()
response = urllib2.urlopen('https://sslbl.abuse.ch/downloads/ssl_extended.csv')
for line in response.readlines():
        if  not line.startswith('#'):
                l = line.strip().split(',')
                try:
                        timeadded = l[0]
                        md5 = l[1]
                        dstip = l[2]
                        dstport = l[3]
                        sha1 = ':'.join(a+b for a,b in zip(l[4][::2], l[4][1::2]))
                        reason = l[5]
                except Exception as err:
                        print ('Error while unpacking')
                finally:
                        t[sha1] = {'sha1':sha1, 'temeadded':timeadded, 'md5':md5, 'dstip':dstip, 'dstport':dstport, 'reason':reason}

filename = sys.argv[1]
with open(filename,'w') as f:
        f.write(json.dumps(t, indent=2))
