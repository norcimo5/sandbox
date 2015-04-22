import socket
import select
import threading
import xml.etree.ElementTree as ET
import time
import datetime

class LGS_Comm(object):
    """
    Simple UDP client to talk/listen to LGS system, with a callback.
    Tom Rafferty, July, 2013
    """

    def __init__(self, LGS_ip, LGS_port, host_ip, host_port):
        self.LGS_ip = LGS_ip
        self.LGS_port = LGS_port
        self.host_ip = host_ip
        self.host_port = host_port
        self.listener_callback = None

        # create UDP socket
        self.socket = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

    def send_request(self, msgType):
        r = self.create_reqstr(msgType)
        print r + "\n"
        self.sendMsg( r )
        
    def set_listener_callback(self, listener_callback):
        self.listener_callback = listener_callback

    def sendMsg(self, msg):
        """
        Send a message to the LGS device
        """
        self.socket.sendto(msg, (self.LGS_ip, self.LGS_port))

    def start(self):
        """
        Start the listening thread
        """
        self.alive = True
        self.thread = threading.Thread(target=self._listener)
        self.thread.start()
        time.sleep(0.1)
        
    def stop(self):
        """
        Stop the listening thread
        """
        self.alive = False
        self.thread.join()

    def _listener(self):
        print '[Starting listening thread]'
        listener_socket = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
        listener_socket.setblocking(0)
        listener_socket.bind((self.host_ip, self.host_port))
        while self.alive:
            data_avail = select.select([listener_socket], [], [], 1) # listen for 1 sec
            if data_avail[0]:
                data, addr = listener_socket.recvfrom(4096) 
                if self.listener_callback is not None:
                    self.listener_callback(data)
        print '[Finishing listening thread]'

    def create_reqstr(self, msgType):
        host_protocol = "udp"
        # now = datetime.datetime.today()   # localtime
        now = datetime.datetime.utcnow()  # UTC time
        future = now + datetime.timedelta(minutes=2)
        start = future.isoformat()[0:-4] + 'Z'
        time = start

        value = '/>'    #default

        if msgType == 'stopCollect':
          msgType = 'collect'
          future = future - datetime.timedelta(hours=1)
          value = '><collect iq-port="0" /></sewsi>'
        elif msgType == 'startCollect':
          msgType = 'collect'
          future = future + datetime.timedelta(hours=1)
          value = '><collect iq-port="50102" /></sewsi>'
        else:
          future = future + datetime.timedelta(hours=1)

        if msgType == 'stopSweep':
          msgType = 'sweep'
          future = future - datetime.timedelta(hours=1)
          value = '><sweep startHz="" stopHz="" stepHz="" /></sewsi>'
        elif msgType == 'startSweep':
          msgType = 'sweep'
          future = future + datetime.timedelta(hours=1)
          value = '><sweep startHz="150000000" stopHz="160000000" stepHz="1000000" /></sewsi>'
        else:
          future = future + datetime.timedelta(hours=1)
 
				
				#all
        stale = future.isoformat()[0:-4] + 'Z'

        if msgType == 'setConfig':        
          msgType = 'config'
          value = '><config is-set="yes" freq="1.624e+06" attn="36" info-tasking="yes" Bandwidth="10000" Channel-id="0" power="on"/></sewsi>'
        elif msgType == 'startNavigation':
          msgType = 'navigation'
          value = '><navigation is-set="yes" pvt="yes" ins="no" address="192.168.11.19:0" /></sewsi>'        
        elif msgType == 'stopNavigation':
          msgType = 'navigation'
          value = '><navigation is-set="yes" pvt="yes" ins="no" address="192.168.11.19:0" /></sewsi>' 

        return ("<?xml version='1.0' standalone='yes'?>"
                 '<event how="m-g" stale="%s" start="%s" time="%s" type="t-x-i" uid="ExternalSystem.58" version="2.0">'
                   '<point ce="" hae="" lat="" le="" lon=""/>'
                   '<detail>'
                     '<request notify="%s:%d:%s"/>'
                     '<sewsi msg="%s" version="1.0"'
                     '%s'
                   '</detail>'
                 '</event>') % (stale, start, time, self.host_ip, self.host_port, host_protocol, msgType, value)

def default_listener_callback(data):
    print "Rcv'd: \n", data
    
def parsing_listener_callback(data):
    print "Rcv'd reply:"
    root = ET.fromstring(data)
    if root.tag == 'event':
        print " Event:"
        for key,val in root.attrib.iteritems():
            print "  %s: %s" % (key, val)
    p = root.findall(".//point")
    if len(p) > 0:
        print " Point:"
        for key,val in p[0].attrib.iteritems():
            print "  %s: %s" % (key, val)
    s = root.findall(".//sewsi")
    if len(s) > 0:
        msg = s[0].attrib['msg']
        if msg == 'state':
            state = s[0].findall('state')
            if len(state) > 0:
                print " State:"
                print "  locked   : %s" % state[0].attrib['locked'] 
                print "  busy     : %s" % state[0].attrib['busy'] 
                print "  fault    : %s" % state[0].attrib['fault'] 
                print "  reference: %s" % state[0].attrib['reference'] 
                for radioState in s[0].iter('radioState'):
                    print "  Radio chan[%s]:" % radioState.attrib['channel-id'] 
                    print "    state: %s" % radioState.attrib['state'] 
            else:
                print " state ACK"
        elif msg == 'cap':
            cap = s[0].findall('cap')
            if len(cap) > 0:
                print " Capabilites:"
                print "  Collect    : %s" % cap[0].attrib['collect'] 
                print "  collect-url: %s" % cap[0].attrib['collect-url'] 
                print "  info-hp    : %s" % cap[0].attrib['info-hp'] 
                print "  mcast      : %s" % cap[0].attrib['mcast'] 
                print "  mcast-addr : %s" % cap[0].attrib['mcast-addr'] 
                for radioCap in s[0].iter('radioCap'):
                    print "  Radio chan[%s]:" % radioCap.attrib['channel-id'] 
                    print "    start-freq: %s" % radioCap.attrib['start-freq'] 
                    print "    stop-freq : %s" % radioCap.attrib['stop-freq'] 
                    print "    start-bw  : %s" % radioCap.attrib['start-bw'] 
                    print "    stop-bw   : %s" % radioCap.attrib['stop-bw'] 
                    print "    is-collect: %s" % radioCap.attrib['is-collect'] 
                    print "    is-array  : %s" % radioCap.attrib['is-array']
            else:
                print " cap ACK"
        elif msg == 'config':
            config = s[0].findall('config')
            if len(config) > 0:
                print " Config:"
                print "  is-set      : %s" % config[0].attrib['is-set'] 
                print "  freq        : %s" % config[0].attrib['freq'] 
                print "  attn        : %s" % config[0].attrib['attn'] 
                print "  info-tasking: %s" % config[0].attrib['info-tasking'] 
                print "  reference   : %s" % config[0].attrib['reference'] 
            else:
                print " cap ACK"
        elif msg == 'info-lp':
            print "info-lp message not implemented yet..."
        elif msg == 'info-hp':
            print "info-hp message not implemented yet..."
        elif msg == 'sweep':
            print "sweep message not implemented yet..."
        elif msg == 'navigation':
            print "navigation message not implemented yet..."
        else:
            print data

if __name__ == "__main__":

    #NOTE: change LGS_ip value
    #LGS_ip    = "192.168.131.130"  #SS1    
    LGS_ip    = "192.168.129.5"     #SS2
    LGS_port  = 50100

    host_ip   = "0.0.0.0"
    host_port = 50101

    lgs = LGS_Comm( LGS_ip, LGS_port, host_ip, host_port )
    lgs.set_listener_callback( default_listener_callback )
    #lgs.set_listener_callback( parsing_listener_callback )
    lgs.start()
    
    try:

        #######################################
        ## Message Types in ICD v0.3
        #   -cap
        #     -radioCap
        #   -state
        #     -radioState
        #   -config
        #   -collect 
        #   -info-lp
        #   -info-hp
        #   -sweep
        #   -navigation
        # 
        ## Message Protocol
        #   ACK
        #   RESPONSE
        #   COMPLETE
        #######################################

        print "+++++++Sending capability request...+++++++"
        lgs.send_request(msgType="cap")
        time.sleep(1)

        print "+++++++Sending state request...+++++++"
        lgs.send_request(msgType="state")
        time.sleep(1)

#        print "+++++++Sending start sweep request...+++++++"
#        lgs.send_request(msgType="startSweep")
#        time.sleep(1)

        print "+++++++Sending set config request...+++++++"
        lgs.send_request(msgType="setConfig")
        time.sleep(1)

 #       print "+++++++Sending state request...+++++++"
 #       lgs.send_request(msgType="state")
 #       time.sleep(1)

        print "+++++++Sending start collect request...+++++++"
        lgs.send_request(msgType="startCollect")
        time.sleep(1)

        print "+++++++Sending state request...+++++++"
        lgs.send_request(msgType="state")
        time.sleep(1)

        time.sleep(10);

 #       print "+++++++Sending state request...+++++++"
 #       lgs.send_request(msgType="state")
 #       time.sleep(1)

 #       print "+++++++Sending state request...+++++++"
 #       lgs.send_request(msgType="state")
 #       time.sleep(1)

 #       print "+++++++Sending state request...+++++++"
 #       lgs.send_request(msgType="state")
 #       time.sleep(1)

 #       print "+++++++Sending state request...+++++++"
 #       lgs.send_request(msgType="state")
 #       time.sleep(1)

        print "+++++++Sending stop collect request...+++++++"
        lgs.send_request(msgType="stopCollect")
        time.sleep(1)

#        print "+++++++Sending stop sweep request...+++++++"
#        lgs.send_request(msgType="stopSweep")
#        time.sleep(1)

        print "+++++++Sending state request...+++++++"
        lgs.send_request(msgType="state")
        time.sleep(1)

#   OTHER MESSAGES
#        print "+++++++Sending get config request...+++++++"
#        lgs.send_request(msgType="config")
#        time.sleep(1)
#        print "+++++++Sending start navigation request...+++++++"
#        lgs.send_request(msgType="startNavigation")
#        time.sleep(1)
#        print "+++++++Sending stop navigation request...+++++++"
#        lgs.send_request(msgType="stopNavigation")
#        time.sleep(1)
#        print "+++++++Sending navigation request...+++++++"
#        lgs.send_request(msgType="navigation")
#        time.sleep(1)
#        print "+++++++Sending info-lp request...+++++++"
#        lgs.send_request(msgType="info-lp")
#        time.sleep(1)
#        print "+++++++Sending info-hp request...+++++++"
#        lgs.send_request(msgType="info-hp")
#        time.sleep(1)
#        print "+++++++Sending sweep request...+++++++"
#        lgs.send_request(msgType="sweep")
#        time.sleep(1)

    except:
        raise
    finally:
        lgs.stop()
