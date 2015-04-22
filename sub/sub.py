#!/usr/bin/python
import subprocess as sub

def run_something():
    df = sub.Popen(['ls', '-ltrah'], stdout=sub.PIPE)
    output = df.communicate()[0]

    print output

run_something()
