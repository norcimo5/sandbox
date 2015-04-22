#!/usr/bin/env python2.7


s1 = " "
s2 = " "
m = []
m.append(0x05)
m +=bytearray(s1.ljust(54,' ')[:54])
m +=bytearray(s1.ljust(54,' ')[:54])
print m
print len(m)
