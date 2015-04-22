#!/usr/bin/python

def midpoint_sum(ints):
    if len(ints) <=2: return None
    
    left = [ints[0]]
    right = {}
    
    for i in range(1, len(ints)/2):
        left.append(ints(i)+ints(i-1))
        

midpoint_sum([4,1,7,9,3,9])
