#!/usr/bin/python
true = True
false = False
null = None
myresponse = '{ "response" : [ { "cmd" : "setLedOn", "parameters" : "bool", "definition" : "Turn on/off LED on 4411 Unit"} ] } '

json_dict = eval(myresponse)

print json_dict
