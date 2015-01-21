#!/usr/bin/env python
import json
import ConfigParser
import pycurl
from StringIO import StringIO
from urllib import urlencode

buffer = StringIO()
curip = StringIO()

config = ConfigParser.RawConfigParser()
config.read('/etc/ddclient/cloudflare.cfg')

tkn = config.get('Cloudflare', 'tkn')
email = config.get('Cloudflare', 'email')
zone = config.get('Cloudflare', 'zone')
host = config.get('Cloudflare', 'host')
fqdn = '"'+host+'.'+zone+'"'

def curlPage(url, post_data=None):
    buffer = StringIO()
    if post_data:
        postfields = urlencode(post_data)
    else:
        postfields = None

    c = pycurl.Curl()
    if postfields != None:
        c.setopt(c.POSTFIELDS, postfields)

    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    
    return buffer

#get all records so we can parse for the rec_id for dyndns to update
#bash # curl --data "?a=rec_load_all&tkn=%{tkn}&email=%{email}&z=%{zone}" https://www.cloudflare.com/api_json.html

post_data = {'a' : 'rec_load_all', 'tkn' : tkn, 'email' : email, 'z' : zone}
buffer = curlPage('https://www.cloudflare.com/api_json.html', post_data)
body = buffer.getvalue()

#print json.dumps(body, indent=1)

try:
    decoded = json.loads(body)
    #print json.dumps(decoded['response']['recs']['objs'], sort_keys=True, indent=4)
    for resource in decoded['response']['recs']['objs']: #, sort_keys=True, indent=4)
        #rec_id exists, we can update the record
        if json.dumps(resource['name']) == fqdn:
            #print json.dumps(resource)
            rec_id = json.dumps(resource['rec_id'])
            '''
            
            
#        if resource['name'] == host:
#            print resource['rec_id']
'''
except (ValueError, KeyError, TypeError):
    print "JSON format error"


recid = rec_id[1:-1]

#This almost Works
curip = curlPage('http://checkip.amazonaws.com/')
newip = curip.getvalue()
newip = newip.replace('\n','')

post_data = {'a': 'rec_edit', 'tkn': tkn, 'id':recid, 'email':email, 'z': zone, 'type':'A', 'name':host, 'content':newip, 'ttl':'120'}
print post_data
buffer = curlPage('https://www.cloudflare.com/api_json.html', post_data)
body = buffer.getvalue()
print json.dumps(body, sort_keys=True, indent=4)
