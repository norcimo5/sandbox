#!/usr/bin/env python2.7

o = "unknown"
s = o.ljust(28, ' ')[:28]
w = [ ord(e) for e in s ]
print w
