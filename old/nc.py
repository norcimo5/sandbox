#!/usr/bin/env python

import socket
import json

#H = dict(line.strip().split('=') for line in open('filename.txt'))

def netcat(hostname, port, content):
    myfile = open("output.txt", "w")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname, port))
    s.sendall(content)
    s.shutdown(socket.SHUT_WR)
    while 1:
        data = s.recv(1024)
        if data == "":
            break
        #print "Received:", repr(data)
        mydata = eval(repr(data))
        print mydata[:-2]
        j = json.loads(mydata.replace(";",""))
        myfile.write(str(j))
    print "Connection closed."
    s.close()
    myfile.close()

#netcat('192.168.129.10', 5072 , '{ "command" : "radioInfo", "parameters" :"" };')
#netcat('192.168.129.10', 5072 , '{ "command" : "radioStatus", "parameters" :"" };')
#netcat('192.168.129.10', 5072 , '{ "command" : "setLedOn", "parameters": "false"};{ "command" : "isLedOn", "parameters": ""};')
netcat('192.168.129.10', 5072 , '{ "command" : "isLedOn", "parameters": ""};')
#netcat('192.168.129.10', 5072 , '{ "command" : "cap", "parameters": ""};')
#netcat('192.168.129.10', 5072 , '{ "command" : "ledOn", "parameters": "true"};')
 
