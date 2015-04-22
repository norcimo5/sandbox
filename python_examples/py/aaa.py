#!/usr/bin/env python2.7

import datetime

version = "1080 PCB Rev.A Fmwr 000.09"
javelinMsg = "#############################################################\n[ " \
              + datetime.datetime.now().strftime('%Y.%m.%d-%H:%M:%S') + " ]  "  + version + "\n" \
              + ("CBR core0 Temperature, \t%d,\t0,\t95\n" % 70) \
              + ("CBR core2 Temperature, \t%d,\t0,\t95\n" % 70)

f = open('/dev/shm/Javelin-health.txt', 'w')
f.write(javelinMsg)
f.close()
