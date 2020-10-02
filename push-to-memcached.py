import hashlib
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from pymemcache.client.base import Client
import json
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

XXX_syslog01 = Client(('10.0.0.1', 11211))
XXX_syslog01 = Client(('10.0.0.2', 11211))
XXX_syslog01 = Client(('10.0.0.3', 11211))


def misppull(dataType):
  headers={'Authorization':'ADD_MISP_API_KEY','Accept':'application/json','Content-type':'application/json'}
  data=json.dumps({"returnFormat":"json","type":dataType,"tags":["export"],"to_ids":"yes","includeEventTags":"yes","includeContext":"yes"})
  response = requests.post('https://MISP_IP/attributes/restSearch',headers=headers,data=data,verify=False)
  return response

if __name__ == '__main__':
  dataTypes={'domain', 'md5', 'sha256', 'url', 'hostname'}
  for dt in dataTypes:
    response = misppull(dt)
    data=response.json()
    if 'response' in data:
      for item in data["response"]["Attribute"]:
        tagList=[]
        if item['type'] == 'url':
          itemValue = str(hashlib.md5(str(item['value']).encode('utf-8')).hexdigest())
          itemType = item['type']
        else:
          itemValue = item['value']
          itemType = item['type']
        if itemType == 'hostname':
          itemType = 'domain'
        for tag in item['Tag']:
          for k,v in tag.items():
            if(k=='name' in tag['name']):
              tagList.append(str(v))
        XXX_syslog01.set(str(itemType + '-' + itemValue), tagList, 86400)
        XXX_syslog01.set(str(itemType + '-' + itemValue), tagList, 86400)
        XXX_syslog01.set(str(itemType + '-' + itemValue), tagList, 86400)

