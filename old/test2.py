#!/usr/bin/env python

import socket
import json

def netcat():
    myfile = open("output.txt", "w")

    mydata = '{ "command": "radioInfo", "response": \n{ "id": "radio0", "serialNumber": "EDM02", "modelNumber": "8649", "manufacturer": "drs", "firmwareVersion": "DRS5.01-TG11.4", "numberOfChannels": "1", "numberOfTuners": "1", "minFrequencyHz": "2000000", "maxFrequencyHz": "3000000000", "minBandwidthHz": "5000", "maxBandwidthHz": "200000" } } ;'

    j = json.loads(mydata[:-1])
    print (j['command'])
    print "--------------------------------------------"
    for k, v in j['response'].items():
        print k  + "=" + v
    print "--------------------------------------------"
    myfile.close()
    print "Connection closed."

netcat()

