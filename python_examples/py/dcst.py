#!/usr/local/bin/python2.7
################################################################################
# Name        : uCtlr.py
# Description : Python interface to uCtlr
# Author      : Manuel A. Perez
#
################################################################################

################################################################################
# IMPORTS                                                                      #
################################################################################
#import subprocess as sub
#import os, sys, socket, time, select, Queue, struct, datetime
#import threading, termios, signal, commands, re, binascii
#import ConfigParser, StringIO
#import json

################################################################################
# INIT                                                                         #
################################################################################

DEFAULT_UCTLR_LOG    = '-uCtlr_status.log'
DEFAULT_BIN_LOG      = '-BinaryDump_uCtlr_status.log'
DEFAULT_UCTLR_DEVICE = '/dev/ttyUSB3'
DEFAULT_LOG_DIR      = '/tmp/'
DEFAULT_NODE_FILE    = '/h/GEOnet/config/node.properties'
DEFAULT_STARMAN_FILE = '/h/GEOnet/bin/config/tm_starman_data.xml'
DEFAULT_GEONET_FILE  = '/dev/shm/geonet_status.snl'
UCTLR_STARTUP_FILE   = '/dev/shm/Starting_uCtlr-mon'
DEFAULT_DCST_PORT    = '5072'
DEFAULT_DCST_HOSTNAME= '127.0.0.1'
DEFAULT_DCST_OUTPUT  = '/tmp/output.txt'

################################################################################
# CLASS DEFINITIONS                                                            #
################################################################################

import time, socket, sys, select
import json

class dcstcommon:
    "Isolate socket handling and buffering from the protcol interpretation."
    def __init__(self, hostname=DEFAULT_DCST_HOSTNAME, port=DEFAULT_DCST_PORT):
        self.sock = None        # in case we blow up in connect
        self.linebuffer = ""
        self.dcstisup   = False
        self.connect(hostname, port)
        self.verbose = 0

    def connect(self, hostname, port):
        """Connect to a host on a given port.

        If the hostname ends with a colon (`:') followed by a number, and
        there is no port specified, that suffix will be stripped off and the
        number interpreted as the port number to use.
        """
        if not port and (host.find(':') == host.rfind(':')):
            i = host.rfind(':')
            if i >= 0:
                hostname, port = host[:i], host[i+1:]
            try: port = int(port)
            except ValueError:
                raise socket.error, "nonnumeric port"

        print '[DEBUG] Connect:', (hostname, port)
        msg = "getaddrinfo returns an empty list"
        self.sock = None
        for res in socket.getaddrinfo(hostname, port, 0, socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            try:
                self.sock = socket.socket(af, socktype, proto)
                self.sock.connect(sa)
            except socket.error, msg:
                self.close()
                continue
            break
        if not self.sock:
            self.dcstisup = False
        else:
            self.dcstisup = True

    def close(self):
        if self.sock:
            self.sock.close()
        self.sock = None

    def __del__(self):
        self.close()

    def isdcstup(self):
        return self.dcstisup

    def waiting(self):
        "Return True if data is ready for the client."
        if self.linebuffer:
            return True
        (winput, woutput, wexceptions) = select.select((self.sock,), (), (), 0)
        return winput != []

    def read(self):
        "Wait for and read data being streamed from the daemon."
        if self.verbose > 1:
            sys.stderr.write("poll: reading from daemon...\n")
        eol = self.linebuffer.find(';')
        if eol == -1:
            frag = self.sock.recv(4096)
            self.linebuffer += frag
            if self.verbose > 1:
                sys.stderr.write("poll: read complete.\n")
            if not self.linebuffer:
                if self.verbose > 1:
                    sys.stderr.write("poll: returning -1.\n")
                # Read failed
                return -1
            eol = self.linebuffer.find(';')
            if eol == -1:
                if self.verbose > 1:
                    sys.stderr.write("poll: returning 0.\n")
                # Read succeeded, but only got a fragment
                return 0
        else:
            if self.verbose > 1:
                sys.stderr.write("poll: fetching from buffer.\n")

        # We got a line
        eol += 1
        self.response = self.linebuffer[:eol]
        self.linebuffer = self.linebuffer[eol:]

        # Can happen if daemon terminates while we're reading.
        if not self.response:
            return -1
        if self.verbose:
            sys.stderr.write("poll: data is %s\n" % repr(self.response))
        self.received = time.time()
        # We got a \n-terminated line
        return len(self.linebuffer)

    def send(self, commands):
        "Ship commands to the daemon."
        if not commands.endswith(";"):
            commands += ";"
        self.sock.sendall(commands)

class dcst(dcstcommon):
    
    def __init__(self, command="", outputfile=DEFAULT_DCST_OUTPUT, host=DEFAULT_DCST_HOSTNAME, port=DEFAULT_DCST_PORT):
        dcstcommon.__init__(self, host, port)
        self.command = command
        self.success = 0
        self.commandmap = { 'drtinfo'   : '{ "command" : "radioInfo", "parameters" :"" };', \
                            'drtstatus' : '{ "command" : "radioStatus", "parameters" :"" };' }
    def exit(self):
        self.closeall()
        return self.success      

    def closeall(self):
        return 

    def reformat(self, data):
        result = {}
        j = json.loads(data.rstrip('\n').rstrip(';'))

        if 'command' in j.keys():
            if   j['command'] == 'isLedOn':
                for l in j['response']:
                    for k, v in l.items():
                        result.update( {j['command'] : v} )
            elif j['command'] == 'radioInfo':
                for l in j['response']:
                    for k, v in l.items():
                        result.update({ k : v })
            elif j['command'] == 'radioStatus':
                for l in j['response']:
                    for k, v in l.items():
                        if k == 'lock':
                            result.update({ (k + "." + "gps") : v['gps'] } )
                            result.update({ (k + "." + "ntp") : v['ntp'] } )
                        else:
                            result.update( {k : v} )

            del j['command']

        return result

    def sendmsg(self, command=""):
        if not self.dcstisup:
            try:
                self.connect(hostname, port)
                self.dcstup = True
            except:
                return None
            
        if command != "":
            self.command = command
        if self.command in self.commandmap.keys():
            if self.verbose:
                print "[DEBUG] Sending: " + self.commandmap[self.command]
            self.success = self.send(self.commandmap[self.command])
            if self.read() == -1:
                self.dcstisup = False
                return None

	    return self.reformat(self.response)

if __name__ == '__main__':
    session = dcst()
    #print session.sendmsg()
    a = session.sendmsg('drtinfo')
    b = session.sendmsg('drtstatus')

    if not a:
        print "nothing for a\n"
    else:
        print a
    if not b:
        print "nothing for b\n"
    else:
        print b
    sys.exit(session.exit())

#  ADD CODE TO START CONNECTION AND KEEP IT
#  CONNECTION SHOULD start when uCtlrcommon starts (?)
#  CONNECTION SHOULD DIE WHEN uctlrcommon dies
#  All errors should be trapped and not cause disruption
#  if unavailable, i should try connecting again
#  keep a variable or indicator to check if dcst service is up, and to try again after each sendmsg()
#  
