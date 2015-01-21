#!/usr/bin/env python
import ConfigParser

email = raw_input('Please supply your Cloudflare login email: ')
tkn = raw_input('Please supply your Cloudflare API Token: ')
zone = raw_input('Please supply the dns zone : ')
host = raw_input('Please supply the dns host within the zone to update - this is just the name, not the FQDN: ')


config = ConfigParser.RawConfigParser()

config.add_section('Cloudflare')
config.set('Cloudflare', 'tkn', tkn)
config.set('Cloudflare', 'email', email)
config.set('Cloudflare', 'zone', zone)
config.set('Cloudflare', 'host', host)

# Writing our configuration file to 'example.cfg'
with open('/etc/ddclient/cloudflare.cfg', 'wb') as configfile:
    config.write(configfile)
