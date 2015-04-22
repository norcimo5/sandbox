#!/usr/bin/env python2.7
import ConfigParser, StringIO

ini_str = '[root]\n' + open('./node.properties', 'r').read()
ini_fp = StringIO.StringIO(ini_str)
config = ConfigParser.RawConfigParser()
config.readfp(ini_fp)

print config.get('root', 'node.site_id')

