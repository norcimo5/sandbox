#!/usr/bin/env python
from SocketClient import SocketClient
from os.path import expanduser
import socket
import cmd
import time
import sys
import math

class picoClient(cmd.Cmd):
    '''
    Simple class to encapulate socket communications with 
    a picoceptor.  Uses a SocketClient, which implements a 
    callback function for data coming into the socket.  Also,
    this client is a subclass of the Cmd class, which implements
    a simple CLI.
    
    History:
        THR:   Oct, 2012:  Initial development    
    '''
    def __init__(self, server_address):
        '''
        Creates the socket and defaults for CLI
        '''
        cmd.Cmd.__init__(self)
        # create/setup client socket to pico
        self.client = SocketClient(server_address)
        self.client.set_listener_callback(self.pico_cmd_callback)
        # setup cmd defaults
        self.prompt = 'pico> '
        self.intro = 'Connected to pico at %s. Press ctrl-D to exit' % str(server_address)
    
    def pico_cmd_callback(self, pico_resp):
        '''
        Callback method used for socket input
        '''
        if pico_resp.find('*IDN') >= 0:
            IDN_list = pico_resp.split(',') 
            print '----- Picoceptor Info ------'
            print '   Model       : %s' % IDN_list[1].split()[0]
            print '   Rev         : %s' % IDN_list[1].split()[1]
            print '   S/N         : %s' % IDN_list[2]
            print '   CA version  : %s' % IDN_list[3]
        else:
            print ">> " + pico_resp,
        self._hist += [ "[resp]: %s" % pico_resp.strip() ]

    def send_msg(self, msg_str, verbose=False):
        '''
        Sends string out socket
        '''
        self.client.send_msg(msg_str)
        if verbose: print "Sent msg: " + msg_str;
        time.sleep(0.050)  # sleep a bit to allow reply
        
    def send_msgs(self, msgs_str, verbose=False):
        '''
        Parse msgs str (separated by ';') into individual msgs and send
        '''
        for msg_str in msgs_str.split(';'):
            self.send_msg(msg_str, verbose)
        
    def default(self, line):
        '''
        This method is called whenever data is entered into the CLI 
        '''
        if line != 'nocmd':
            self.send_msg(line)
    
    def preloop(self):
        '''
        Called (automatically) right before we enter CLI loop.
        this starts the socket listener thread that 
        reads input and passes to callback
        '''
        self._hist    = []  # create a list to hold history...
        self.client.start()
        time.sleep(0.050)  # sleep a bit to allow listener thread to startup

    def precmd(self, line):
        """ This method is called after the line has been input but before
            it has been interpreted. If you want to modifdy the input line
            before execution (for example, variable substitution) do it here.
        """
        if len(line) > 0:
            if line[0] == '@':
                pieces = line[1:].split(' ')
                #print "running cmd: " + line[1:]
                if pieces[0] == 'starttune':
                    self.starttune(pieces[1:])
                elif pieces[0] == 'stoptune':
                    self.stoptune(pieces[1:])
                elif pieces[0] == 'startpsd':
                    self.startpsd(pieces[1:])
                elif pieces[0] == 'stoppsd':
                    self.stoppsd(pieces[1:])
                elif pieces[0] == 'startscan':
                    self.startscan(pieces[1:])
                elif pieces[0] == 'stopscan':
                    self.stopscan(pieces[1:])
                elif pieces[0] == 'ref':
                    self.ref()
                elif pieces[0] == 'reset':
                    self.reset()
                elif pieces[0] == 'stat':
                    self.stat()
                return ""
            elif line[0] == '?':
                self.printHelp()
                return ""
            else:
                self._hist += [ line.strip() ]
                return line
        else:
            return "nocmd"

    def do_EOF(self, line):
        '''
        Called when EOF (ctrl-D) is entered on CLI
        '''
        self.stop()
        return True       
        
    def stop(self):
        '''
        Call this to do any cleanup and stop the listener thread
        '''
        self.client.stop()
        hist_file_path = "%s/.pico_history" %  expanduser("~")
        hist_file = open(hist_file_path, "a")
        for hist in self._hist:
            print>>hist_file, hist
        hist_file.close()
    
    def starttune(self, args):
        ''' args: chan(1 | 2)  bws_setting(5->12) freq digitalAudio_flag(y | n, default = n)
        '''
        if len(args) > 0:
            chan = int(args[0])
            bws  = int(args[1])
            freq = float(args[2])
            if len(args) > 3 and args[3] == 'y':
                audio_config_str = "IQS 0;DAS 1;RSP 1"
            else:
                audio_config_str = "IQS 1;DAS 0"
            startTuneStr = "RCH %d;DFM 1;^CLT 1;BWS %d;FRQ %f;FRD -00600000;%s;OPM 1" % (chan, bws, freq, audio_config_str)
        else:
            startTuneStr = "RCH 1;DFM 1;^CLT 1;BWS 8;FRQ 00162.800000;FRD ?;FRD -00600000;IQS 1;DAS 0;OPM 1"
        self.send_msgs(startTuneStr, True)
        
    def stoptune(self, args):
        ''' args: chan(1 | 2)
        '''
        if len(args) > 0:
            chan       = int(args[0])
            self.send_msgs("RCH %d;OPM 0;BWS 7;IQS 0;^CLT 0" % (chan), True)
        else:
            self.send_msgs("RCH 1;OPM 0;BWS 7;IQS 0;^CLT 0", True)
        
    def startpsd(self, args):
        ''' args: chan(1 | 2) start_freq end_freq bins
        '''
        if len(args) > 0:
            chan       = int(args[0])
            start_freq = float(args[1])
            end_freq   = float(args[2])
            bins       = int(args[3])
            
            fra = start_freq + (5.0 / 2.0)
            if ((end_freq - start_freq) % 5.0) > 0:
                frb = end_freq + (5.0 - ((end_freq - start_freq) % 5.0)) - (5.0 / 2.0)
            else:
                frb = end_freq - (5.0 / 2.0)
            fbs = int(math.log(bins, 2))
            startTuneStr = "RCH %d;SSO -01;FRA %f;FRB %f;INC 5.000;FBS %d;BWS 7;AGC 0;AGP 0;IQS 0;DAS 0;FTC 250;OPM 1;OPR 4" % (chan, fra, frb, fbs)
        else:
            startTuneStr = "RCH 1;SSO -01;FRA 090.500;FRB 105.500;INC 5.000;FBS 13;BWS 7;AGC 0;AGP 0;IQS 0;DAS 0;FTC 250;OPM 1;OPR 4"
        self.send_msgs(startTuneStr, True)
        
    def stoppsd(self, args):
        ''' args: chan(1 | 2)
        '''
        if len(args) > 0:
            chan       = int(args[0])
            self.send_msgs("RCH %d;OPR 1;AGC 1;AGP 1" % (chan), True)
        else:
            self.send_msgs("RCH 1;OPR 1;AGC 1;AGP 1", True)

    def startscan(self, args):
        ''' args: chan(1 | 2) dwell_time_s, freq_1, freq_2, ..., freq_n
        
        Use the Pico SMD command to setup memory locs for each freq in scan list.  
        Then use STL command to set the channels, then change to operation mode 3 for
        Scan.
        '''
        if len(args) > 0:
            chan          = int(args[0])
            mem_chan = 0        #  Memory Channel Number           1 to 200   
            IDM = "0"           #  Idle Mode Status (IDM)          0 or 1              When idle mode is enabled (IDM 1), AGC, threshold, and scan operations are suspended.
            FRQ = ""            #  Tuned Frequency (FRQ)           See FRQ
            BWS = "9"           #  Bandwidth Slot (BWS)            5 to 12
            COR = "10"          #  Carrier Output Relay (COR)      -01 to 99           Threshold relative to NF that indicates a signal is present
            DET = "0"           #  Detection Mode (DET)            0 to 9              "0" == I&Q
            AGC = "1"           #  Automatic Gain Control (AGC)    0 or 1
            ATN = "0"           #  Attenuation Setting (ATN)       0 to 84.0
            AFC = "0"           #  Automatic Freq Control (AFC)    0 to 3
            PDW = "50"          #  Pre-signal dwell (PDW)          -1 to 996 ms
            SDW = args[1]       #  Signal Dwell (SDW)              -1 to 600 sec
            LDW = "0"           #  Lost Signal Dwell (LDW)         -1 to 60 sec
            FRA = "88.0"        #  Sweep Start Frequency (FRA)     See FRA
            FRB = "108.0"       #  Sweep Stop Frequency (FRB)      See FRB
            INC = "0.05"        #  Sweep Increment Freq (INC)      See INC
            SWD = "0"           #  Sweep Direction (SWD)           0 or 1
            BFO = "0"           #  Beat Freq Oscillator (BFO)      -8 kHz to +8 kHz
            
            for mem_chan, FRQ in enumerate(args[2:]):
                addSMD = "SMD %d, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 0" % ((mem_chan+1), IDM, FRQ, BWS, COR, DET, AGC, ATN, AFC, PDW, SDW, LDW, FRA, FRB, INC, SWD, BFO)
                self.send_msgs(addSMD, True)
            
            self.send_msgs("RCH %d;STL (1:%d)" % (chan, ( mem_chan+1 )), True)
            self.send_msgs("RCH %d;IQS 1;OPM 1;OPR 3" % (chan), True)

    def stopscan(self, args):
        ''' args: chan(1 | 2)
        '''
        if len(args) > 0:
            chan       = int(args[0])
            self.send_msgs("RCH %d;OPR 1;IQS 0" % (chan), True)
        else:
            self.send_msgs("RCH 1;OPR 1;IQS 0", True)

    def ref(self):
        ''' args: 
        '''
        self.send_msgs("RCH 1;REF 0;PPS 1", True)
    
    def reset(self):
        ''' args: 
        '''
        print '\n*********************************\nResetting Pico...please stand by.\n*********************************\n'
        self.send_msg("*RST", True)
        time.sleep(6)
        self.send_msg("BWL?", True)
        self.send_msg("FRG?", True)
        time.sleep(1)
        self.send_msgs("RCH 1;OPR 2;OPR 1;REF 1;PPS 0;DFM 0;AGC 1;AGP 1;DET 0;SQL -150;SAO 0;IQS 0;DAS 0;BWS 7;BFO ?")
        time.sleep(0.5)
        self.send_msgs("RCH 2;OPR 2;OPR 1;AGC 1;AGP 1;DET 0;SQL -1;SAO 0;IQS 0;DAS 0;BWS 7;BFO ?;^CFC CC -2;^CFC OFC -2;FID ?;^FID ?;CDE?")

    def stat(self):
        ''' args: 
        '''
        print '\n*********************************\nStats for channel 1:'
        self.send_msgs("RCH 1;OPR?;IQS?;DAS?;FTS?;OPM?")
        time.sleep(0.5)
        print '*********************************\nStats for channel 2:'
        self.send_msgs("RCH 2;OPR?;IQS?;DAS?;FTS?;OPM?;RCH 1")

    
    def printHelp(self):
        helpStr = '''Special commands:
        @starttune  chan(1 | 2)  bws_setting(5->12) freq [digitalAudio_flag]
        @stoptune   chan(1 | 2)
        @startpsd   chan(1 | 2) start_freq end_freq bins
        @stoppsd    chan(1 | 2)
        @startscan  chan(1 | 2) dwell_time_s, freq_1, freq_2, ..., freq_n
        @stopscan   chan(1 | 2)
        @ref       
        @setup       
        
        Precede these with '@'"
        '''
        print helpStr

if __name__ == "__main__":
    try:
        picoIP = socket.gethostbyname('pico')
    except:
        picoIP = '192.168.43.101'
    picoPort = 8081
    
    if len(sys.argv) > 1:
        picoIP = sys.argv[1]
        picoPort = int(sys.argv[2])
    try:
        pico = picoClient((picoIP, picoPort))
    except:
        print "Error connecting to pico at %s:%d" % (picoIP, picoPort)
        sys.exit()

    pico.send_msg('*IDN?')
    try:
        pico.cmdloop()
    except (KeyboardInterrupt, SystemExit):
        print "User interrupt...exiting"
        pico.stop()
        sys.exit()
