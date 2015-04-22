#!/usr/bin/env python

from optparse import OptionParser
from requestrouter import *
from requestparsing import *
from msgpacking import MsgStream

import Queue
import msgpacking
import SocketServer
import re
import threading
import os, commands
import struct

class TransactionCounter:
    __count = 0
    __count_lock = threading.RLock()
    
    __slots__ = [ '__count', '__count_lock' ]
    
    
    def __init__( self ):
        try:
            self.__count_lock.acquire()
            import random
            TransactionCounter.__count = random.randint( 1, 1000000 )
        finally:
            self.__count_lock.release()

    def get( self ):
        try:
            self.__count_lock.acquire()
            count = TransactionCounter.__count
            TransactionCounter.__count += 1
            return count

        finally:
            self.__count_lock.release()

TransCounter = TransactionCounter()

class Transaction:
    def __init__( self, path, tid, openmode ):
        self.path = path + os.path.sep + str( tid )
        self.tid = tid
        self.openmode = openmode
            
class TList:
    def __init__( self ):
        self.listLock = threading.RLock()
        self.tlist = list()

    def append( self, trans ):
        try:
            self.listLock.acquire()
            self.tlist.append( trans )
        finally:
            self.listLock.release()

    def get( self, tid ):
        try:
            self.listLock.acquire()
            for trans in self.tlist:
                if trans.tid == tid:
                    return trans

            return None
        finally:
            self.listLock.release()

    def remove( self, tid ):
        try:
            self.listLock.acquire()
            for trans in self.tlist:
                if trans.tid == tid:
                    self.tlist.remove( trans )
        finally:
            self.listLock.release()
    
TransactionsList = TList()

class GlobalOptions:
    pass

class ConfigGuiConnectionHandler( SocketServer.BaseRequestHandler ):
    def handle( self ):
        # socket is self.request
        # address is self.client_address
        print "client %s connected" % self.client_address[0]

        router = RequestRouter( self.request )
        router.add_handler( re.compile( r'^get\s+nodelist',
                                        re.IGNORECASE ),
                            self.handleGetNodeList )

        router.add_handler( re.compile( r'^save\s+nodelist',
                                        re.IGNORECASE ),
                            self.handleSaveNodeList )

        router.add_handler( re.compile( r'^commit\s+transaction',
                                        re.IGNORECASE ),
                            self.handleCommitTransaction )

        router.add_handler( re.compile( r'^clear\s+transaction',
                                        re.IGNORECASE ),
                            self.handleClearTransaction )

        self.sendClientAddress( self.request, self.client_address[0] )

        self.incoming_stream = str()
        while True:                    
            data = self.request.recv( 4096 )
            if not data: break

#            import pdb; pdb.set_trace();

            self.incoming_stream += data

            while len( self.incoming_stream ) > 0 :
                text = str()
                mstream = MsgStream( self.incoming_stream )
                for msg in mstream:
                    text += msg.text
                    if msg.sequence_number >= msg.total_messages:
                        break
                else:
                    break  # didn't read all of the messages in sequence
            
                print "Received:\n%s" % ( text )
                try:
                    try:
                        if router.route( text ):
                            pass
                            # print "Server handled: %s" %  text
                    except( RoutingError ), msg:
                        print "RoutingError: ", msg
                finally:
                    self.incoming_stream = self.incoming_stream[ len( self.incoming_stream ) - len( mstream.stream ): ]



        print "client %s disconnected" % self.client_address[0]
        self.request.close( )

    def sendClientAddress( self, socket, address ):
        addrmsg = "client address=" + address
        print "server '%s'" % addrmsg
        buf = msgpacking.pack( addrmsg )
        socket.send( buf )

    def createTransaction( self, openmode ):
        
        if GlobalOptions.subversion:
            trans = Transaction( GlobalOptions.transactions_directory,
                                 TransCounter.get(),
                                 openmode )

            svncmd = 'svn co ' + GlobalOptions.subversion + ' ' + \
                     trans.path

            status = commands.getstatusoutput( svncmd )
            if status[0]:
                raise Exception( status[1] )
            else:
                global TransactionsList
                TransactionsList.append( trans )
                return trans
        else:
            raise Exception( "No repository directory found" )
        

    def handleGetNodeList( self, socket, text ):

        filename = str()
        errmsg = str()

        sourcestr = getAttributeValue( 'source', text )
        openmode = getAttributeValue( 'openmode', text )
        transid = getAttributeValue( 'transactionID', text )

        if not openmode:
            print "missing openmode=[readonly|readwrite] parameter from get nodelist, defaulting to readonly"
            openmode = 'readonly'

        if sourcestr == 'data':
            filename = GlobalOptions.datafilename
        elif sourcestr == 'meta':
            filename = GlobalOptions.metafilename
        elif sourcestr == 'both':
            pass
        else:
            errmsg = "missing source=[data|meta|both] parameter from get nodelist"

        if not errmsg:
            try:
                trans = None
                try:
                    if transid:
                        try:
                            tid = int( transid )
                            trans = TransactionsList.get( tid )
                            if not trans:
                                errmsg = "No transaction found matching transaction ID %d" % int( transid )
                        except( ValueError ), arg:
                            errmsg = "Exception converting %s to int: %s" % ( transid, arg.message )
                    else:
                        trans = self.createTransaction( openmode )
                except( Exception ), arg:
                    errmsg = "Exception encountered creating transaction: " + arg.message
                    print errmsg

                if trans:
                    try:
                        buf = str()
                        if not filename:
                            metafilename = trans.path + os.path.sep + GlobalOptions.metafilename
                            datafilename = trans.path + os.path.sep + GlobalOptions.datafilename
                            fd = open( metafilename )
                            try:
                                buf = fd.read()
                                if os.path.exists( datafilename ):
                                    fd2 = open( datafilename )
                                    try:
                                        buf2 = fd2.read()
                                        buf += buf2
                                    finally:
                                        fd2.close()
                            finally:
                                fd.close()
                                
                        else:
                            filename = trans.path + os.path.sep + filename
                            fd = open( filename )
                            try:
                                buf = fd.read()
                            finally:
                                fd.close()
                        
                            
                        try:
                            bufmsg = 'got nodelist source=' + sourcestr + ' transactionID=' + str( trans.tid ) + ';\n' + buf
                            print "constructed: %s" % bufmsg
                            bufmsg = msgpacking.pack( bufmsg )

                            if not filename:
                                filename="both meta and data"

                            print "server sending data from %s" % filename
                            socket.send( bufmsg )

                        except( struct.error ), msg:
                            print "msg packing error: ", msg

                    except IOError, arg:
                        errmsg = "IOError encountered opening %s: %s" % ( filename, arg[1] )
                        print errmsg

            except( Exception ), arg:
                errmsg = "Unable to create transaction, error=%s" % arg.message
                print errmsg

        if errmsg:
            msg = "failed nodelist msg='" + errmsg + "';"
            bufmsg = msgpacking.pack( msg )
            print "server sending %s" % msg
            socket.send( bufmsg )

        return True
                
    def handleCommitTransaction( self, socket, text ):

        errmsg = str()
        trans = None
        
        transid = getAttributeValue( 'transactionID', text )
        if not transid:
            errmsg = "invalid transactionID specified in save nodelist command"
        else:
            try:
                transidint = int( transid )
                trans = TransactionsList.get( transidint )
                if not trans:
                    errmsg = "No transaction found matching transaction ID %d" % int( transidint )
            except( ValueError ), arg:
                errmsg = "Exception converting %s to int: %s" % ( transid, arg.message )

        if not errmsg:
            for fil in os.listdir( trans.path ):
                if fil.startswith( '.' ):
                    continue

                svnpath = GlobalOptions.subversion + os.path.sep + fil
                svncmd = 'svn list ' + svnpath
                status = commands.getstatusoutput( svncmd )
                if status[0]:
                    print "file %s not found, attempting to import..." % ( fil )
                    svncmd = "svn import -m 'initial import of %s' %s %s" % ( fil, trans.path + os.path.sep + fil, svnpath )
                    status = commands.getstatusoutput( svncmd )
                    if status[0]:
                        errmsg = "failed to import %s to repository %s: %s" % ( fil, GlobalOptions.subversion, status[1] )
                        break


            svncmd = "svn ci -m 'committing transaction %d' %s" % ( trans.tid, trans.path )
            status = commands.getstatusoutput( svncmd )
            if status[0]:
                errmsg = "failure committing transaction: %s" % status[1]
                print "removing transaction"
                self.removeTransaction( trans.tid )
            else:
                print "successfully committed transaction %s" % ( trans.tid )
                buf = 'committed transaction transactionID=%d' % ( trans.tid )
                bufpacked = msgpacking.pack( buf )
                socket.send( bufpacked )

                
        if errmsg:
            print errmsg
            buf = msgpacking.pack( 'failed commit msg=\'' + errmsg + '\';' )
            socket.send( buf )

        return True



    def removeTransaction( self, tid ):
        trans = TransactionsList.get( tid )
        if not trans:
            return

        direct = os.path.join( GlobalOptions.transactions_directory, str( tid ) )
        if os.path.exists( direct ):
            rmcmd = "rm -rf " + direct
            status = commands.getstatusoutput( rmcmd )
            if status[0]:
                print "error removing transaction: %s" % ( status[1] )
            else:
                TransactionsList.remove( tid )
    
    def handleClearTransaction( self, socket, text ):
        errmsg = str()

        tid = int()
        transid = getAttributeValue( 'transactionID', text )
        if not transid:
            errmsg = "invalid transactionID specified in save nodelist command"
        else:
            try:
                tid = int( transid )
                trans = TransactionsList.get( tid )
                if not trans:
                    errmsg = "No transaction found matching transaction ID %d" % tid
            except( ValueError ), arg:
                errmsg = "Exception converting %s to int: %s" % ( transid, arg.message )

        if errmsg:
            print errmsg
            return True

        self.removeTransaction( tid )

        return True


    def handleSaveNodeList( self, socket, text ):
        errmsg = str()
        
        filename = GlobalOptions.datafilename
        sourcestr = getAttributeValue( 'source', text )

        trans = None
        tid = int()
        transid = getAttributeValue( 'transactionID', text )
        if not transid:
            errmsg = "invalid transactionID specified in save nodelist command"
        else:
            try:
                tid = int( transid )
                trans = TransactionsList.get( tid )
                if not trans:
                    errmsg = "No transaction found matching transaction ID %d" % tid
            except( ValueError ), arg:
                errmsg = "Exception converting %s to int: %s" % ( transid, arg.message )

        if sourcestr == 'meta':
            filename = GlobalOptions.metafilename
        elif sourcestr != 'data':
            errmsg = "invalid source field in source= parameter of save nodelist command"

        if not errmsg:
            try:
                filename = trans.path + os.path.sep + filename
                fd = open( filename, 'w' )
                try:
                    try:
                        yamlfile = text[ text.find( '---' ) : ]
                        print "Server writing %s" % filename
                        print >> fd, yamlfile
                        fd.flush()

                        buf = msgpacking.pack( 'saved nodelist;' )
                        print "server sending saved nodelist;"
                        socket.send( buf )
                    except( struct.error ), msg:
                        print "msg packing error: ", msg

                finally:
                    fd.close()

            except IOError, arg:
                errmsg = "IOError encountered opening %s: %s" % ( filename, arg[1] )
                print errmsg

        if errmsg:
            print errmsg
            buf = msgpacking.pack( 'failed save msg=\'' + errmsg + '\';' )
            socket.send( buf )

        return True


def main( argc, argv ):

    parser = OptionParser()
    parser.add_option( "-p", "--port",
                       dest="port",
                       type="int",
                       help="specify server port",
                       default=5007,
                       metavar=" PORT" )

    parser.add_option( "-f", "--file",
                       dest="file",
                       type="string",
                       help="specify masterlist file",
                       default="nodelist_data.yaml",
                       metavar=" FILE" )

    parser.add_option( "-m", "--meta",
                       dest="meta",
                       type="string",
                       help="specify masterlist meta file",
                       default="nodelist_meta.yaml",
                       metavar=" FILE" )

    parser.add_option( "-s", "--subversion",
                       dest="subversion_spec",
                       type="string",
                       help="specify subversion repository root+directory",
                       metavar=" SVNROOT" )

    parser.add_option( "-t", "--transactions-directory",
                       dest="transactions_directory",
                       type="string",
                       help="where to check out revisions of master list",
                       default="transactions",
                       metavar=" DIR" )

    ( options, args ) = parser.parse_args()

    if not options.subversion_spec:
        print "missing required < -s, --subversion= > argument"
        print parser.format_help()
        return 1
        

    GlobalOptions.metafilename = options.meta
    print "server using master list meta %s" % GlobalOptions.metafilename

    GlobalOptions.datafilename = options.file
    print "server using master list %s" % GlobalOptions.datafilename

    GlobalOptions.subversion = options.subversion_spec.rstrip( os.path.sep )
    GlobalOptions.transactions_directory = options.transactions_directory

    tmpdir = "/tmp/.%d.masterlist-server" % os.getpid();


    if os.path.exists( GlobalOptions.transactions_directory ):
        print "removing transaction directory %s" % GlobalOptions.transactions_directory
        commands.getstatusoutput( "rm -rf %s" % GlobalOptions.transactions_directory )

    if GlobalOptions.subversion:
        print "server using subversion repository root %s" % GlobalOptions.subversion
        svnstring = 'svn co ' + GlobalOptions.subversion + ' ' + tmpdir

        print "checking repository status..."
        print "executing ", svnstring
    
        commands.getstatusoutput( "mkdir -p %s" % tmpdir )
        
        status = commands.getstatusoutput( svnstring )
        if status[0]:
            print "subversion error: %s" % status[1]
            print "attempting to import metadata..."
            if os.path.exists( GlobalOptions.metafilename ) :
                svnstring = "svn import -m 'initial import of masterlist meta' " + \
                            GlobalOptions.metafilename + " " + GlobalOptions.subversion + \
                            os.path.sep + GlobalOptions.metafilename

                status = commands.getstatusoutput( svnstring )
                if status[0]:
                    print "subversion error: %s" % status[1]
                    print "version control failed, unable to import %s to %s" % ( GlobalOptions.metafilename, GlobalOptions.subversion )
                    return 1
                else:
                    print "successfully imported %s" % ( GlobalOptions.subversion + os.path.sep + GlobalOptions.metafilename )

            else:
                print "no repository revision found and file: %s does not exist, unable to continue" % GlobalOptions.metafilename
                return 1
        else:
            print "success, checking for meta..."
            if os.path.exists( tmpdir + os.path.sep + GlobalOptions.metafilename ):
                print "success, removing temporary files..."
                if os.path.exists( tmpdir ):
                    commands.getstatusoutput( "rm -rf %s" % tmpdir )
            else:
                print "repository directory exists, but doesn't contain meta, importing..."
                # directory exists, but meta doesn't exist, we need to import it
                svnstring = "svn import -m 'initial import of masterlist meta' " + \
                            GlobalOptions.metafilename + " " + GlobalOptions.subversion + \
                            os.path.sep + GlobalOptions.metafilename

                status = commands.getstatusoutput( svnstring )
                if status[0]:
                    print "subversion error: %s" % status[1]
                    print "version control failed, unable to import %s to %s" % ( GlobalOptions.metafilename, GlobalOptions.subversion )
                    return 1
                else:
                    print "successfully imported masterlist meta"
                    print "removing temporary files..."
                    if os.path.exists( tmpdir ):
                        commands.getstatusoutput( "rm -rf %s" % tmpdir )

    localaddr = ( '', options.port )
    print "server configured with port %d" % options.port

    server = SocketServer.ThreadingTCPServer( localaddr, ConfigGuiConnectionHandler )
    print "server accepting connections on localhost:%d" % (options.port)

    server.serve_forever()
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit( main( len( sys.argv ), sys.argv ) )
