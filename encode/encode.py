#!/usr/bin/python

def encode(msg):
    return "".join("{:02x}".format(ord(x)^35) for x in msg)

msg = raw_input("Text to encode: ")
print encode(msg)

