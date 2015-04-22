#!/usr/bin/python

import random


def mypattern(num):
  return bin(num).strip("0b").zfill(32).replace('0',' ').replace('1', '+')

for i in range(0,32):
  print mypattern(random.randrange(0, 4294967296))
  
