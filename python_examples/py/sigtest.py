#!/usr/bin/env python2.7


import signal, os
import time

def handler(signum, frame):
  print 'signal handler called with signal', signum
  
signal.signal(signal.SIGINT, handler)

while True:
    time.sleep(1)
    print "Tick\n"
