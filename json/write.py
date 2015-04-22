#!/usr/bin/python

mylist = [ 5*i for i in range(0,5) ]

f = open("./test.txt","w")

for item in mylist:

    f.write(str(item) + "\n")
