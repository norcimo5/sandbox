#!/usr/bin/env python

# $Id: runp.py 155066 2013-04-26 14:08:55Z acopeland $

import os
import sys
import socket
import time

JICD_PROXY_REGEX='.*/jicd_.*'

FTP_BASE_DIR='/localhome/flink'
FTP_DIR_SUFFIX='/'+os.environ['USER']+'/runp'
FTP_SERVER_DIR=FTP_BASE_DIR+FTP_DIR_SUFFIX

RUNP_LINK_CON_PATH='/tmp/runp_link_con/' + str(os.getpid())

def _is_socket_JICD(transport_type):
  return transport_type == 'socket_JICD_sink' or transport_type == 'socket_JICD_source'

class Sensor:
    def __init__( self, tokens ):
        self.file = tokens[1]
        self.site_id = tokens[2]
        global used_ports
        if ( tokens[3] != 'auto' ):
            self.port = int(tokens[3])
            used_ports.append( self.port )
        else:
            self.port = -1
        self.flags = {}
        self.flags['ntg'] = 'true'
        #if ( len( tokens ) > 3 ):
        #    print "Extra tokens for", self.site_id, ": ", tokens[4:]
        for extra in tokens[4:]:
            key, value = extra.split( '=' )
        #    print '  ', key, '->', value
            self.flags[key] = value
        if ( self.flags['ntg'] == 'true' and options.ntg_tree == '' ):
            print "At least one node (",self.site_id,") requires NTG, but no run tree is specified"
            sys.exit( 1 )

class RealSensor:
    def __init__( self, tokens ):
        self.site_id = tokens[1]
        global used_ports
        if ( tokens[2] != 'auto' ):
            self.port = int(tokens[2])
            used_ports.append( self.port )
        else:
            self.port = -1
        self.flags = {}
        self.flags['ntg'] = 'true'
        for extra in tokens[3:]:
            key, value = extra.split( '=' )
            self.flags[key] = value

class NoSensor:
    def __init__( self, tokens ):
        self.site_id = tokens[1]
        global used_ports
        if ( tokens[2] != 'auto' ):
            self.port = int(tokens[2])
            used_ports.append( self.port )
        else:
            self.port = -1
        self.flags = {}

class ClonedSensor:
    def __init__( self, tokens ):
        self.source_site_id = tokens[1]
        self.site_id = tokens[2]
        global used_ports
        if ( tokens[3] != 'auto' ):
            self.port = int(tokens[3])
            used_ports.append( self.port )
        else:
            self.port = -1
        self.flags = {}
        self.flags['ntg'] = 'true'
        for extra in tokens[4:]:
            key, value = extra.split( '=' )
            self.flags[key] = value


class Gate:
    def __init__( self, levels, tokens ):
        global default_transport
        self.site_id = tokens[1]
        global used_ports
        if ( tokens[2] != 'auto' ):
            self.port = int(tokens[2])
            used_ports.append( self.port )
        else:
            self.port = -1

        self.levels = levels

        self.flags = {'transport': default_transport,
                      'supportsMetrics' : 'true',
                      'ntg': 'true',
                      'ntg_proxy': '',
                      'ntg_proxy_regex':'.*',
                      'ip': None}

        self.flags['ntg'] = 'true'
        for extra in tokens[3:]:
            key, value = extra.split( '=' )
            self.flags[key] = value
        if ( self.flags['ntg'] == 'true' and options.ntg_tree == '' ):
            print "At least one node (",self.site_id,") requires NTG, but no run tree is specified"
            sys.exit( 1 )
        if self.flags['transport'] not in transport_types:
            print "Do not recognize transport type " + self.flags['transport']
            sys.exit(1)

class Observer:
    def __init__( self, tokens ):
        self.site_id = tokens[1]
        global used_ports
        if ( tokens[2] != 'auto' ):
            self.port = int(tokens[2])
            used_ports.append( self.port )
        else:
            self.port = -1
        self.flags = {'ntg': 'true'}
        for extra in tokens[3:]:
            key, value = extra.split( '=' )
        #    print '  ', key, '->', value
            self.flags[key] = value
        if ( self.flags['ntg'] == 'true' and options.ntg_tree == '' ):
            print "At least one node (",self.site_id,") requires NTG, but no run tree is specified"
            sys.exit( 1 )

class MessageSwitch:
    def __init__( self, tokens ):
        self.site_id = tokens[1]
        self.base_directory = tokens[2]
        global used_ports
        if ( tokens[3] != 'auto'):
          self.port = int(tokens[3])
          used_ports.append(self.port)
        else:
          self.port = -1
        self.flags = dict()
        for extra in tokens[4:]:
            key, value = extra.split( '=' )
            self.flags[key] = value
        self.flags['transport'] = 'ntg'
        if (not self.flags.has_key('start_proxy_and_ntg')): self.flags['start_proxy_and_ntg'] = 'true'


class Network:
    def __init__ ( self, filenames ):
        global options
        self.geonet_nodes = []
        self.real_geonet_nodes = []
        self.jicd_nodes = []
        self.geonet_observers = []
        self.jicd_observers = []
        self.geonet_gate = None
        self.jicd_gate = None
        self.extra_tacticals_distance_to_emitter = 2000
        self.extra_tacticals = 0
        self.extra_tacticals_created = 0
        self.message_switch = None
        import re

        for filename in filenames:
          file = open( filename, 'r' )
          line = file.readline()
          while line:
            if ( re.search( r'^\s*\n*$', line ) ):
              line = file.readline()
              continue
            if ( re.search( r'^\s*#', line ) ):
              while ( re.search( r'\\$', line ) ):
                line = file.readline()
              line = file.readline()
              continue

            tokens = line.split()
            #print tokens
            if ( tokens[0] == 'node' ):
                self.geonet_nodes.append( Sensor( tokens ) )
            elif ( tokens[0] == 'real_node' ):
                self.real_geonet_nodes.append( RealSensor( tokens ) )
            elif ( tokens[0] == 'cloned_node' ):
                self.geonet_nodes.append( ClonedSensor( tokens ) )
                self.extra_tacticals += 1
            elif ( tokens[0] == 'tm_node' ):
                self.geonet_nodes.append( NoSensor( tokens ) )
            elif ( tokens[0] == 'gate' ):
                assert( not self.geonet_gate )
                self.geonet_gate = Gate( geonet_gate_levels[options.black_level], tokens)
            elif ( tokens[0] == 'observer' ):
                self.geonet_observers.append( Observer( tokens ) )
            elif ( tokens[0] == 'jnode' ):
                self.jicd_nodes.append( Sensor( tokens ) )
            elif ( tokens[0] == 'jgate' ):
                assert( not self.jicd_gate )
                self.jicd_gate = Gate( jicd_gate_levels[options.black_level], tokens )
            elif ( tokens[0] == 'jobserver' ):
                self.jicd_observers.append( Observer( tokens ) )
            elif ( tokens[0] == 'extra_tacticals_distance_to_emitter' ):
                self.extra_tacticals_distance_to_emitter = int(tokens[1])
            elif ( tokens[0] == 'message_switch' ):
                assert( not self.message_switch )
                self.message_switch = MessageSwitch( tokens )
            else:
                print "Unknown entry type:", tokens[0], " in line: ", line

            line = file.readline()


        # If there is a near-side gate and a far-side gate, and nobody's overridden proxy
        # parameters, use the message switch by default. 
        if (self.geonet_gate and self.geonet_gate.flags['ntg_proxy'] == '' and self.jicd_gate and self.jicd_gate.flags['ntg_proxy'] == ''):
                global JICD_PROXY_REGEX
                geonet_flags = self.geonet_gate.flags
                jicd_flags = self.jicd_gate.flags
                if (not self.message_switch): self.message_switch = MessageSwitch( ['message_switch', 'msg_switch', '/tmp/jicd', 'auto'] )
                if (geonet_flags['transport'] == 'ntg'):
                  geonet_flags['ntg_proxy'] = self.message_switch.site_id
                  geonet_flags['ntg_proxy_regex'] = JICD_PROXY_REGEX
                if (jicd_flags['transport'] == 'ntg'):
                  jicd_flags['ntg_proxy'] = self.message_switch.site_id
                  jicd_flags['ntg_proxy_regex'] = JICD_PROXY_REGEX

        if (self.message_switch and not (self.geonet_gate and self.jicd_gate)):
            print "Note: there is a message switch specified, but only one gate. If this is not multi-jicd mode, there may be a configuration issue.\n"

        #for gate-to-gate ntg or socket JICD, some gates have to be sinks (near-side) and some not (far-side)
        if options.gate_is_source and self.geonet_gate and not self.jicd_gate:
            self.jicd_gate = self.geonet_gate
            self.jicd_nodes = self.geonet_nodes + self.real_geonet_nodes
            self.jicd_observers = self.geonet_observers
            self.geonet_gate = None
            self.geonet_nodes = []
            self.geonet_observers = []

        # If both gates exist and it's a socket JICD configuration, give the user an early failure if it's misconfigured.
        if (self.geonet_gate and _is_socket_JICD(self.geonet_gate.flags['transport']) and self.jicd_gate and _is_socket_JICD(self.jicd_gate.flags['transport'])):
            assert(self.geonet_gate.flags['transport'] != self.jicd_gate.flags['transport']) # If this triggers, they're both a sink or both a source.

class MultiJICDGate:
    def __init__( self, tokens ):
        self.site_id = tokens[1]
        self.port = int(tokens[2])
        self.path = tokens[3]
        self.flags = { 'supportsMetrics' : 'true'}
        for extra in tokens[4:]:
          key, value = extra.split( '=' )
          self.flags[key] = value

num_jicd_links = 0
class MultiJICDLink:
    def __init__( self, tokens ):
        global num_jicd_links, default_transport
        self.gate_a = tokens[1]
        self.gate_b = tokens[2]
        self.levels = tokens[3]
        self.flags = {'transport': default_transport, 'ntg_proxy': '' }
        for extra in tokens[4:]:
            key, value = extra.split( '=' )
            self.flags[key] = value

        if self.flags['transport'] not in transport_types:
            print "Do not recognize transport type " + self.flags['transport']
            sys.exit(1)
        elif self.flags['transport'] == 'ntg':
            self.flags['ntg_name'] = 'NTG' + str(num_jicd_links)
            num_jicd_links += 1
        elif _is_socket_JICD(self.flags['transport']):
            self.flags['socket_JICD_name'] = 'SOCKET_JICD' + str(num_jicd_links)
            num_jicd_links += 1


class MultiJICDNode:
    def __init__( self, tokens ):
        self.file = tokens[1]
        self.site_id = tokens[2]
        self.port = int(tokens[3])
        self.gate = tokens[4]

class MultiJICDObserver:
    def __init__( self, tokens ):
        self.site_id = tokens[1]
        self.port = int(tokens[2])
        self.gate = tokens[3]

class MultiJICDPeerPropagationOverride:
  def __init__( self, tokens ):
       self.overriding_gate = tokens[1]
       self.config_line = tokens[2]

class MultiJICDNetwork:
    def __init__ ( self, filename ):
        global options
        self.gates = []
        self.nodes = []
        self.observers = []
        self.links = []
        self.peer_propagation_overrides = []
        self.message_switch = None
        import re
        file = open( filename, 'r' )
        line = file.readline()
        while line:
            if( re.search( r'^\s*\n*$', line ) ):
                  line = file.readline()
                  continue
            if ( re.search( r'^\s*#', line ) ):
                while ( re.search( r'\\$', line ) ):
                    line = file.readline()
                line = file.readline()
                continue
            tokens = line.split()
            #print tokens
            if ( tokens[0] == 'mjgate' ):
                self.gates.append( MultiJICDGate( tokens ) )
            elif ( tokens[0] == 'mjlink' ):
                self.links.append( MultiJICDLink( tokens ) )
            elif ( tokens[0] == 'mjnode' ):
                self.nodes.append( MultiJICDNode( tokens ) )
            elif ( tokens[0] == 'mjobserver' ):
                self.observers.append( MultiJICDObserver( tokens ) )
            elif ( tokens[0] == 'message_switch' ):
                assert( not self.message_switch ) # For now, only one message switch can be used at a time.
                self.message_switch = MessageSwitch( tokens )
            elif ( tokens[0] == 'propagation_rule' ):
                self.peer_propagation_overrides.append( MultiJICDPeerPropagationOverride( tokens ) )
            else:
                print "Multi-JICD Unknown entry type:", line
            line = file.readline()

        if self.message_switch == None:
            self.message_switch = MessageSwitch( ['message_switch', 'msg_switch', '/tmp/jicd', str(get_next_auto_port()) ] )


def proj_to_bin ( dir ):
    # Given a directory, return a useable bin directory underneath that, be it
    # backend/run_tree, 4.0-tng/rhel_5_i386, or /h/GEOnet.

    make_bin = "/run_tree/Linux/h/segment/bin"

    if ( os.path.isdir( dir + make_bin ) ):
        return dir + make_bin;

    scons_area = "/../../rhel_5_i386"

    if ( os.path.isdir( dir + scons_area ) ):
        if ( os.path.isdir( dir + scons_area + "/debug" ) ):
            return dir + scons_area + "/debug/modules/backend" + make_bin
        if ( os.path.isdir( dir + scons_area + "/release" ) ):
            return dir + scons_area + "/release/modules/backend" + make_bin
        print dir, "looks like an scons tree, but neither debug nor release is built!"
        sys.exit( 1 )

    # Installed image from RPMs
    if ( os.path.isdir( dir + "/bin" ) ):
        return dir + "/bin"

    print "Can't find a bin directory under", dir
    sys.exit( 1 )

# Maintain old behavior: only add the proxy route for GEOnet gates; not JICD
def write_ntg_gate_file ( gate, **kwargs ):
    ### Setup default arguments. Maintains previous behavior; I've added an "add_routes" value that will
    ### allow me to add the proxy route without setting the farside node ports.
    farside_ntg_listen_ports = ""
    if (kwargs.has_key("farside_ntg_listen_ports")): farside_ntg_listen_ports = kwargs['farside_ntg_listen_ports']

    add_route_to_proxy = False
    if (farside_ntg_listen_ports == ""):    add_route_to_proxy = True
    if (kwargs.has_key('add_proxy_route')): add_route_to_proxy = kwargs['add_proxy_route']

    whitelist_names = []
    if (kwargs.has_key('whitelist_starman')    and kwargs['whitelist_starman']):    whitelist_names.append('starman')
    if (kwargs.has_key('whitelist_jicd_proxy') and kwargs['whitelist_jicd_proxy']): whitelist_names.append('jicd_proxy')

    whitelist_string = ""
    for count in range(0,len(whitelist_names)):
        string_number = str(count+1)
        whitelist_string = whitelist_string + "whitelist." + string_number + ".clientName=" + whitelist_names[count] + "\n"
        whitelist_string = whitelist_string + "whitelist." + string_number + ".ipAddress=127.0.0.1\n"

    ### Done reorganizing default arguments. farside_ntg_listen_ports defaults to "". add_route_to_proxy defaults to False, unless
    ### farside_ntg_listen_ports == "", in which case it defaults to True instead. It can be overridden in either case.

    global options, ntg_bandwidths

    ntg_file_loc = "/tmp/"
    if (options.dry_run or options.debug ):
        print 'Writing ntg.properties for gate in ', ntg_file_loc , ' for port ', farside_ntg_listen_ports
        if (options.dry_run ):
            return

    rpc_server_port=str(int(gate.port) + 40)
    if (rpc_server_port == "5040"):
        rpc_server_port = str(10030)

    f = open( str(ntg_file_loc) + "ntg.properties." + str(gate.port), "w" )
    f.write( '''nodename=''' +gate.site_id+ '''

log.directory=/GEOnet/${nodename}/log

# Supplying an interface type of starman so that we can interface with the HITS gate per the normal method.
interface.type=rpc

interface.rpc.server_port='''+rpc_server_port+'''

nmsg.connectmode=connect

host.hits.minBandwidth='''+str(ntg_bandwidths['min'])+'''
host.hits.maxBandwidth='''+str(ntg_bandwidths['max'])+'''

# What port(s) do we setup to allow other ntgs to connect to us?
local.ntgport='''+str( int(gate.port) + 9 ))
    if (gate.flags['transport'] == 'ntg' and farside_ntg_listen_ports != ""):
        ports = farside_ntg_listen_ports.split(",")
        f.write('''
# Do we wish to connect to other ntgs?  If so, what are their hostname and port
''')
        for i in range(len(ports)):
            farside_port = ports[i]
            f.write("ntg." + str(i) + ".host=127.0.0.1\n")
            f.write("ntg." + str(i) + ".port="+str(int(farside_port) + 9) + "\n")

    f.write('''
pingDelay=5

transitChannel=0

#channel number, names, and bandwidths (in bps)
channelInfo.0.name=transit
channelInfo.0.maxBW='''+str(ntg_bandwidths['channel'])+'''
channelInfo.1.name=audio
channelInfo.1.maxBW='''+str(ntg_bandwidths['channel'])+'''
channelInfo.2.name=commandAndControl
channelInfo.2.maxBW='''+str(ntg_bandwidths['channel'])+'''
channelInfo.3.name=data
channelInfo.3.maxBW='''+str(ntg_bandwidths['channel'])+'''

# Snooper/Intercepter permission list
# In order for a client to snoop or intercept messages, it must be on this permission list.
'''+whitelist_string+'''

# what should the MTU be?
bestMTU=1448''')

    if (add_route_to_proxy):
        f.write('''
# Route Table
# destination can be any perl style regular expression
route.1.destinationUrl='''+gate.flags['ntg_proxy_regex'] + '''
route.1.nextHop='''+gate.flags['ntg_proxy'] + '''
route.1.cost=1
''')


    f.write('''
# Transport manager to use.  Known types are
#    DirectConnect
#    TCP
transportManager TCP
''' )

def write_ntg_node_file ( node, gate  ):
    global options, ntg_bandwidths

    ntg_file_loc = "/tmp/"
    if (options.dry_run or options.debug ):
        print 'Writing ntg.properties for gate in ', ntg_file_loc, ' for port ', node.port
    if (options.dry_run ):
        return

    ntg_rpc_port=str(int(node.port) + 40)
    if (ntg_rpc_port == "5040"):
        ntg_rpc_port = str(10030)

    gate_host = "127.0.0.1"
    if ( gate.flags['ip'] ):
        gate_host = gate.flags['ip']

    f = open( str(ntg_file_loc) + "ntg.properties." + str(node.port), "w" )
    f.write( '''nodename=''' + node.site_id + '''

log.directory=/GEOnet/${nodename}/log

# Supplying an interface type of starman so that we can interface with the HITS gate per the normal method.
interface.type=rpc

interface.rpc.server_port='''+ntg_rpc_port+'''

nmsg.connectmode=connect

host.hits.minBandwidth='''+str(ntg_bandwidths['min'])+'''
host.hits.maxBandwidth='''+str(ntg_bandwidths['max'])+'''

# What port do we setup to allow other ntgs to connect to us?
#local.ntgport = 5107

# Do we wish to connect to other ntgs?  If so, what are their hostname and port
ntg.0.host=''' + gate_host + '''
ntg.0.port='''+str(int(gate.port) + 9)+'''

pingDelay=5

transitChannel=0

channelInfo.0.name=transit
channelInfo.0.maxBW='''+str(ntg_bandwidths['channel'])+'''
channelInfo.1.name=audio
channelInfo.1.maxBW='''+str(ntg_bandwidths['channel'])+'''
channelInfo.2.name=commandAndControl
channelInfo.2.maxBW='''+str(ntg_bandwidths['channel'])+'''
channelInfo.3.name=data
channelInfo.3.maxBW='''+str(ntg_bandwidths['channel'])+'''

# what should the MTU be?
bestMTU=1448

# Route Table
# destination can be any perl style regular expression
route.1.destinationUrl=.*
route.1.nextHop='''+gate.site_id+'''
route.1.cost=1

# Transport manager to use.  Known types are
#    DirectConnect
#    TCP
transportManager TCP
''')

def write_starman_data ( dir, base_port, real_ip ):
    global options
    if ( options.dry_run or options.debug ):
        print 'Writing tm_starman_data.xml in', dir, 'for port', base_port
    if ( options.dry_run ):
        return

    #print "real_ip =", real_ip

    if ( real_ip ):
        ip_addr = real_ip
    else:
        try:
            ip_addr = socket.gethostbyaddr(socket.gethostname())[2][0]
        except:
            print "Gethostbyname failed, falling back to localhost"
            ip_addr = ''

    if ( ip_addr == '' ):
        ip_addr = "127.0.0.1"

    #print "ip_addr =", ip_addr

    f = open( proj_to_bin( str( dir ) ) + "/config/tm_starman_data.xml", "w" )
    f.write( '''<?xml version="1.0" encoding="UTF-8"?>
<!-- edited with XMLSPY v5 rel. 4 U (http://www.xmlspy.com) by Steven Glicker (Ticom Geomatics Inc) -->
<config xmlns="http://www.ticom-geo.com/geonet-config-data" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.ticom-geo.com/geonet-config-data ../../configSchemas/config_data.xsd" name="tm_starman">
	<table name="table">
		<stringColumn name="node">
			<value>localhost</value>
		</stringColumn>
		<booleanColumn name="use" recommended="false">
			<value>true</value>
		</booleanColumn>
		<netAddressColumn name="ip">
			<ipAddress>''' +ip_addr+ '''</ipAddress>
		</netAddressColumn>
		<longColumn name="port" recommended="5007">
''' )
    f.write( "\t\t\t<value>" + str( int(base_port) + 7 ) + "</value>\n" )
    f.write( '''		</longColumn>
	</table>
</config>
''' )

def convert_to_mj_level_str(level):
  level_str = "Unknown"
  if (level == "isLower"): level_str = "hightolow"
  elif (level == "isHigher"): level_str = "lowtohigh"
  elif (level == "normal"): level_str = "normal"
  return level_str

def write_link_con_data ( build_dir, this_gate, far_gate, port ):
    global options
    global FTP_SERVER_DIR

    if ( options.config_only or options.dry_run or options.debug ):
        print 'Writing gate_config.xml in dir', tgt_dir, 'for gate', this_gate.site_id, 'with level', level
    if ( options.dry_run ):
        return

    this_level_str = convert_to_mj_level_str(this_gate.levels)
    far_level_str = convert_to_mj_level_str(far_gate.levels)
    config_str  = "mjgate " + this_gate.site_id + " " + str(this_gate.port) + " " + build_dir + "\n"
    config_str += "mjgate " + far_gate.site_id + " " + str(far_gate.port) + " " + build_dir + "\n"
    config_str += "mjlink " + this_gate.site_id + " " + far_gate.site_id + " " + this_level_str
    config_str +=     " transport=" + this_gate.flags['transport']
    config_str +=     " ntg_proxy=" + this_gate.flags['ntg_proxy']
    config_str +=     "\n"
    config_str += "mjlink " + far_gate.site_id + " " + this_gate.site_id + " " + far_level_str
    config_str +=     " transport=" + far_gate.flags['transport']
    config_str +=     " ntg_proxy=" + far_gate.flags['ntg_proxy']
    config_str +=     "\n"
    f = open("/tmp/runp_mjnet_temp", 'w')
    f.write(config_str)
    f.close()
    mjnet = MultiJICDNetwork("/tmp/runp_mjnet_temp")
    #os.system("rm /tmp/runp_mjnet_temp")

    mjgate = "invalid"
    for gate in mjnet.gates:
      if (gate.site_id == this_gate.site_id): mjgate = gate
    if (mjgate == "invalid"):
      print "Failed to convert gate to mjgate: " + this_gate.site_id + "\n"
      sys.exit(1)
    write_mj_link_con_data(mjgate, mjnet)

def write_proxy_file (message_switch, proxy_gates):
    global options

    ntg_file_loc = "/tmp/"
    if (options.dry_run or options.debug ):
        print 'Writing jicd_proxy.properties for message_switch in ', ntg_file_loc , ' for port ', message_switch.port
        if (options.dry_run ):
            return

    rpc_server_port=str(int(message_switch.port) + 40)
    if (rpc_server_port == "5040"):
        rpc_server_port = str(10030)

    f = open( str(ntg_file_loc) + "jicd_proxy.properties." + str(message_switch.port), "w" )

    proxy_list_separator = " "
    f.write("ntg.host=localhost\n")
    f.write("ntg.port="+str(rpc_server_port)+"\n")

    proxy_list = ""
    for count in range(0, len(proxy_gates)):
        proxy_list = proxy_list + "proxy.gate."+str(count+1)+"="+proxy_gates[count] + "\n"

    
    f.write(proxy_list)
    f.write("base_directory="+message_switch.base_directory+"\n")
    f.write("data_repository_base_directory="+message_switch.base_directory+"\n")
    f.write("data_repository_name=z0gate00\n");
    f.close()
  

def write_geonet_config_files ( network ):
    global options
    global jicd_gate_levels
    global geonet_gate_levels
    if ( network.geonet_gate and int(network.geonet_gate.port) > 0 ):
        write_starman_data( options.geonet_project,
                            network.geonet_gate.port,
                            network.geonet_gate.flags['ip'] )
        for node in network.geonet_nodes:
            if ( 'dir' in node.flags ):
                write_starman_data( node.flags['dir'],
                                    network.geonet_gate.port,
                                    network.geonet_gate.flags['ip'])
        for node in network.real_geonet_nodes:
            if ( 'dir' in node.flags ):
                write_starman_data( node.flags['dir'],
                                    network.geonet_gate.port,
                                    network.geonet_gate.flags['ip'])
        for node in network.geonet_observers:
            if ( 'dir' in node.flags ):
                write_starman_data( node.flags['dir'],
                                    network.geonet_gate.port,
                                    network.geonet_gate.flags['ip'])

    if ( network.geonet_gate and network.jicd_gate ):
        if ( int(network.geonet_gate.port) > 0 ):
            write_link_con_data( options.geonet_project,
                                 network.geonet_gate,
                                 network.jicd_gate,
                                 network.geonet_gate.port )
            copy_config(proj_to_bin(options.geonet_project) + "/config/gate_config.xml",
                        network.geonet_gate.site_id)

def write_ntg_config_files ( network ):
    """Write the NTG config files for all the gates, sensors, and observers"""
    global options, default_transport

    geonet_gate = None
    g_port = options.gate_port
    if( options.gate_site_id and options.gate_port ):
        geonet_gate = Gate( geonet_gate_levels[options.black_level], \
                            [ 'gate', options.gate_site_id, options.gate_port ] )
    elif ( network.geonet_gate
           and int(network.geonet_gate.port) > 0
           and network.geonet_gate.flags['ntg'] == 'true' ):
        geonet_gate = network.geonet_gate

    if( geonet_gate is not None):
        if (network.message_switch):
            use_proxy = (geonet_gate.flags['transport'] == 'ntg')
            write_ntg_gate_file( geonet_gate,farside_ntg_listen_ports=str(network.message_switch.port), add_proxy_route=use_proxy,whitelist_starman=True, whitelist_jicd_proxy=use_proxy)
        else:
            write_ntg_gate_file( geonet_gate, whitelist_starman=True )
        (g_site_id, g_port) = (geonet_gate.site_id, geonet_gate.port)
        for node in network.geonet_nodes:
            write_ntg_node_file( node, geonet_gate )
        for node in network.real_geonet_nodes:
            write_ntg_node_file( node, geonet_gate )
        for node in network.geonet_observers:
            write_ntg_node_file( node, geonet_gate )

    jicd_gate = None
    if( options.jgate_site_id and options.jgate_port ):
        jicd_gate = Gate( jicd_gate_levels[options.black_level], \
                          [ 'gate', options.jgate_site_id, options.jgate_port ] )
    elif ( network.jicd_gate
           and int(network.jicd_gate.port) > 0
           and network.jicd_gate.flags['ntg'] == 'true' ):
        jicd_gate = network.jicd_gate

    if( jicd_gate is not None):
        if (network.message_switch):
            use_proxy = (jicd_gate.flags['transport'] == 'ntg')
            write_ntg_gate_file( jicd_gate,farside_ntg_listen_ports=str(network.message_switch.port), add_proxy_route=use_proxy,whitelist_starman=True, whitelist_jicd_proxy=use_proxy)
        else:
            write_ntg_gate_file( jicd_gate, farside_ntg_listen_ports=str(g_port), whitelist_starman=True )
        (jg_site_id,jg_port) = (network.jicd_gate.site_id,network.jicd_gate.port)
        for node in network.jicd_nodes:
            write_ntg_node_file( node, jicd_gate )
        for node in network.jicd_observers:
            write_ntg_node_file( node, jicd_gate )

    if (network.message_switch and network.message_switch.flags['start_proxy_and_ntg'] == 'true'):
        proxy_gates = []
        have_two_gates = network.geonet_gate and network.jicd_gate
        if ( have_two_gates and network.geonet_gate.flags['transport'] == 'ntg' and network.jicd_gate.flags['transport'] == 'ftp' ):
            proxy_gates.append(network.jicd_gate.site_id)
        if ( have_two_gates and network.geonet_gate.flags['transport'] == 'ftp' and network.jicd_gate.flags['transport'] == 'ntg'):
            proxy_gates.append(network.geonet_gate.site_id)
        write_ntg_gate_file( network.message_switch, add_proxy_route=False, whitelist_jicd_proxy=True )
        write_proxy_file( network.message_switch, proxy_gates )


def write_jicd_config_files ( network ):
    global options
    global jicd_gate_levels
    global geonet_gate_levels

    if ( network.jicd_gate and int(network.jicd_gate.port) > 0 ):
        write_starman_data( options.jicd_project,
                            network.jicd_gate.port,
                            network.jicd_gate.flags['ip'])
        for node in network.jicd_nodes:
            if ( 'dir' in node.flags ):
                write_starman_data( node.flags['dir'],
                                    network.jicd_gate.port,
                            network.jicd_gate.flags['ip'] )
        for node in network.jicd_observers:
            if ( 'dir' in node.flags ):
                write_starman_data( node.flags['dir'],
                                    network.jicd_gate.port,
                            network.jicd_gate.flags['ip'] )

    if ( network.geonet_gate and network.jicd_gate ):
        if ( int(network.jicd_gate.port) > 0 ):
            write_link_con_data( options.jicd_project,
                                 network.jicd_gate,
                                 network.geonet_gate,
                                 network.jicd_gate.port )
            copy_config(proj_to_bin(options.jicd_project) + "/config/gate_config.xml",
                        network.jicd_gate.site_id)


def xterm_options ( title, cmd ):
    global options
    answer = " -geometry 200x25 -ls" + options.iconic + " -sl 100000" + " -T \"" + title + "\"" + " -e \"" + cmd + "\""
    if ( options.debug ):
        print "  : ", answer
    return answer

def do_command ( title, site_id, bindir, cmd ):
    global options
    os.chdir( bindir )
    if ( options.sleep_after ):
        cmd += ' ; sleep 1d'

    if ( options.debug or options.dry_run ):
        print 'Doing:  ', cmd, 'from', os.getcwd()

    if ( options.dry_run ):
        return

    if ( options.foreground ):
        os.system( cmd )
    elif ( options.no_xterm ):
        os.system(  cmd + ' &' )
    else:
        os.system( 'xterm '
                   + xterm_options( title + ' ' + site_id + ' ' + bindir, cmd )
                   + ' &' )


def start_tm ( site_id, bindir, mode, port, title, flags ):
    global options
    if ( options.dcs_only ):
        return

    print site_id, ': ',
    for k, v in flags.iteritems():
        print k, '->', v, ',',
    print 'port ->', port

    if ( 'dir' in flags ):
        bindir = proj_to_bin( flags['dir'] )
    if ( 'GEONET_OLD_TM_SIMULATION' in os.environ ):
        del os.environ['GEONET_OLD_TM_SIMULATION']
    if ( flags['ntg'] == "false" ):
        os.environ['GEONET_OLD_TM_SIMULATION'] = str(1)
    elif ( int(port) == 5000 ):
        #respect default NTG port for offset 5000 (for ML compatibility)
        os.environ['GEONET_NTG_SERVER_PORT'] = str(10030)
    else:
        os.environ['GEONET_NTG_SERVER_PORT'] = str(int(port) + 40)
    #print "for site",site_id,"port",port,"GEONET_NTG_SERVER_PORT=",os.environ['GEONET_NTG_SERVER_PORT']
    geonet_data = "/GEOnet/" + site_id
    os.environ['SLOG_SOCKET_PATH'] = geonet_data + "/runtime/slog_socket"
    if ( options.hits_environment ):
        os.environ['HITS_BASE_PORT']   = str( port )
    else:
        os.environ['GEONET_BASE_PORT'] = str( port )
    if ( options.debug ):
        print "On port", port, ":"
    do_command( title, site_id, bindir, 'GEONET_NO_GCS_SAUDIO=1 ./run_tm -i ' + site_id + ' -c ' + mode )

def start_ntg ( site_id, config_file ):
    global options

    if ( options.dcs_only ):
        return

    bindir = options.ntg_tree + "/bin"

    print "starting NTG in ", bindir, " with config file ", config_file

    if ( options.save_ntg_log ):
        quiet_ntg = '>/tmp/' + site_id + '.ntg.log 2>&1'
    else:
        quiet_ntg = '>/dev/null 2>&1'

    do_command("NTG", site_id, bindir, './NetworkTrafficGovernor ' + config_file + quiet_ntg)

    time.sleep(1)

def start_proxy( site_id, config_file ):
    global options
    if (options.dcs_only):
      return

    bindir = options.jicd_proxy_bin_dir + '/run_tree/Linux/h/segment/bin/'
    print "writing jicd_proxy log4cxx properties in " + bindir + "/../config/"
    os.system("mkdir -p "+bindir+'/../config')

    f = open(bindir + "/../config/log4cxx_jicd.properties", "w")
    f.write('''
file.pattern=LOG:%-5p %d{ISO8601}(%c{2})%F,%L: - %m%n

log4j.rootLogger=DEBUG, PATTERN_FILE

log4j.appender.PATTERN_FILE=org.apache.log4j.RollingFileAppender
log4j.appender.PATTERN_FILE.layout=org.apache.log4j.PatternLayout
log4j.appender.PATTERN_FILE.layout.ConversionPattern=${file.pattern}
log4j.appender.PATTERN_FILE.File=/tmp/jicd_proxy.log
log4j.appender.PATTERN_FILE.MaxBackupIndex=6
log4j.appender.PATTERN_FILE.MaxFileSize=10000KB
log4j.logger.org=ERROR
''')
    f.close()


    print "starting jicd_proxy in ", bindir, " with config file ", config_file

    # Note: log messages will be logged to the file specified in the config file above (/tmp/jicd_proxy.log)
    quiet_jicd_proxy = '>/dev/null 2>&1'
    do_command("jicd_proxy", site_id, bindir, 'JICD_PROXY_USE_FLAT_DIRECTORY_STRUCTURE=1 ./jicd_proxy ' + config_file + quiet_jicd_proxy)

def start_soft_dcs ( site_id, bindir, port, file ):
    global options

    if ( file == "none" ):
        file = "-austin 1"

    portstr = str( int( port ) + 1 )
    if ( options.hits_environment ):
        os.environ['HITS_TM_CLIENT']   = 'c,localhost:' + portstr
    else:
        os.environ['GEONET_TM_CLIENT'] = 'c,localhost:' + portstr
    os.environ['LD_LIBRARY_PATH'] = bindir + '/../lib'
    cmd = './soft_dcs'
    if ( options.soft_dcs ):
        cmd += ' ' + options.soft_dcs
    cmd += ' ' + file

    if ( options.double_collect ):
        cmd = cmd  + ' ' + file

    if ( os.fork() ):
        return

    time.sleep( 10 )

    do_command( 'DCS for ', site_id, bindir, cmd )

    sys.exit( 0 )

def start_dcs_clone ( site_id, bindir, port, source_site_id, extra_tacticals, distance_to_emitter, extra_tacticals_created ):
    global options

    os.environ['LD_LIBRARY_PATH'] = bindir + '/../lib'
    os.environ['DCS_CLONE_POSITION_EXTRA_TACTICALS'] = str(extra_tacticals)
    os.environ['DCS_CLONE_DISTANCE_TO_EMITTER'] = str(distance_to_emitter)
    os.environ['DCS_CLONE_SOURCE_SITE_ID'] = source_site_id
    os.environ['DCS_CLONE_POSITION_INDEX'] = str(extra_tacticals_created)
    os.environ['DCS_CLONE_TARGET_HOST'] = 'localhost'
    os.environ['DCS_CLONE_TARGET_BASE_PORT'] = str( int( port ) )
    cmd = './dcs_clone'
    if ( options.dcs_clone ):
        cmd += ' ' + options.dcs_clone

    if ( os.fork() ):
        return

    time.sleep( 10 )

    do_command( 'DCS for ', site_id, bindir, cmd )

    sys.exit( 0 )

def start_dcs ( site_id, bindir, port ):
    global options

    portstr = str( int( port ) + 1 )
    if ( options.hits_environment ):
        os.environ['HITS_TM_CLIENT']   = 'c,localhost:' + portstr
    else:
        os.environ['GEONET_TM_CLIENT'] = 'c,localhost:' + portstr
    os.environ['LD_LIBRARY_PATH'] = bindir + '/../lib'
    cmd = './run_dcs'
    if ( options.dcs ):
        cmd += ' ' + options.dcs

    if ( os.fork() ):
        return

    time.sleep( 10 )

    do_command( 'DCS for ', site_id, bindir, cmd )

    sys.exit( 0 )

def start_gate ( site_id, bindir, port, title ):
    global options
    "Start the extra stuff for a gate"

    if ( options.dcs_only ):
        return

    geonet_data = "/GEOnet/" + site_id
    os.environ['SLOG_SOCKET_PATH'] = geonet_data + "/runtime/slog_socket"
    if ( options.hits_environment ):
        os.environ['HITS_SITE_ID']   = site_id
        os.environ['HITS_BASE_PORT']   = str( port )
    else:
        os.environ['GEONET_SITE_ID'] = site_id
        os.environ['GEONET_BASE_PORT'] = str( port )

    if ( options.start_processor ):
      do_command( title + ' MGW ',
                  site_id,
                  bindir,
                  'SLOG_LOG_TO_CONSOLE=y ./run_mgw > /tmp/mgw.log' )

    if not options.gate_only:
        do_command( title + ' *man ', site_id, bindir, './run_starman' )


def start_ntgs ( network ):
    if ( network.message_switch and network.message_switch.flags['start_proxy_and_ntg'] == 'true' and int(network.message_switch.port) > 0 ):
        # If the connections are asymmetric, there may be some setup required for the proxy directories.
        # jicd_proxy now sets these up, so rather than create the proxy directory, we sanity check ftp directories
        if ( network.geonet_gate and network.jicd_gate ):
            if (network.geonet_gate.flags['transport'] == 'ntg' and network.jicd_gate.flags['transport'] == 'ftp'):
                check_ftp_dir(network.message_switch, network.jicd_gate.site_id)
            elif(network.jicd_gate.flags['transport'] == 'ntg' and network.geonet_gate.flags['transport'] == 'ftp'):
                check_ftp_dir(network.message_switch, network.geonet_gate.site_id)
        # Now that everything's set up, start the proxy.
        start_proxy(network.message_switch.site_id, "/tmp/jicd_proxy.properties." + str(network.message_switch.port))
        start_ntg(network.message_switch.site_id, "/tmp/ntg.properties." + str(network.message_switch.port))

    if not options.gate_only:
        for node in network.geonet_nodes:
            if ( node.flags['ntg'] == 'true' ):
              start_ntg(node.site_id, "/tmp/ntg.properties." + str(node.port))
        for node in network.real_geonet_nodes:
            if ( node.flags['ntg'] == 'true' ):
              start_ntg(node.site_id, "/tmp/ntg.properties." + str(node.port))
        for node in network.geonet_observers:
            if ( node.flags['ntg'] == 'true' ):
              start_ntg(node.site_id, "/tmp/ntg.properties." + str(node.port))
    if ( network.geonet_gate
         and int(network.geonet_gate.port) > 0
         and network.geonet_gate.flags['ntg'] == 'true'
         and not network.geonet_gate.flags['ip'] ):
        start_ntg(network.geonet_gate.site_id, "/tmp/ntg.properties." + str(network.geonet_gate.port))

    if not options.gate_only:
        for node in network.jicd_nodes:
            if ( node.flags['ntg'] == 'true' ):
              start_ntg(node.site_id, "/tmp/ntg.properties." + str(node.port))
        for node in network.jicd_observers:
            if ( node.flags['ntg'] == 'true' ):
              start_ntg(node.site_id, "/tmp/ntg.properties." + str(node.port))

    if ( network.jicd_gate
         and int(network.jicd_gate.port) > 0
         and network.jicd_gate.flags['ntg'] == 'true'
         and not network.jicd_gate.flags['ip']  ):
        start_ntg(network.jicd_gate.site_id, "/tmp/ntg.properties." + str(network.jicd_gate.port))


def start_geonet_nodes ( network ):

    if ( options.hits_environment ):
        os.environ['HITS_POST_PROC_FILTER_FILENAMES']   = "yes";
        os.environ['HITS_BYPASS_TICKET']   = "yes";
        os.environ['HITS_CONNECT_TO_STARMAN']   = "yes";
        os.environ['HITS_ALLOW_MULTIPLE_TMS']   = "yes";
        if ( not options.no_connect_all ):
            os.environ['HITS_STARMAN_CONNECT_ALL']   = "yes";
    else:
        os.environ['GEONET_POST_PROC_FILTER_FILENAMES'] = "yes";
        os.environ['GEONET_BYPASS_TICKET'] = "yes";
        os.environ['GEONET_CONNECT_TO_STARMAN'] = "yes";
        os.environ['GEONET_ALLOW_MULTIPLE_TMS'] = "yes";
        os.environ['GEONET_ALLOW_MULTIPLE_MGWS'] = "yes";
        if ( not options.no_connect_all ):
            os.environ['GEONET_STARMAN_CONNECT_ALL'] = "yes";

    os.environ['SMART_STARMAN_CHECK'] = "yes";

    if (network.geonet_gate and network.geonet_gate.flags['transport'] == 'socket_JICD_sink'):
        jicd_listen_port = str(network.geonet_gate.port+56)
        print "Setting GEONET_SOCKET_JICD_LISTEN_PORT to " + jicd_listen_port
        os.environ['GEONET_SOCKET_JICD_LISTEN_PORT'] = jicd_listen_port

    dcs_clone_dir = proj_to_bin( options.geonet_project )
    if ( options.dcs_clone_dir ):
        dcs_clone_dir = proj_to_bin( options.dcs_clone_dir )

    if not options.gate_only:
        for node in network.geonet_nodes:

            soft_dcs_dir = proj_to_bin( options.geonet_project )
            if ( options.soft_dcs_dir ):
                soft_dcs_dir = proj_to_bin( options.soft_dcs_dir )
            if ( options.native_soft_dcs and 'dir' in node.flags ):
                soft_dcs_dir = proj_to_bin( node.flags['dir'] )
                print node.site_id, 'soft_dcs from', node.flags['dir']


            start_tm( node.site_id,
                      proj_to_bin( options.geonet_project ),
                      "hits_dcs",
                      node.port,
                      "GEOnet",
                      node.flags )
            if node.__class__.__name__ not in ['NoSensor', 'ClonedSensor']:
                start_soft_dcs( node.site_id,
                                soft_dcs_dir,
                                node.port,
                                node.file )
            elif node.__class__.__name__ == 'ClonedSensor':
                start_dcs_clone( node.site_id,
                                 dcs_clone_dir,
                                 node.port,
                                 node.source_site_id,
                                 network.extra_tacticals,
                                 network.extra_tacticals_distance_to_emitter,
                                 network.extra_tacticals_created )
                network.extra_tacticals_created += 1
        for node in network.real_geonet_nodes:
            start_tm( node.site_id,
                      proj_to_bin( options.geonet_project ),
                      "hits_dcs",
                      node.port,
                      "GEOnet",
                      node.flags )
            start_dcs( node.site_id,
                       proj_to_bin( options.geonet_project ),
                       node.port )

        for node in network.geonet_observers:
            start_tm( node.site_id,
                      proj_to_bin( options.geonet_project ),
                      "observer",
                      node.port,
                      "GEOnet Observer",
                      node.flags)

    if ( network.geonet_gate
         and int(network.geonet_gate.port) > 0
         and not network.geonet_gate.flags['ip'] ):
        start_tm( network.geonet_gate.site_id,
                  proj_to_bin( options.geonet_project ),
                  "hits_nsp",
                  network.geonet_gate.port,
                  "GEOnet Gate",
                  network.geonet_gate.flags )
        start_gate( network.geonet_gate.site_id,
                    proj_to_bin( options.geonet_project ),
                    network.geonet_gate.port,
                    "GEOnet Gate" )


def start_jicd_nodes ( network ):

    if ( options.hits_environment ):
        os.environ['HITS_POST_PROC_FILTER_FILENAMES']   = "yes";
        os.environ['HITS_BYPASS_TICKET']   = "yes";
        os.environ['HITS_CONNECT_TO_STARMAN']   = "yes";
        if ( not options.no_connect_all ):
            os.environ['HITS_STARMAN_CONNECT_ALL']   = "yes";
        os.environ['HITS_ALLOW_MULTIPLE_TMS']   = "yes";
    else:
        os.environ['GEONET_POST_PROC_FILTER_FILENAMES'] = "yes";
        os.environ['GEONET_BYPASS_TICKET'] = "yes";
        os.environ['GEONET_CONNECT_TO_STARMAN'] = "yes";
        if ( not options.no_connect_all ):
            os.environ['GEONET_STARMAN_CONNECT_ALL'] = "yes";
        os.environ['GEONET_ALLOW_MULTIPLE_TMS'] = "yes";
        os.environ['GEONET_ALLOW_MULTIPLE_MGWS'] = "yes";

    os.environ['SMART_STARMAN_CHECK'] = "yes";

    if (network.jicd_gate and network.jicd_gate.flags['transport'] == 'socket_JICD_sink'):
        jicd_listen_port = str(network.jicd_gate.port+56)
        print "Setting GEONET_SOCKET_JICD_LISTEN_PORT to " + jicd_listen_port
        os.environ['GEONET_SOCKET_JICD_LISTEN_PORT'] = jicd_listen_port

    if not options.gate_only:
        for node in network.jicd_nodes:
            start_tm( node.site_id,
                      proj_to_bin( options.jicd_project ),
                      "hits_dcs",
                      node.port,
                      "JICD",
                      node.flags )

            soft_dcs_dir = proj_to_bin( options.jicd_project )
            if ( options.soft_dcs_dir ):
                soft_dcs_dir = proj_to_bin( options.soft_dcs_dir )

            start_soft_dcs( node.site_id,
                            soft_dcs_dir,
                            node.port,
                            node.file )

        for node in network.jicd_observers:
            start_tm( node.site_id,
                      proj_to_bin( options.jicd_project ),
                      "observer",
                      node.port,
                      "JICD Observer",
                      node.flags )


    if ( network.jicd_gate and int(network.jicd_gate.port) > 0 ):
        start_tm( network.jicd_gate.site_id,
                  proj_to_bin( options.jicd_project ),
                  "hits_nsp",
                  network.jicd_gate.port,
                  "JICD Gate",
                  network.jicd_gate.flags )
        start_gate( network.jicd_gate.site_id,
                    proj_to_bin( options.jicd_project ),
                    network.jicd_gate.port,
                    "JICD Gate" )

def get_relclass( level ):
  if( level == "normal" ):
      return "normal"
  elif( level == "hightolow" ):
      return "isLower"
  elif( level == "lowtohigh" ):
      return "isHigher"
  elif( level == "blacktolow" ):
      return "isRestrictedLower"
  else:
      print "Unknown JICD link level: ", level
  return "Unknown"

def is_black_gate(mjgate, mjnet):
  mjlinks = mjnet.links
  for mjlink in mjlinks:
    if( mjlink.gate_a == mjgate.site_id ):
      if mjlink.levels == "blacktolow": return 1
  return 0

def write_mj_link_con_data ( mjgate, mjnet ):
    """Create the gate_config.xml file for a gate in a multi-jicd setup"""
    global FTP_SERVER_DIR
    mjlinks = mjnet.links
    linkCount = 0
    for mjlink in mjlinks:
        if( mjlink.gate_a == mjgate.site_id ):
            linkCount = linkCount + 1
    os.chdir( proj_to_bin( mjgate.path ) + "/config" )
    f = open( "gate_config.xml", "w" )
    f.write( "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n" )
    f.write( "<config>\n\n" )
    f.write( "\t<local_gate_settings>\n" )
    if is_black_gate(mjgate,mjnet): f.write("\t\t<black_gate>true</black_gate>\n")
    f.write( "\t\t<classification_level>Unclassified</classification_level>\n" )
    f.write( "\t\t<classification_compartment/>\n" )
    f.write( "\t</local_gate_settings>\n\n" )
    f.write( "\t<link_propagations use_legacy_propagation_rules=\"true\">\n" )
    for override in mjnet.peer_propagation_overrides:
      if (override.overriding_gate == mjgate.site_id):
        line = override.config_line.split("=")
        source = line[0]
        for target in line[1].split(","):
          f.write("\t\t<propagation_rule first=\""+source+"\" second=\""+target+"\"/>\n")
    f.write( "\t</link_propagations>\n\n" )

    f.write( "\t<links>\n" )
    if ( options.data_repository ):
        f.write( "\t\t<data_repository_link id=\"z0gate00\">\n" )
        f.write( "\t\t\t<send connection_ref_id=\"MyFTP\"/>\n" )
        f.write( "\t\t\t<recv connection_ref_id=\"MyFTP\"/>\n" )
        f.write( "\t\t</data_repository_link>\n\n" )

    ftp_relclasses = set()
    for mjlink in mjlinks:
        if( mjlink.gate_a == mjgate.site_id ):
            r = get_relclass(mjlink.levels)
            transport_name = _get_just_transport_name(mjlink.flags)
            if (transport_name == "FTP"): ftp_relclasses.add(r) # remember relclasses for later
            if (transport_name == "FTP"): transport_name = "MyFTP_" + r
            metrics="true"
            for gate in mjnet.gates:
              if (gate.site_id == mjlink.gate_b):
                metrics = gate.flags['supportsMetrics']
            f.write( "\t\t<gate_link id=\"" + mjlink.gate_b + "\" supports_metrics=\""+metrics+"\" " \
                     +               "has_IQ=\"true\" has_extend=\"true\" has_retune=\"true\">\n" )
            f.write( "\t\t\t<send connection_ref_id=\"" + transport_name + "\" />\n" )
            f.write( "\t\t\t<recv connection_ref_id=\"" + transport_name + "\" />\n" )
            f.write( "\t\t</gate_link>\n\n" )

    f.write( "\t</links>\n\n" )
    f.write( "\t<connections>\n" )

    if (options.data_repository):
      f.write( "\t\t<connection id=\"MyFTP\" relclass=\"normal\">\n" )
      f.write( "\t\t\t<ftp passive=\"true\" dirmirror=\"true\" simultaneous_connections=\"2\">\n" )
      f.write( "\t\t\t\t<host>"+options.ftp_server+"</host>\n" )
      f.write( "\t\t\t\t<user>flink</user>\n" )
      f.write( "\t\t\t\t<password>7=:?&lt;E6DE</password>\n" )
      f.write( "\t\t\t\t<directory>"+FTP_SERVER_DIR+"</directory>\n" )
      f.write( "\t\t\t</ftp>\n" )
      f.write( "\t\t</connection>\n\n" )

    for r in ftp_relclasses:
      f.write( "\t\t<connection id=\"MyFTP"+"_"+r+"\" relclass=\""+r+"\">\n" )
      f.write( "\t\t\t<ftp passive=\"true\" dirmirror=\"true\" simultaneous_connections=\"2\">\n" )
      f.write( "\t\t\t\t<host>"+options.ftp_server+"</host>\n" )
      f.write( "\t\t\t\t<user>flink</user>\n" )
      f.write( "\t\t\t\t<password>7=:?&lt;E6DE</password>\n" )
      f.write( "\t\t\t\t<directory>"+FTP_SERVER_DIR+"</directory>\n" )
      f.write( "\t\t\t</ftp>\n" )
      f.write( "\t\t</connection>\n\n" )

    f.write(_create_mj_ntg_con_table(mjgate, mjlinks))
    f.write(_create_mj_socket_jicd_con_table(mjgate, mjnet))

    f.write("\t</connections>\n\n")
    f.write("</config>\n")
    f.close()

def _get_transport_type(link_info):
    transport_type = "\t\t\t<value>"
    if link_info['transport'] == 'ftp':
        transport_type += "ftp"
    elif link_info['transport'] == 'ntg':
        transport_type += "ntg"
    elif _is_socket_JICD(link_info['transport']):
        transport_type += "socket JICD"
    else:
        print "Don't recognize transport type " + link_info['transport']
    transport_type += "</value>\n"
    return transport_type

def _get_just_transport_name(link_info):
    if link_info['transport'] == 'ftp':
        return "FTP"
    elif link_info['transport'] == 'ntg':
        if (link_info.has_key('ntg_name')): return link_info['ntg_name']
        else:                               return 'NTG'
    elif _is_socket_JICD(link_info['transport']):
        if (link_info.has_key('socket_JICD_name')): return link_info['socket_JICD_name']
        else:                                       return 'SOCKET_JICD'
    else:
        print "Don't recognize transport type " + link_info['transport']
    return "Unknown"

def _get_transport_name(link_info):
    return "\t\t\t<value>My" + _get_just_transport_name + "</value>\n"

def _create_mj_ntg_con_table(gate, links):
    """Helper function to create the ntg_con table for a multi-jicd environment"""
    ntg_links = []
    for link in links:
        if gate.site_id == link.gate_a and link.flags['transport'] == 'ntg':
            ntg_links.append(link)
    ntg_con_table = ""
    for link in ntg_links:
        ntg_con_table += "\t\t<connection id=\""+link.flags['ntg_name']+"\"" + \
                         " relclass=\"" + get_relclass(link.levels) + "\">\n"
        ntg_con_table += "\t\t\t<ntg>\n"
        ntg_con_table += "\t\t\t\t<host>localhost</host>\n"
        rpc_server_port=str(int(gate.port) + 40)
        if (rpc_server_port == "5040"):
          rpc_server_port = str(10030)
        ntg_con_table += "\t\t\t\t<port>"+rpc_server_port+"</port>\n"
        ntg_con_table += "\t\t\t\t<proxy_name>" + link.flags['ntg_proxy'] + "</proxy_name>\n"
        ntg_con_table += "\t\t\t</ntg>\n"
        ntg_con_table += "\t\t</connection>\n\n"
    return ntg_con_table

def _create_mj_socket_jicd_con_table(gate, network):
    """Helper function to create the def_socket_con table for a multi-jicd environment"""
    links = network.links
    def_links = []
    for link in links:
        if gate.site_id == link.gate_a and _is_socket_JICD(link.flags['transport']):
            def_links.append(link)
    def_con_table = ""
    for link in def_links:
        def_con_table += "\t\t<connection id=\""+link.flags['socket_JICD_name']+"\"" + \
                         " relclass=\"" + get_relclass(link.levels) + "\">\n"
        def_con_table += "\t\t\t<socketJICD>\n"
        def_con_table += "\t\t\t\t<host>localhost</host>\n"
        server_port = str(int(gate.port)+56)
        # if this gate is the source, use the sink's port
        if (link.flags['transport'] == 'socket_JICD_source'):
            for g in network.gates:
                if (g.site_id == link.gate_b):
                    server_port = str(int(g.port)+56)
                    if (g.port == 0): server_port = "7056" # maintain existing behavior for jicd_testbed
        def_con_table += "\t\t\t\t<port>"+server_port+"</port>\n"
        def_con_table += "\t\t\t\t<listen>" + str(link.flags['transport'] == 'socket_JICD_sink').lower() + "</listen>\n"
        def_con_table += "\t\t\t</socketJICD>\n"
        def_con_table += "\t\t</connection>\n\n"
    return def_con_table

def write_mj_runp_config ( mjgate, mjnodes, mjobservers, msg_switch, use_default_proxy, link_map ):
    os.chdir( "/tmp" )
    f = open( "runp." + mjgate.site_id + ".config", "w" )
    f.write( "#Generated runp config for multi-JICD setup\n" )
    f.write( "#Parent: " + options.config_file + "\n" )

    output_type = ''

    # If there are multiple output types, ntg with proxy should win.
    for key, value in link_map[mjgate.site_id].iteritems():
      if (output_type != 'ntg'): output_type = value

    assert(output_type != '')

    extra_gate_options = ""
    if use_default_proxy:
      global JICD_PROXY_REGEX
      if (output_type == 'socket_JICD_sink'): extra_gate_options += " transport=socket_JICD_sink"
      elif (output_type == 'socket_JICD_source'): extra_gate_options += " transport=socket_JICD_source"
      elif (output_type == 'ftp'): extra_gate_options += " transport=ftp"
      else: extra_gate_options += " ntg_proxy=" + msg_switch.site_id + " ntg_proxy_regex="+JICD_PROXY_REGEX

    for flag in mjgate.flags.items():
      extra_gate_options += " " + flag[0] + "=" + flag[1]
    extra_gate_options += "\n"

    f.write( "gate " + mjgate.site_id + " " + str(mjgate.port) + extra_gate_options)
    for mjnode in mjnodes:
        if( mjnode.gate == mjgate.site_id ):
            f.write("node " + mjnode.file + " " + mjnode.site_id + " " + str(mjnode.port) + "\n")
    for mjobserver in mjobservers:
        if( mjobserver.gate == mjgate.site_id ):
            f.write("observer " + mjobserver.site_id + " " + str(mjobserver.port) + "\n")

    msg_switch_str = "message_switch " + msg_switch.site_id + " " + msg_switch.base_directory + " " + str(msg_switch.port) + " start_proxy_and_ntg=false\n"

    f.write(msg_switch_str + "\n")
    f.close()

def check_ftp_dir(msg_switch, ftp_gate):
    global FTP_SERVER_DIR
    expected = options.ftp_server + ":" + FTP_SERVER_DIR
    search_command = "df "+msg_switch.base_directory+" | head -n 2 | tail -n 1 | grep -o '^"+expected+"$' | wc -l"
    is_mounted = os.system("exit `"+search_command+"`")
    if (not is_mounted):
        print "ERROR: Detected ftp gates that need to be proxied for the message switch, but the jicd proxy directory ("+msg_switch.base_directory+") is not mounted to the ftp server directory ("+FTP_SERVER_DIR+" on "+options.ftp_server+")"
        print "(expected "+search_command+" to print 1)"
        print "Recommend: sudo mount "+options.ftp_server+":"+FTP_SERVER_DIR+" "+msg_switch.base_directory
        sys.exit(1)
    print "Identified FTP gate that need to be proxied: ", ftp_gate, ". FTP server location appears to be mounted properly."

def launch_mj_runps ( mjnet ):
    global options
    do_delay = False
    for mjgate_a in mjnet.gates:
        for mjgate_b in mjnet.gates:
            if(mjgate_a != mjgate_b and mjgate_a.path == mjgate_b.path):
                do_delay = True
    is_jicd_gate = True

    no_ntg_proxy = True
    link_map = dict()
    for mjgate in mjnet.gates: link_map[mjgate.site_id] = dict()
    for link in mjnet.links:
        if (link.flags['ntg_proxy'] != ""): no_ntg_proxy = False
        try: link_map[link.gate_a][link.gate_b] = link.flags['transport']
        except KeyError: print "Link with a gate (" + link.gate_a + ") that does not exist!"

    # alias the message switch. For now, only one can exist.
    msg_switch = mjnet.message_switch

    if (no_ntg_proxy):
      for i in range(0,len(mjnet.links)):
          mjnet.links[i].flags['ntg_proxy'] = msg_switch.site_id

    proxy_gate_set = set()
    for mjlink in mjnet.links:
        try:
          # First, verify socket JICD configurations make sense
          if (link_map[mjlink.gate_a][mjlink.gate_b] == 'socket_JICD_sink'):
            assert(link_map[mjlink.gate_b][mjlink.gate_a] == 'socket_JICD_source')
          if (link_map[mjlink.gate_a][mjlink.gate_b] == 'socket_JICD_source'):
            assert(link_map[mjlink.gate_b][mjlink.gate_a] == 'socket_JICD_sink')
        except:
          print "Link with a non-existent gate is preventing verification of socket JICD setup"

        try:
          # Second, check for ntg->ftp connections. In that case, we need to set up the inbox (message switch would do it in a real environment)
          if (link_map[mjlink.gate_a][mjlink.gate_b] == 'ntg' and
              link_map[mjlink.gate_b][mjlink.gate_a] == 'ftp'):
              if (not options.config_only):
                  check_ftp_dir(msg_switch, mjlink.gate_b)
                  proxy_gate_set.add(mjlink.gate_b)
        except:
          print "Link with non-existent gate is preventing proxy_gate determination"

    # Set up the proxy properties file and the proxy's NTG properties, then start the proxy and it's NTG
    write_ntg_gate_file( msg_switch, add_proxy_route=False, whitelist_jicd_proxy=True )
    write_proxy_file( msg_switch, list(proxy_gate_set) )
    if (not options.config_only):
        start_proxy(msg_switch.site_id, "/tmp/jicd_proxy.properties." + str(msg_switch.port))
        start_ntg(msg_switch.site_id, "/tmp/ntg.properties." + str(msg_switch.port))

    # All done with initial setup. Kick off runp again in non-multi-jicd mode for each gate
    for i in range(len(mjnet.gates)):
        mjgate = mjnet.gates[i]
        print "writing configs for gate", mjgate.site_id
        write_mj_link_con_data( mjgate, mjnet )
        copy_config(proj_to_bin( mjgate.path ) + "/config/gate_config.xml", mjgate.site_id)
        write_mj_runp_config( mjgate, mjnet.nodes, mjnet.observers, msg_switch, no_ntg_proxy, link_map )
        print "launching runp for gate", mjgate.site_id
        command = proj_to_bin( mjgate.path ) + "/tools/runp"
        command += " -p " + mjgate.path
        command += " -c /tmp/runp." + mjgate.site_id + ".config"
        command += " -n " + options.ntg_tree
        command += " -f " + options.ftp_server
        #pass through appropriate command line options
        if is_jicd_gate:
            geonet_gates = _get_geonet_ports(mjnet, mjgate)
            command += " --far-side-ntg -j " + mjgate.path
            if (geonet_gates): gate_port_string = " --gate-port " + geonet_gates
        if( options.lan_mode ):
            command += " --lan"
        if( options.soft_dcs and len(options.soft_dcs) ):
            command += " --soft-dcs-options '" + options.soft_dcs + "'"
        if( options.dcs and len(options.dcs) ):
            command += " --dcs-options '" + options.dcs + "'"
        if( options.config_only ):
            command += " --config-only"
        if( options.gate_only ):
            command += " --gate-only"
        if( options.dry_run ):
            command += " --dry-run"
        if( options.double_collect ):
            command += " -2"
        if( options.save_ntg_log ):
            command += " --save-ntg-log"
        if( options.no_xterm ):
            command += " -x"
        if( options.iconic == " " ):
            command += " --no-icon"
        if( options.debug ):
            command += " -d"
        if( options.foreground ):
            command += " --foreground"
        if( options.sleep_after ):
            command += " -s"
        if( options.verbose ):
            command += " -v"
        if( options.hits_environment ):
            command += " --hits-environment"
        if( options.old_mgm ):
            command += " --old-mgm"
        print command
        #JICD Wait
        os.system(command)
        if(do_delay):
            time.sleep( 1.0 * options.jicd_wait )
        is_jicd_gate = not is_jicd_gate

    if (options.validate):
      perform_validation([x.site_id for x in mjnet.gates])
      global RUNP_LINK_CON_PATH

    #os.system("rm -rf " + RUNP_LINK_CON_PATH)

    return

#need to remember what pairs of ports have been used so you don't try to set up
#a connection from A to B and then B to A
port_pairs = []
def _get_geonet_ports(mjnet, mjgate):
    """Helper function for launch_mj_runps. Figures out
       which gate's (or gates') port(s) a far-side gate will want to connect to."""
    #figure out which ports have already been connected to the local gate's port
    #so they're not connected the other direction
    global port_pairs
    ports_not_to_connect_to = []
    for pair in port_pairs:
        if pair[0] == mjgate.port:
            ports_not_to_connect_to.append(pair[1])
        elif pair[1] == mjgate.port:
            ports_not_to_connect_to.append(pair[0])

    gates_to_connect_to = []
    for link in mjnet.links:
        if link.gate_a == mjgate.site_id:
            gates_to_connect_to.append(link.gate_b)

    ports_to_connect_to = []
    for gate_name in gates_to_connect_to:
        for gate in mjnet.gates:
            if gate_name == gate.site_id and gate.port not in ports_not_to_connect_to:
                ports_to_connect_to.append(str(gate.port))
                port_pairs.append([mjgate.port, gate.port])
    comma = ","
    ports = comma.join(ports_to_connect_to)
    return ports





def instructions ():
    print '''  runp runs several sensor layer nodes on your local machine,
as specified by a configuration file.  You can run soft_dcs nodes, observers,
gates, and JICD nodes all from a single command line.  It will write out
whatever configuration files are necessary to set up your network, but
it does not run any mission layers.

  The configuration file (~/etc/runp by default) looks like this:

    -------------------------------------------------------------
    # Pound to end of line is a comment, blank lines are ignored

    node local.uff3  nlocal00 5000
    node remote.uff3 nremot00 7000 ntg=false
    gate ngate100 8000
    -------------------------------------------------------------

  This example would run 3 nodes--two collectors and one gate--using the
specified .uff3 files for soft_dcs, the site IDs nlocal00, nremot00,
and ngate100.  The numbers 5000, 7000, and 8000 specify what port numbers
to use (i.e. $GEONET_BASE_PORT). If you don't care what port a node runs on,
you can use the keyword 'auto' instead.  The node key specifier of 'ntg', is used for
a to indicate whether the tm associated with this node is to be run using NTG
or not (value of true indicates to connect to starman over NTG, false indicates
to use it's legacy nmsg port).

  The first word on each line tells runp what kind of node to run.  Possible
values are:

    node        a regular GEOnet sensor node using soft_dcs:
                    node <uff-file> <site-id> <base-port>

    real_node   a regular GEOnet sensor node allowing starting your own dcs:
                    real_node <site-id> <base-port>

    cloned_node a GEOnet sensor node taking its data from another GEOnet sensor node:
                    cloned_node <source-node-site-id> <site-id> <base-port>

    gate        a near-side GEOnet gate:
                    gate <site-id> <base-port>

    jnode       a far-side JICD sensor node:
                    jnode <uff-file> <site-id> <base-port>

    jgate       a far-side JICD gate:
                    gate <site-id> <base-port>

    observer    a near-side observer node:
                    observer <site-id> <base-port>

    jobserver   a far-side observer node:
                    jobserver <site-id> <base-port>

  If you specify any JICD nodes, runp will assume:
    * For FTP connections, you want to use machine''', options.ftp_server, ''',
      user 'flink' as your FTP server
    * For FTP connections, You have created a subdirectory of /localhome/flink
      on''', options.ftp_server, ''' named after your user ID, and a subdirectory below that called runp.

  See 'runp -h' for options controlling where your code is, etc., or
  Dan T. (x444) if you have any other questions.
'''


def is_open(ip,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, int(port)))
        s.shutdown(2)
        return True
    except:
        return False

def get_next_auto_port():
  global used_ports

  next_port = 3000
  while ( used_ports.count( next_port ) or is_open( '127.0.0.1', next_port ) ):
        next_port += 1000
  used_ports.append(next_port)
  return next_port

def set_auto_port ( node, next_port ):
    global used_ports

    if ( node.port > -1 ):
        return next_port

    next_port = get_next_auto_port();
    node.port = next_port
    return next_port
    
def set_auto_ports ( network ):
    global used_ports
    next_port = 3000

    for node in network.geonet_nodes:
        next_port = set_auto_port( node, next_port )
    for node in network.geonet_observers:
        next_port = set_auto_port( node, next_port )
    for node in network.real_geonet_nodes:
        next_port = set_auto_port( node, next_port )
    if ( network.geonet_gate ):
        next_port = set_auto_port( network.geonet_gate, next_port )
    for node in network.jicd_nodes:
        next_port = set_auto_port( node, next_port )
    for node in network.jicd_observers:
        next_port = set_auto_port( node, next_port )
    if ( network.jicd_gate ):
        next_port = set_auto_port( network.jicd_gate, next_port )
    if ( network.message_switch):
        next_port = set_auto_port( network.message_switch, next_port )
    

def main( argc, argv ):

    import string

    from optparse import OptionParser
    parser = OptionParser()

    parser.add_option( "-p", "--project",
                       dest="geonet_project",
                       help="Source tree for near-side nodes" )

    parser.add_option( "-j", "--jicd",
                       dest="jicd_project", 
                       help="Source tree for far-side nodes" )

    parser.add_option( "-n", "--ntg",
                      dest="ntg_tree", default="/net/float/data/ntg/Arthur",
                      help="Run tree for ntg")

    parser.add_option( '--instructions',
                       dest='instructions',
                       default=False,
                       action='store_true',
                       help='Print detailed instructions and exit' )

    parser.add_option( '-c', '--config-file',
                       dest='config_files',
                       action='append',
                       help='Location of the runp configuration file (node list)' )

    parser.add_option( '--high',
                       dest='black_level',
                       default=0,
                       action='store_const',
                       const=1,
                       help='Make the near (GEOnet) side the high side of a black gate' )

    parser.add_option( '--lan',
                       dest='lan_mode',
                       default=False,
                       action='store_true',
                       help='Raise NTG bandwidth limits for testing on a LAN' )

    parser.add_option( '--low',
                       dest='black_level',
                       default=0,
                       action='store_const',
                       const=2,
                       help='Make the near (GEOnet) side the low side of a black gate' )

    parser.add_option( '-i', '--installed-image',
                       dest='installed_image',
                       default=False,
                       action='store_true',
                       help='''OBSOLETE:  Run from an installed image instead
of a source tree (i.e. no run_tree)''' )

    parser.add_option( '--soft-dcs-options',
                       dest='soft_dcs',
                       help='Extra options (space-separated) to pass to soft_dcs' )

    parser.add_option( '--soft-dcs-dir',
                       dest='soft_dcs_dir',
                       help='Use this directory instead of default runtree to find soft_dcs' )

    parser.add_option( '--dcs-clone-dir',
                       dest='dcs_clone_dir',
                       help='Use this directory instead of default runtree to find dcs_clone' )

    parser.add_option( '--dcs-options',
                       dest='dcs',
                       help='Extra options (space-separated) to pass to dcs' )

    parser.add_option( '--dcs-clone-options',
                       dest='dcs_clone',
                       help='Extra options (space-separated) to pass to dcs_clone' )

    parser.add_option( '--config-only',
                       dest='config_only',
                       default=False,
                       action='store_true',
                       help='Just write tm_starman_data & link_con_data, do not start nodes' )

    parser.add_option( '--gate-only',
                       dest='gate_only',
                       default=False,
                       action='store_true',
                       help='Only start the gate(s), not any observer or sensor nodes' )

    parser.add_option( '--dcs-only',
                       dest='dcs_only',
                       default=False,
                       action='store_true',
                       help='Only start the soft_dcs jobs, no tm, ntg, or anything else' )

    parser.add_option( '--start-processor',
                       dest='start_processor',
                       default=True,
                       action='store_false',
                       help='Start the MGW on the gate' )

    parser.add_option( '-f', '--ftp-server',
                       dest='ftp_server',
                       default='vbtf-ftp',
                       help='Name of the FTP server to use for JICD connections' )

    parser.add_option( '--dry-run',
                       dest='dry_run',
                       default=False,
                       action='store_true',
                       help='Just print commands, do not execute' )

    parser.add_option( '--data-repo',
                       dest='data_repository',
                       default=False,
                       action='store_true',
                       help='Add a data repository to the gate map' )

    parser.add_option( '-2', '--two-collects',
                       dest='double_collect',
                       default=False,
                       action='store_true',
                       help='Load each data file twice for simultaneous collects' )

    parser.add_option( "--save-ntg-log",
                       default= False,
                       dest="save_ntg_log",
                       action="store_true",
                       help="Save NTG log files in /tmp" )

    parser.add_option( '-A', '--no-connect-all',
                       default=False,
                       dest='no_connect_all',
                       action='store_true',
                       help='If set, do NOT use STARMAN_CONNECT_ALL' )

    parser.add_option( "-x", "--no-xterm",
                       dest="no_xterm", default=False,
                       action="store_true",
                       help="Run processes in background instead of xterms" )

    parser.add_option( "--no-icon",
                       dest="iconic",
                       default=" -iconic",
                       action="store_const",
                       const=" ",
                       help="Run xterms up instead of iconified" )

    parser.add_option( '-d', '--debug',
                       dest='debug',
                       default=False,
                       action='store_true',
                       help='Debug the runp script' )

    parser.add_option( '--foreground',
                       dest='foreground',
                       default=False,
                       action='store_true',
                       help='Run in forground (only useful for debugging)' )

    parser.add_option( '-s', '--sleep-after',
                       dest='sleep_after',
                       default=False,
                       action='store_true',
                       help='Log to console and sleep 1 day after each command'
                         + ' (so you can see the output)' )

    parser.add_option( '-v', '--verbose',
                       dest='verbose',
                       default=False,
                       action='store_true',
                       help='Log verbosely to console (if inside an xterm)' )

    parser.add_option( '--hits-environment',
                       dest='hits_environment',
                       default=False,
                       action='store_true',
                       help='Use HITS_xxx environment variables rather than GEONET_xxx' )

    parser.add_option( '--old-mgm',
                       dest='old_mgm',
                       default=False,
                       action='store_true',
                       help='Use original mgm and mgwatcher' )

    parser.add_option( '-w', '--jicd-wait',
                       dest='jicd_wait',
                       type='float',
                       default=20,
                       help='''Wait JICD_WAIT seconds between starting near and far side,
 if both are running from the same tree''' )

    parser.add_option( '--gate-site-id',
                       dest='gate_site_id',
                       type='string',
                       default=None,
                       help='explicitly specify GEOnet gate site id for non-gate nodes' )

    parser.add_option( '--gate-port',
                       dest='gate_port',
                       type='string',
                       default=None,
                       help='explicitly specify GEOnet gate port(s) for non-gate nodes' )

    parser.add_option( '--jgate-site-id',
                       dest='jgate_site_id',
                       type='string',
                       default=None,
                       help='explicitly specify JICD gate site id for non-gate nodes' )

    parser.add_option( '--jgate-port',
                       dest='jgate_port',
                       type='int',
                       default=None,
                       help='explicitly specify JICD gate port for non-gate nodes' )

    parser.add_option( '--multi-jicd',
                       dest='multi_jicd',
                       default=False,
                       action='store_true',
                       help='run multi-jicd mode, requires appropriate config file' )

    parser.add_option( '--far-side-ntg',
                       dest='far_side_ntg',
                       default=False,
                       action='store_true',
                       help='in a multi-jicd environment, set up this gate with a far-side ntg (only relevant for gate-to-gate ntg). Same as --gate-is-source.'
                       )

    parser.add_option( '--gate-is-source',
                       dest='gate_is_source',
                       default=False,
                       action='store_true',
                       help='in a multi-jicd environment, set up this gate to be a source; not a sink (only relevant for ntg or socket JICD)'
                       )

    parser.add_option( '--native-soft-dcs',
                       dest='native_soft_dcs',
                       default=False,
                       action='store_true',
                       help='If "dir" is set, get soft_dcs from there instead of -p or -j' )

    parser.add_option( '--jicd_proxy_bin_dir',
                       dest='jicd_proxy_bin_dir',
                       action = 'store',
                       type='string',
                       help='Directory where a jicd_proxy binary resides. Defaults to the near-side runtree path, then the far-side runtree path' )

    parser.add_option( '--validate',
                       dest='validate',
                       default=False,
                       action='store_true',
                       help='perform network validation')

    global options
    global ntg_bandwidths
    global used_ports
    (options, args) = parser.parse_args()

    # Alias "--gate-is-source" and "--far-side-ntg"
    if (options.gate_is_source or options.far_side_ntg):
      options.gate_is_source = True
      options.far_side_ntg = True

    if (options.validate):
      print "Validation mode. Setting config_only, and wait time to 0."
      options.config_only = True
      options.jicd_wait = 0

    if ( not options.jicd_proxy_bin_dir ):
        if (options.geonet_project):     options.jicd_proxy_bin_dir = options.geonet_project
        elif (options.jicd_proxy_bin_dir): options.jicd_proxy_bin_dir = options.jicd_project
        else: print "Cannot determine proxy bin directory!\n"

    if ( options.installed_image ):
        print '''You no longer need to use --installed-image; runp should
figure it out on its own'''

    if ( options.instructions ):
        instructions()
        sys.exit( 0 );

    if ( not options.geonet_project ):
        print "-p is required"
        sys.exit( 1 )

    if ( not options.jicd_project ):
        options.jicd_project = options.geonet_project

    if ( options.lan_mode ):
        for key in ntg_bandwidths.keys():
            ntg_bandwidths[key] = 1000000

    if ( not options.no_xterm and options.verbose ):
        os.environ['SLOG_LOG_TO_CONSOLE'] = 'y'

    if ( options.old_mgm ):
        os.environ['GEONET_MGM_USE_MGM2'] = 'no'

    if ( not options.config_files ):
      options.config_files = [ os.environ['HOME'] + '/etc/runp' ]

    for file in options.config_files:
      if ( not os.path.isfile( file ) ):
        print "Error:  Can't read", file
        sys.exit( 1 )

    if ( not os.path.isfile( '/etc/sysconfig/geonet' ) ):
        print "Error:  /etc/sysconfig/geonet does not exist; needed by NTG to log properly"

    if ( options.multi_jicd ):
      if ( 1 != len( options.config_files ) ):
           print "Error:  multi-jicd mode only allows one config file"
           sys.exit( 1 )

      options.config_file = options.config_files.pop()
      if ( os.path.isfile( options.config_file ) ):
        mjnet = MultiJICDNetwork( options.config_file )
        launch_mj_runps( mjnet )
        sys.exit( 0 )

    network = Network( options.config_files )
    print 'Used ports:', used_ports
    set_auto_ports( network )
    print 'All ports:', used_ports


    write_geonet_config_files( network )
    if ( not options.config_only ):
        if ( options.ntg_tree != '' ):
            write_ntg_config_files( network )
            start_ntgs( network )
        start_geonet_nodes( network )

    if ( network.geonet_gate
         and network.jicd_gate and int(network.jicd_gate.port) > 0
         and options.geonet_project == options.jicd_project ):

        print "Waiting for near side to start up..."
        time.sleep( 1.0 * options.jicd_wait )
        print "Done waiting"

    write_jicd_config_files( network )
    if ( not options.config_only and network.jicd_gate and int(network.jicd_gate.port) > 0 ):
        start_jicd_nodes( network )

    if (options.validate):
      perform_validation([network.geonet_gate, network.jicd_gate])
      os.system("rm -rf " + RUNP_LINK_CON_PATH)

def copy_config(path_to_config, gate_id):
  dir = RUNP_LINK_CON_PATH + "/" + gate_id + "/"
  print "Copying config " + path_to_config + " to " + dir
  os.system("mkdir -p " + dir)
  os.system("cp " + path_to_config + " " + dir)

def perform_validation(gate_list):
  global options
  cmd = proj_to_bin(options.geonet_project) + "/tools/NetworkTopologyTool"
  for gateid in gate_list:
    cmd = cmd + " " + gateid + ":" + RUNP_LINK_CON_PATH + "/" + gateid
  os.system(cmd)

geonet_gate_levels = [ 'normal', 'isHigher', 'isLower' ]
jicd_gate_levels = [ 'normal', 'isLower', 'isHigher' ]
used_ports = [6000] # used by X server
ntg_bandwidths = { 'min' : 1000, 'max' : 7000, 'channel' : 35000 }
transport_types = [ 'ftp', 'ntg', 'socket_JICD_sink', 'socket_JICD_source' ]
default_transport = transport_types[1]

if __name__ == "__main__":
    import sys
    sys.exit( main( len( sys.argv ), sys.argv ) )
