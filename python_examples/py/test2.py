#!/usr/bin/python
import struct
import binascii

packed_data = binascii.unhexlify('0100000061620000cdcc2c40')

myfile = open("./testfile.txt", "w")
myfile.write(packed_data)
myfile.close()
