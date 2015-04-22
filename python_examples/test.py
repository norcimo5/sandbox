#!/usr/bin/python

def start(x):
  def increment(y):
    return x + y
  return increment


first_inc = start(0)

second_inc = start(8)

print first_inc(3)
print second_inc(3)
