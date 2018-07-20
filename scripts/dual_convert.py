#!/usr/bin/env python
import csv
import json
import sys

tmp = []

ipv4_in = dict()
ipv4_out = dict()
fqdn = dict()
#"103.77.228.76","IPv4","inbound","http://www.blocklist.de/lists/courierimap.txt","","2018-03-08"
response = open('/etc/logstash/scripts/combine/harvest.csv')
for line in response.readlines():
        if  not line.startswith('#'):
                try:
                        entity, type, direction, source, notes, date = [_.strip("\"\r\n") for _ in line.split(",")]
                except Exception as err:
                        print ('Error while unpacking')
                finally:
                        if type == "IPv4" and direction == "inbound":
                                ipv4_in[entity] = {'entity':entity, 'type':type, 'direction':direction, 'source':source, 'notes':notes, 'date':date}
                        elif type == "IPv4" and direction == "outbound":
                                ipv4_out[entity] = {'entity':entity, 'type':type, 'direction':direction, 'source':source, 'notes':notes, 'date':date}
                        else:
                                fqdn[entity] = {'entity':entity, 'type':type, 'direction':direction, 'source':source, 'notes':notes, 'date':date}

#filename = 'ipv4-' + sys.argv[1]
filename = '/etc/logstash/translate/ipv4-in-combine.json'
with open(filename,'w') as f:
        f.write(json.dumps(ipv4_in, indent=2))

filename = '/etc/logstash/translate/ipv4-out-combine.json'
with open(filename,'w') as f:
        f.write(json.dumps(ipv4_out, indent=2))

#filename1 = 'fqdn-' + sys.argv[1]
filename1 = '/etc/logstash/translate/fqdn-combine.json'
with open(filename1,'w') as f1:
f1.write(json.dumps(fqdn, indent=2))
