#! /usr/bin/env python
import os

question = os.system("zenity --question --text='continue?'")
if question == 256:
    print "Operation canceled."
    exit()
else:
    print "Operation continuing."  
