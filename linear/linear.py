#!/usr/bin/python

x = 50.0
y = 20.0
m = y / x

for dx in range(0, int(x)):
    dy = float(dx) * m
    print float(dx), dy
