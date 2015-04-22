#!/usr/bin/env python

# 2.5 and newer
# from __future__ import with_statement

from Tkinter import *
from tkSimpleDialog import Dialog
from threading import *
from select import select
from msgpacking import MsgStream
from requestrouter import *
from requestparsing import *
from CustomWidgets import *
from CustomDialogs import *
from nodelist import *

import socket
import Queue
import yaml
import msgpacking
import re
import time
import commands



clientthread = None
nodeconfig_version = "0.1"


globalNodeListData = NodeListSynchronizer()
globalNodeListMeta = NodeListSynchronizer()

clientAddressName = None

class GlobalOptions:
    pass

class SynchronizedMethod:
    def __init__( self, func, lock ):
        self.func = func
        self.lock = lock

    def __call__( self, *args ):

        # 2.5 and newer
        #        with self.lock:
        try:
            self.lock.acquire()

            if args:
                return self.func( *args )
            else:
                return self.func()
        finally:
            self.lock.release()

class StatusEvent:
    def __init__( self, msg ):
        self.message = msg

class ReceivedNodeListDataEvent:
    def __init__( self, nodelist, tid ):
        self.nodelist = None
        self.tid = tid
        if nodelist:
            self.nodelist = nodelist

class ReceivedNodeListMetaEvent:
    def __init__( self, nodelist, tid ):
        self.nodelist = None
        self.tid = tid
        if nodelist:
            self.nodelist = nodelist

class ReceivedNodeListCheckoutEvent:
    def __init__( self, nodelist_meta, nodelist_data, tid ):
        self.nodelist_data = nodelist_data
        self.nodelist_meta = nodelist_meta
        self.tid = tid

class SavedConfirmationEvent:
    def __init__( self, confirmed ):
        self.confirmed = confirmed

class CommitConfirmationEvent:
    def __init__( self, confirmed ):
        self.confirmed = confirmed

class ExitEvent:
    pass

class ConnectedEvent:
    pass

class ClientApp( Thread ):
    def __init__( self, server, port, eventFunc = None ):
        Thread.__init__( self )

        self.server = server
        self.port = port

        self.eventFunc = eventFunc

        self.outgoing = Queue.Queue()
        self.incoming = Queue.Queue()
        self.incoming_stream = str()

        self.__terminate_flag = False;
        self.__terminateLock = RLock()

        self.terminate = SynchronizedMethod( self.__unsync_terminate,
                                             self.__terminateLock )

        self.isTerminated = SynchronizedMethod( self.__unsync_isTerminated,
                                                self.__terminateLock )

        self.__queueLock = RLock()
        self.queueText = SynchronizedMethod( self.__unsync_queueText,
                                             self.__queueLock )

        self.queueFile = SynchronizedMethod( self.__unsync_queueFile,
                                             self.__queueLock )

    def run( self ):
        try:
            # connect to server
            self.statusPrint( "Connecting to server " + self.server + ":" + str( self.port ) )

            self.socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            try:
                self.socket.settimeout( 5.0 )
                self.socket.connect( (self.server, self.port) )
            except( socket.error, socket.timeout ), arg:
                self.statusPrint( "error connecting to %s %d:  %s" % ( self.server, self.port, arg[1] ) )
                self.socket.close()
                self.onExitEvent()
                return

            sname = self.socket.getsockname()
            self.statusPrint( "Connected on Address %s:%s" % (sname[0],sname[1]) )
            
            router = RequestRouter( self.socket )
            router.add_handler( re.compile( r'^got\s+nodelist\s+source=data',
                                            re.IGNORECASE ),
                                self.handleReceivedNodeListData )

            router.add_handler( re.compile( r'^got\s+nodelist\s+source=meta',
                                            re.IGNORECASE ),
                                self.handleReceivedNodeListMeta )

            router.add_handler( re.compile( r'^got\s+nodelist\s+source=both',
                                            re.IGNORECASE ),
                                self.handleReceivedNodeListBoth )

            router.add_handler( re.compile( r'^failed\s+nodelist',
                                            re.IGNORECASE ),
                                self.handleGetNodeListFailure )

            router.add_handler( re.compile( r'^saved\s+nodelist',
                                            re.IGNORECASE ),
                                self.handleSavedNodeList )

            router.add_handler( re.compile( r'^failed\s+save',
                                            re.IGNORECASE ),
                                self.handleSaveNodeListFailure )

            router.add_handler( re.compile( r'^committed\s+transaction',
                                            re.IGNORECASE ),
                                self.handleCommittedTransaction )

            router.add_handler( re.compile( r'^failed\s+commit',
                                            re.IGNORECASE ),
                                self.handleCommitNodeListFailure )

            router.add_handler( re.compile( r'^client\s+address',
                                            re.IGNORECASE ),
                                self.handleReceivedClientAddress )


            self.onConnectedEvent()
            
            self.socket.setblocking( 0 )
        
            while not self.isTerminated():

                ( readers_out, writers_out, errors_out ) = select( [ self.socket ],
                                                                   list(),
                                                                   list(),
                                                                   0.5  )

                if not self.outgoing.empty():
                    try:
                        msg = self.outgoing.get_nowait()
                        if GlobalOptions.debug:
                            self.statusPrint( "sending message to server: " + str( msg ) )

                        try:
                            buf = msgpacking.pack( msg )
                            length_sent = self.socket.send( buf )

                            ( retries, maxretries, socket_timeout ) = 1, 2, 5.0
                            while length_sent < len( buf ):
                                self.statusPrint( "sent a partial message, attempting to send the remainder: retry %d" % retries )
                                ( ro, writers, eo ) = select( list(),
                                                              [ self.socket ],
                                                              list(),
                                                              socket_timeout )
                                if self.socket in writers:
                                    self.socket.send( buf[ length_sent: ] )

                                retries += 1
                                time.sleep( 0.01 )
                                if retries > maxretries:
                                    break

                            if retries > maxretries:
                                self.statusPrint( "send error after %d retries, data lost" % maxretries )
                                    

                        except( socket.error ), arg:
                            self.statusPrint( "socket send error: %s" % ( arg[1] ) )

                    except Queue.Empty:
                        break

                if self.socket in readers_out:

                    # read some data
                    try:
                        buf = self.socket.recv( 4096 )
                        self.incoming.put( buf )
                    except( socket.error ), arg:
                        self.statusPrint( "socket recv error: %s" % ( arg[1] ) )
                        
                if not self.incoming.empty():
                    
                    msg = self.incoming.get_nowait()
                    self.incoming_stream += msg
                    if False:
                        self.statusPrint( "Client received: " + msg )

                    while len( self.incoming_stream ) > 0 :
                        text = str()
                        mstream = MsgStream( self.incoming_stream )
                        for msg in mstream:
                            text += msg.text
                            if msg.sequence_number >= msg.total_messages:
                                break
                        else:
                            self.statusPrint( "Received partial message, queueing" )
                            break


                        try:
                            try:
                                if router.route( text ):
                                    pass
                            except( RoutingError ), msg:
                                self.statusPrint( "RoutingError: %s" % msg )
                                    
                        finally:
                            self.incoming_stream = self.incoming_stream[ len( self.incoming_stream ) - len( mstream.stream ): ]


            # end while not self.isTerminated

        finally:
            if self.socket:
                self.socket.close()

        self.statusPrint( "Client Request Thread Exiting" )
        self.onExitEvent()


    def statusPrint( self, text ):
        if self.eventFunc is not None:
            self.eventFunc( StatusEvent( text ) )
        else:
            print text

    def onExitEvent( self ):
        if self.eventFunc is not None:
            self.eventFunc( ExitEvent() )

    def onConnectedEvent( self ):
        if self.eventFunc:
            self.eventFunc( ConnectedEvent() )

# incoming message handlers

    def handleCommittedTransaction( self, socket, text ):
        if self.eventFunc:
            self.eventFunc( CommitConfirmationEvent( True ) )
        else:
            self.statusPrint( "Client event generator off-line, unable to deliver commit notification" )

    def handleCommitNodeListFailure( self, socket, text ):
        if self.eventFunc:
            self.eventFunc( CommitConfirmationEvent( False ) )
        else:
            self.statusPrint( "Client event generator off-line, unable to deliver commit notification" )

    def handleSavedNodeList( self, socket, text ):
        if self.eventFunc:
            self.eventFunc( SavedConfirmationEvent( True ) )
        else:
            self.statusPrint( "Client event generator off-line, unable to deliver saved notification" )

    def handleSaveNodeListFailure( self, socket, text ):
        if self.eventFunc:
            self.eventFunc( SavedConfirmationEvent( False ) )
        else:
            self.statusPrint( "Client event generator off-line, unable to deliver saved notification" )

    def handleReceivedNodeListData( self, socket, text ):
        self.statusPrint( "Client received NodeList from server: " )
        yamlstart = text.find( '---' )
        self.statusPrint( text[ : yamlstart ] )

        transid = getAttributeValue( 'transactionID', text )
        text = text[ yamlstart : ]
        nodelist = NodeList()
        nodelist.initialize( yaml.load( text ), 'NodeList_data' )

        tid = None
        try:
            if transid:
                tid = int( transid )
            else:
                self.statusPrint( "Missing transactionID in response" )
                
        except( ValueError ), arg:
            self.statusPrint( "Exception converting %s to int: %s" % ( transid, arg.message ) )

        if self.eventFunc:
            if tid:
                self.eventFunc( ReceivedNodeListDataEvent( nodelist, tid ) )
        else:
            self.statusPrint( "Received NodeList Data: " + str( nodelist ) )

    def handleReceivedNodeListMeta( self, socket, text ):
        self.statusPrint( "Client received NodeList_meta from server: " )
        yamlstart = text.find( '---' )
        self.statusPrint( text[ : yamlstart ] ) 

        transid = getAttributeValue( 'transactionID', text )
        text = text[ yamlstart : ]
        nodelist = NodeList()
        nodelist.initialize( yaml.load( text ), 'NodeList_meta' )

        tid = None
        try:
            if transid:
                tid = int( transid )
            else:
                self.statusPrint( "Missing transactionID in response" )
                
        except( ValueError ), arg:
            self.statusPrint( "Exception converting %s to int: %s" % ( transid, arg.message ) )
            
        if self.eventFunc:
            if tid:
                self.eventFunc( ReceivedNodeListMetaEvent( nodelist, tid ) )
        else:
            self.statusPrint( "Received NodeList Meta: " + str( nodelist ) )

    def handleReceivedNodeListBoth( self, socket, text ):
        idx = text.find( '---' )
        if idx == -1:
            self.statusPrint( "received text doesn't seem to contain a yaml document" )
            return

        transid = int( getAttributeValue( 'transactionID', text ) )
        if not transid:
            self.statusPrint( "missing transactionID in got nodelist response" )
            return

        metatext, datatext = ( str(), str() )
        endidx = text.rfind( '---' )
        if endidx == idx:  # no data file included
            metatext = text[ idx + 3 :  ]
        else: # data file included
            metatext = text[ idx + 3 : endidx ]
            datatext = text[ endidx + 3 : ]
        
        nodelist_meta = NodeList()
        nodelist_meta.initialize( yaml.load( metatext ), 'NodeList_meta' )

        nodelist_data = None
        if datatext:
            nodelist_data = NodeList()
            nodelist_data.initialize( yaml.load( datatext ), 'NodeList_data' )

        if self.eventFunc:
            self.eventFunc( ReceivedNodeListCheckoutEvent( nodelist_meta, nodelist_data, transid ) )
        else:
            self.statusPrint( "Created transaction %d" % transid )

    def handleReceivedClientAddress( self, socket, text ):
        self.statusPrint( "client received text %s" % text )
        address = text.lower().find( 'address=' )
        if address == -1:
            self.statusPrint( "missing address= field in text" )
            return

        address = text[ address : ].split( '=' )[1]
        global clientAddressName
        clientAddressName = address
        self.statusPrint( "set client address to %s" % clientAddressName )

    def handleGetNodeListFailure( self, socket, text ):
        msg = text[ text.lower().find( "msg=" ) : ].split( '=' )[1].rstrip(';')
        self.statusPrint( "nodelist retrieval failure: %s" % msg )
        


# unsynchronized methods
    def __unsync_terminate( self ):
        self.__terminate_flag = True
    def __unsync_isTerminated( self ):
        return self.__terminate_flag
        
    def __unsync_queueText( self, text ):
        self.outgoing.put( text )
    def __unsync_queueFile( self, filename ):
        try:
            #with open( filename ) as fd:
            try:
                fd = open( filename )
                self.outgoing.put( fd.read() )
            finally:
                fd.close()
        except:
            self.statusPrint( "IO error encountered with file " + filename )

    def requestNodeListData( self, tid, openmodewrite=False ):
        modestr = "readonly"
        if openmodewrite:
            modestr = "readwrite"

        text = "get nodelist source=data " + "openmode=" + modestr
        if tid:
            text += " transactionID=" + str( tid ) + ";"
            
        self.queueText( text )

    def requestNodeListMeta( self, tid, openmodewrite=False ):
        modestr = "readonly"
        if openmodewrite:
            modestr = "readwrite"

        text = "get nodelist source=meta " + "openmode=" + modestr
        if tid:
            text += " transactionID=" + str( tid ) + ";"
            
        self.queueText( text )


    def requestNodeListAll( self, openmodewrite=False ):
        modestr = "readonly"
        if openmodewrite:
            modestr = "readwrite"

        text = "get nodelist source=both " + "openmode=" + modestr  + ";"
        self.queueText( text )
        

    def saveNodeListData( self, nodeList, tid ):

        text = 'save nodelist source=data '
        text += ' transactionid='
        text += str( tid )
        text += ';\n'
        text += '---\n'
        text += yaml.dump( nodeList.to_dict(), default_flow_style=False )
        text += '\n'

        self.queueText( text )


    def saveNodeListMeta( self, nodeList, tid ):

        text = 'save nodelist source=meta'
        text += ' transactionid='
        text += str( tid )
        text += ';\n'
        text += '---\n'
        text += yaml.dump( nodeList.to_dict(), default_flow_style=False )
        text += '\n'

        self.queueText( text )

    def commitTransaction( self, tid ):

        self.queueText( 'commit transaction transactionid=' + str( tid ) + ';' )


    def clearTransaction( self, tid ):

        self.queueText( 'clear transaction transactionID=' + str( tid ) + ';' )

# about box

class AboutBox( Dialog ):
    def __init__( self, master, title=None ):
        Dialog.__init__( self, master, title )

    def buttonbox( self ):
        self.okbutton = Button( self, text="Ok", command=self.destroy, default=ACTIVE )
        self.okbutton.pack( side=BOTTOM )

    def body( self, master ):
        self.frame = Frame( self )
        self.frame.pack( side=TOP, expand=NO )
        Label( self.frame, text="\n\n\n\nNode Configuration Editor\nv " + nodeconfig_version + "\nCopyright (C) Ticom Geomatics, Inc. 2007" ).pack( side=LEFT )
        self.geometry( "300x200" )

    def apply( self ): pass


class Transaction:
    def __init__( self, nodelist, tid ):
        self.nodelist = nodelist
        self.tid = tid

class SaveDataTransaction( Transaction ):
    def __init__( self, nodelist, tid ):
        Transaction.__init__( self, nodelist, tid )

class SaveMetaTransaction( Transaction ):
    def __init__( self, nodelist, tid ):
        Transaction.__init__( self, nodelist, tid )

class CommitTransaction( Transaction ):
    def __init__( self, tid ):
        Transaction.__init__( self, None, tid )

class ReleaseNodeTransaction( Transaction ):
    def __init__( self, idx, nodelist, tid ):
        Transaction.__init__( self, nodelist, tid )
        self.idx = idx

class ClaimNodeTransaction( Transaction ):
    def __init__( self, idx, nodelist, tid ):
        Transaction.__init__( self, nodelist, tid )
        self.idx = idx

# Main window to be displayed
            
class StandardConfigEditorWindow( Frame ):
    def __init__( self, parent=None, readonly=True, **configopts ):
        Frame.__init__( self, parent, **configopts )

        self.transactionID = None

        global clientAddressName
        if clientAddressName is None:
            clientAddressName = socket.getfqdn()

        self.readonly = readonly
        self.pendingTransactions = list()
        self.nodesReceivedCount = 0

        if parent is not None:
            self.parent = self.winfo_toplevel()
        else:
            self.parent = parent

        self.createBody()

        self.eventLock = RLock()
        self.clientEventQueue = Queue.Queue()

        self.generateClientEvent = SynchronizedMethod( self.__unsync_generateClientEvent,
                                                       self.eventLock )
        
        self.bind( '<<StatusEvent>>', self.clientEventDispatcher )
        self.bind( '<<ReceivedNodeListDataEvent>>', self.clientEventDispatcher )
        self.bind( '<<ReceivedNodeListMetaEvent>>', self.clientEventDispatcher )
        self.bind( '<<ReceivedNodeListCheckoutEvent>>', self.clientEventDispatcher )
        self.bind( '<<ExitEvent>>', self.clientEventDispatcher )
        self.bind( '<<ConnectedEvent>>', self.clientEventDispatcher )
        self.bind( '<<CommitConfirmationEvent>>', self.clientEventDispatcher )
        self.bind( '<<SavedConfirmationEvent>>', self.clientEventDispatcher )
        
        self.statusPrint( "Node Configuration GUI " + nodeconfig_version + " starting..." )

        self.startup()

    def createBody( self ):

        xwidth = float( self.winfo_screenwidth() ) * .6
        yheight = float( self.winfo_screenheight() ) * .6
        xpos = ( self.winfo_screenwidth() - xwidth ) / 2
        ypos = ( self.winfo_screenheight() - yheight ) / 2
        
        self.winfo_toplevel().geometry( "%dx%d+%d+%d" % ( xwidth, yheight, xpos, ypos ) )
        self.winfo_toplevel().title( "Node Configuration Editor" )

        self.parent.rowconfigure( 0, weight=1 )
        self.parent.columnconfigure( 0, weight=1 )

        self.nodeInfoFrames = list()
        self.activeNodeInfoFrame = None

        self.createWidgets()
        self.grid( row=0, column=0, sticky=NSEW )

        self.createWidgetsHook()

        self.localChanges = False


    def startup( self ):
        pass
#        self.onConnectToServerButtonClick()
        
    def createWidgetsHook( self ):
        pass
                

    def cleanupNodeInfoWidgets( self ):
        for item in self.nodeInfoFrames:
            for widget in item.nodeEditorTable:
                widget[0].grid_remove()
                widget[1].grid_remove()

            item.grid_remove()

        self.nodeInfoFrames = list()
        self.activeNodeInfoFrame = None
            

    def selectNodeInfoWidgets( self, idx ):
        if idx < len( self.nodeInfoFrames ):
            # show the widgets and return
            self.activeNodeInfoFrame = self.nodeInfoFrames[ idx ]
            self.activeNodeInfoFrame.tkraise()

    def createNodeInfoWidgets( self, entryNode ):

        self.nodeInfoFrames.append( Frame( self.nodeeditorcanvas, relief=SUNKEN, borderwidth=2 ) )
        idx = len( self.nodeInfoFrames )-1
        
        self.nodeInfoFrames[ idx ].nodeEditorTable = list()

        for key in entryNode.keys():

            value = entryNode.__dict__[ key ]
            if isinstance( value, MetaEntry ):
                continue
            
            e1 = StringVar()
            e2 = StringVar()
            optionentry = StringVar()

            if isinstance( value, MultiEntry ):
                self.nodeInfoFrames[ idx ].nodeEditorTable.append( [ Entry( self.nodeInfoFrames[ idx ],
                                                                            textvariable=e1,
                                                                            disabledforeground='Black' ),

                                                                     ExtendedOptionMenu( self.nodeInfoFrames[ idx ],
                                                                                         optionentry,
                                                                                         *(tuple(value.valid_entries) ) ) ] )
                e1.set( key )
                optionentry.set( value.entry )
            else:
                self.nodeInfoFrames[ idx ].nodeEditorTable.append( [ Entry( self.nodeInfoFrames[ idx ],
                                                                            textvariable=e1,
                                                                            disabledforeground='Black' ),

                                                                     Entry( self.nodeInfoFrames[ idx ],
                                                                            textvariable=e2 ) ] )
                e1.set( key )
                e2.set( value )

        self.nodeeditorcanvas.create_window( 0, 0, window=self.nodeInfoFrames[ idx ] )
        self.nodeInfoFrames[ idx ].rowconfigure( 0, weight=1 )
        self.nodeInfoFrames[ idx ].columnconfigure( 0, weight=1 )
        self.nodeInfoFrames[ idx ].grid( row=1, column=0, sticky=NSEW )

        for i in range( len( self.nodeInfoFrames[ idx ].nodeEditorTable ) ):
            self.nodeInfoFrames[ idx ].nodeEditorTable[i][0].config( state=DISABLED )
            self.nodeInfoFrames[ idx ].nodeEditorTable[i][0].grid( row=i, column=0, sticky=NSEW )
            self.nodeInfoFrames[ idx ].nodeEditorTable[i][1].grid( row=i, column=1, sticky=NSEW )
            if self.readonly:
                self.nodeInfoFrames[ idx ].nodeEditorTable[i][1].config( state=DISABLED )

        self.activeNodeInfoFrame = self.nodeInfoFrames[ idx ]

        sr = list(self.nodeeditorcanvas.bbox("all"))
        self.nodeeditorcanvas.config(scrollregion=tuple(sr))
        self.nodeeditorcanvas.update_idletasks()

    def configureNodeEditorPane( self ):

        self.nodeeditorpane.grid( row=1, column=1, sticky=NSEW )
        self.nodeeditorpane.rowconfigure( 0, weight=1 )
        self.nodeeditorpane.columnconfigure( 0, weight=1 )

        self.nodeeditorcanvas.grid( row=1, column=0, sticky=NSEW )
        self.nodeeditorcanvas.rowconfigure( 0, weight=1 )
        self.nodeeditorcanvas.columnconfigure( 0, weight=1 )

# scrolling is buggy, remove for now
#        self.nodeeditorverticalscroll.grid( row=1, column=1, sticky=N+S ) 
#        self.nodeeditorhorizontalscroll.grid( row=2, column=0, sticky=E+W )

        self.editbuttonspane.grid( row=2, column=0, sticky=NSEW )
# uncomment below to align buttons left
#        self.editbuttonspane.columnconfigure( 0, weight=0 )
#        self.editbuttonspane.columnconfigure( 1, weight=1 )
        self.editbuttonspanegroup.grid( row=0, column=0 )
        
        self.createNodePropertiesButton.grid( row=0, column=1, sticky=W )
        self.releaseNodeButton.grid( row=0, column=2, sticky=W )

        self.nodeeditorinfo.grid( row=0, column=0, sticky=NSEW )

        self.nodeeditorcanvas.update_idletasks()

    def configureNodeListPane( self ):
        self.nodelistbuttonspane.grid( row=0, column=0, columnspan=2, sticky=NSEW )
        self.nodelistbuttonspane.columnconfigure( 0, weight=0 )
        self.nodelistbuttonspane.columnconfigure( 1, weight=1 )
        self.nodelistbuttonsgroup.grid( row=0, column=0 )
        
#        self.connectToServerButton.grid( row=0, column=0, sticky=W  )
        self.reloadNodeListButton.grid( row=0, column=1, sticky=W  )
        self.nodelistpane.grid( row=1, column=0, sticky=NSEW )
        self.nodelistpane.rowconfigure( 1, weight=1 )
        self.nodelistpane.columnconfigure( 0, weight=1 )
        self.nodelistboxlabel.grid( row=0, column=0, sticky=E+W )
        self.nodelistboxscrollbar.grid( row=1, column=1, sticky=N+S )
        self.nodelistbox.grid( row=1, column=0, sticky=NSEW )

    def configureStatusPane( self ):
        self.statuspane.grid( row=2, column=0, columnspan=2, sticky=NSEW )
        self.statuspane.rowconfigure( 0, weight=1 )
        self.statuspane.columnconfigure( 0, weight=1 )
        self.statustextscrollbar.grid( row=0, column=1, sticky=N+S )
        self.statustext.grid( row=0, column=0, sticky=NSEW )

    def createMainMenu( self ):
        self.mainmenu = Menu( self.parent, tearoff=0 )
        self.parent.config( menu=self.mainmenu )
        self.filemenu = Menu( self.mainmenu, tearoff=0 )
        self.editmenu = Menu( self.mainmenu, tearoff=0 )
        self.helpmenu = Menu( self.mainmenu, tearoff=0 )

#        self.filemenu.add_command( label=self.serverButtonConnectString,
#                                   compound=LEFT,
#                                   image=self.connectToServerButtonImage,
#                                   command=self.onConnectToServerButtonClick,
#                                   underline=1 )
        
        self.filemenu.add_separator()
        self.filemenu.add_command( label='Exit',
                                   compound=LEFT,
                                   image=self.fileExitImage,
                                   command=self.onExitClick,
                                   underline=1 )

        self.editmenu.add_command( label='Reload NodeList',
                                   compound=LEFT,
                                   image=self.reloadNodeListButtonImage,
                                   command=self.onReloadNodeListButtonClick,
                                   underline=1 )
                                  

                                   
        self.helpmenu.add_command( label="About", command=self.onAboutClick );

        self.mainmenu.add_cascade( label="File", menu=self.filemenu, underline=1 )
        self.mainmenu.add_cascade( label="Edit", menu=self.editmenu, underline=1 )
        self.mainmenu.add_cascade( label="Help", menu=self.helpmenu, underline=1 )

    
    def createWidgets( self ):

        self.fileExitImage = PhotoImage( file='icons/quit.gif' )
        self.createNodePropertiesButtonImage = PhotoImage( file='icons/claim.gif' )
        self.reloadNodeListButtonImage = PhotoImage( file='icons/reload.gif' )
        self.connectToServerButtonImage = PhotoImage( file='icons/disconnected.gif' )
        self.releaseNodeButtonImage = PhotoImage( file='icons/release.gif' )

        self.serverButtonConnectString = 'Connect To Server'
        self.createMainMenu()

        self.nodeeditorpane = Frame( self )
        self.editbuttonspane = Frame( self.nodeeditorpane, relief=RAISED, borderwidth=2 )
        self.editbuttonspanegroup = Frame( self.editbuttonspane )
        
        
        self.createNodePropertiesButton = Button( self.editbuttonspanegroup,
                                                  text="Claim Node",
                                                  compound=LEFT,
                                                  image=self.createNodePropertiesButtonImage,
                                                  command=self.onCreateNodePropertiesButtonClick,
                                                  state=DISABLED )

        self.releaseNodeButton = Button( self.editbuttonspanegroup,
                                         text="Release Node",
                                         compound=LEFT,
                                         image=self.releaseNodeButtonImage,
                                         command=self.onReleaseNodeButtonClick,
                                         state=DISABLED )

        self.nodeeditorinfo = Label( self.nodeeditorpane, text="Node Attributes", foreground='gray' )

        self.nodeeditorcanvas = Canvas( self.nodeeditorpane, height=0, width=0 )
        self.nodeeditorverticalscroll = Scrollbar( self.nodeeditorpane, command=self.nodeeditorcanvas.yview )
        self.nodeeditorhorizontalscroll = Scrollbar( self.nodeeditorpane, command=self.nodeeditorcanvas.xview, orient=HORIZONTAL )
        self.nodeeditorcanvas.config( yscrollcommand=self.nodeeditorverticalscroll.set,
                                      xscrollcommand=self.nodeeditorhorizontalscroll.set )

        self.nodelistpane = Frame( self )
        self.nodelistbuttonspane = Frame( self, relief=RAISED, borderwidth=2 )
        self.nodelistbuttonsgroup = Frame( self.nodelistbuttonspane )


        self.reloadNodeListButton = Button( self.nodelistbuttonsgroup,
                                            compound=LEFT,
                                            text='Reload NodeList',
                                            image=self.reloadNodeListButtonImage,
                                            command=self.onReloadNodeListButtonClick )

#        self.connectToServerButton = Button( self.nodelistbuttonsgroup,
#                                             text=self.serverButtonConnectString,
#                                             compound=LEFT,
#                                             image=self.connectToServerButtonImage,
#                                             command=self.onConnectToServerButtonClick,
#                                             width=130 )

        self.nodelistboxscrollbar = AutoScrollbar( self.nodelistpane )

        self.nodelistbox = SelectionControlListbox( self.nodelistpane,
                                                    yscrollcommand=self.nodelistboxscrollbar.set,
                                                    exportselection=False,
                                                    eventhandler=self.onNodeSelect )
        
#        self.nodelistbox.bind( '<Button-1>', self.onNodeSelect )
 #       self.nodelistbox.bindtags( self.nodelistbox.bindtags()[1:]+self.nodelistbox.bindtags()[0:1] )  # process system bindings first
        
        self.nodelistboxscrollbar.config( command=self.nodelistbox.yview )
        self.nodelistboxlabel = Label( self.nodelistpane, text="Available Node IDs" )

        self.statuspane = Frame( self )
        self.statustext = Text( self.statuspane, state=DISABLED, wrap=WORD, height=10 )
        self.statustextscrollbar = AutoScrollbar( self.statuspane )
        self.statustext.configure( yscrollcommand = self.statustextscrollbar.set )
        self.statustextscrollbar.configure( command = self.statustext.yview )

        createToolTip( self.reloadNodeListButton, 'Connect to Server and Request NodeList' )

        self.rowconfigure( 1, weight=1 )
        self.rowconfigure( 2, weight=1 )
        self.columnconfigure( 0, weight=1 )
        self.columnconfigure( 1, weight=1 )

        self.configureNodeListPane()
        self.configureNodeEditorPane()
        self.configureStatusPane()


    def __unsync_generateClientEvent( self, event ):
        self.clientEventQueue.put( event )
        if isinstance( event, StatusEvent ):
            self.event_generate( '<<StatusEvent>>', when='tail' )
        elif isinstance( event, ReceivedNodeListMetaEvent ):
            self.event_generate( '<<ReceivedNodeListDataEvent>>', when='tail' )
        elif isinstance( event, ReceivedNodeListMetaEvent ):
            self.event_generate( '<<ReceivedNodeListMetaEvent>>', when='tail' )
        elif isinstance( event, ReceivedNodeListCheckoutEvent ):
            self.event_generate( '<<ReceivedNodeListCheckoutEvent>>', when='tail' )            
        elif isinstance( event, ExitEvent ):
            self.event_generate( '<<ExitEvent>>', when='tail' )
        elif isinstance( event, ConnectedEvent ):
            self.event_generate( '<<ConnectedEvent>>', when='tail' )
        elif isinstance( event, CommitConfirmationEvent ):
            self.event_generate( '<<CommitConfirmationEvent>>', when='tail' )
        elif isinstance( event, SavedConfirmationEvent ):
            self.event_generate( '<<SavedConfirmationEvent>>', when='tail' )

    def clientEventDispatcher( self, e ):

        while not self.clientEventQueue.empty():
            event = self.clientEventQueue.get()
            if isinstance( event, StatusEvent ):
                self.handleStatusPrintEvent( event )
            elif isinstance( event, ReceivedNodeListDataEvent ):
                self.handleReceivedNodeListDataEvent( event )
            elif isinstance( event, ReceivedNodeListMetaEvent ):
                self.handleReceivedNodeListMetaEvent( event )
            elif isinstance( event, ReceivedNodeListCheckoutEvent ):
                self.handleReceivedNodeListCheckoutEvent( event )                
            elif isinstance( event, ExitEvent ):
                self.handleClientExitEvent( event )
            elif isinstance( event, ConnectedEvent ):
                self.handleConnectedEvent( event )
            elif isinstance( event, CommitConfirmationEvent ):
                self.handleCommittedEvent( event )
            elif isinstance( event, SavedConfirmationEvent ):
                self.handleSavedConfirmationEvent( event )

    def handleStatusPrintEvent( self, event ):
        self.statusPrint( event.message )
        
    def statusPrint( self, thetext ):
        self.statustext.configure( state=NORMAL )
        self.statustext.insert( END, "%s\n" % thetext )
        self.statustext.configure( state=DISABLED )

#        import pdb; pdb.set_trace()
#        self.statustextscrollbar.command( "moveto", 1 )

    def handleReceivedNodeListMetaEvent( self, event ):
        self.transactionID = event.tid
        globalNodeListMeta.set( event.nodelist )
#        self.terminateClientThread()

    def handleReceivedNodeListDataEvent( self, event ):
        self.transactionID = event.tid
        self.localChanges = False
        globalNodeListData.set( event.nodelist )
        self.nodesReceivedCount = len( event.nodelist )
        self.displayNodeListBox( globalNodeListData.get() )

    def handleReceivedNodeListCheckoutEvent( self, event ):
        self.transactionID = event.tid
        self.statusPrint( "Client checked out nodelist from server" )
        self.statusPrint( event.nodelist_meta )
        globalNodeListMeta.set( event.nodelist_meta )
#        self.terminateClientThread()
        if event.nodelist_data:
            self.statusPrint( event.nodelist_data )
            self.localChanges = False
            globalNodeListData.set( event.nodelist_data )
            self.nodesReceivedCount = len( event.nodelist_data )
            self.displayNodeListBox( globalNodeListData.get() )

    def setClaimButtons( self, isclaimed ):
        if isclaimed:
            self.createNodePropertiesButton.config( state=DISABLED )
            self.releaseNodeButton.config( state=NORMAL )
        else:
            self.createNodePropertiesButton.config( state=NORMAL )
            self.releaseNodeButton.config( state=DISABLED )

    def disableClaimButtons( self ):
        self.createNodePropertiesButton.config( state=DISABLED )
        self.releaseNodeButton.config( state=DISABLED )


    def clearNodeListBoxEntries( self ):
        self.nodelistbox.delete( 0, END )
        
    def insertNodeListBoxEntry( self, index, node ):
        self.nodelistbox.insert( index, node.english_name )

    def modifyNodeListBoxEntry( self, index, node ):
        if node.claimed.value:
            if node.claimed_by.value == clientAddressName:
                self.nodelistbox.itemconfig( index, foreground='green', selectbackground='green' )
            else:
                self.nodelistbox.disable( index )
            
    def displayNodeListBox( self, nodelist ):

        if not nodelist:
            return
        
        thelist = list()

        self.clearNodeListBoxEntries()
        
        for node in nodelist:
            thelist.append( node.english_name )
            self.insertNodeListBoxEntry( END, node )

        self.cleanupNodeInfoWidgets()
        for english_name in thelist:
            idx = self.getNodeListIndex( english_name )
            self.createNodeInfoWidgets( nodelist[idx] )

        idx = 0
        for node in nodelist:
            self.modifyNodeListBoxEntry( idx, node )
            idx += 1
            
        self.nodelistbox.selection_clear( 0, END )
        for i in range( len( thelist ) ):
            if i not in self.nodelistbox.disabled_indices:
                self.nodelistbox.selection_set( i )
                self.onNodeSelect( None )
                break

    def handleClientExitEvent( self, event ):
        global clientthread
        clientthread = None

#        self.connectToServerButton.grid_remove()

#        self.serverButtonConnectString = 'Connect To Server'
        
#        self.connectToServerButtonImage = PhotoImage( file='icons/disconnected.gif' )
#        self.connectToServerButton = Button( self.nodelistbuttonsgroup,
#                                             text="Connect To Server",
#                                             compound=LEFT,
#                                             image=self.connectToServerButtonImage,
#                                             command=self.onConnectToServerButtonClick,
#                                             width=130 )

#        self.connectToServerButton.grid( row=0, column=0, sticky=W  )

#        self.createMainMenu()

#        self.disableButtonsHook()


    def handleConnectedEvent( self, event ):
        pass
#        self.connectToServerButton.grid_remove()

#        self.serverButtonConnectString = 'Connected'

#        self.connectToServerButtonImage = PhotoImage( file='icons/connected.gif' )
#        self.connectToServerButton = Button( self.nodelistbuttonsgroup,
#                                             text="Connected",
#                                             compound=LEFT,
#                                             image=self.connectToServerButtonImage,
#                                             command=self.onConnectToServerButtonClick,
#                                             state=DISABLED,
#                                             width=130 )

#        self.connectToServerButton.grid( row=0, column=0, sticky=W  )

#        self.createMainMenu()

#        self.requestNodeListButton.config( state=NORMAL )

    def handleSavedConfirmationEvent( self, event ):
        if self.pendingTransactions:
            trans = None
            for i in range( len( self.pendingTransactions ) ):
                if isinstance( i, SaveDataTransaction ) or isinstance( i, SaveMetaTransaction ):
                    trans = i
            if trans:
                if event.confirmed:
                    if isinstance( self.pendingTransactions[ trans ], SaveDataTransaction ):
                        globalNodeListData.set( self.pendingTransactions[ trans ].nodelist )
                        self.localChanges = False
                    elif isinstance( self.pendingTransactions[ trans ], SaveMetaTransaction ):
                        globalNodeListMeta.set( self.pendingTransactions[ trans ].nodelist )

                self.pendingTransactions = self.pendingTransactions[:trans]+self.pendingTransactions[trans+1:]


    def handleCommittedEvent( self, event ):
        while self.pendingTransactions:
            trans = self.pendingTransactions.pop()
            if event.confirmed:

                self.statusPrint( 'Committed NodeList' )

                if isinstance( trans, ClaimNodeTransaction ):
                    self.claimedNodeTransactionHandler( trans )
                elif isinstance( trans, ReleaseNodeTransaction ):
                    self.releaseNodeTransactionHandler( trans )
                elif isinstance( trans, CommitTransaction ):
                    self.committedTransactionHandler( trans )
            else:
                ErrorDialog( self, "Commit Failure Encountered", "Error" )
        
    def claimedNodeTransactionHandler( self, transaction ):
        self.nodelistbox.itemconfig( transaction.idx, foreground='green', selectbackground='green' )
        self.claimedNode( transaction )
        self.onNodeSelect( None )
        
    def releaseNodeTransactionHandler( self, transaction ):
        globalNodeListData.set( transaction.nodelist )
        self.nodelistbox.itemconfig( transaction.idx, foreground='', selectbackground='' )
        self.releasedNode( transaction )
        self.onNodeSelect( None )

    def committedTransactionHandler( self, transaction ):
        self.statusPrint( "Successfully committed, clearing transaction %d" % transaction.tid )
        self.startClientThread()
        clientthread.clearTransaction( self.transactionID )
        self.transactionID = None
        self.pendingTransactions = list()
        clientthread.requestNodeListAll()

    def enableButtonsHook( self ):
#        self.commitNodeListButton.config( state=NORMAL )
#        self.createNodePropertiesButton.config( state=NORMAL )
        self.nodeeditorinfo.config( foreground='black' )

    def disableButtonsHook( self ):
        self.createNodePropertiesButton.config( state=DISABLED )
        self.nodeeditorinfo.config( foreground='gray' )

# button and menu item handlers
    def onExitClick( self ):
        if clientthread is not None:
            clientthread.terminate()
            timeout = 5.0
            clientthread.join( timeout )
            if clientthread.isAlive():
                print "timeout after %d seconds waiting on client shutdown" % int( timeout )
        
        self.winfo_toplevel().quit()
        
    def onSubmitButtonClick( self ):
        editstr = self.edittext.get( "1.0", "1.end" )
        if len( editstr ) and clientthread is not None:
            clientthread.queueText( editstr )

#    def onConnectToServerButtonClick( self ):
#        global clientthread
#        if clientthread is None:
#            clientthread = ClientApp( GlobalOptions.server,
#                                      GlobalOptions.port,
#                                      self.generateClientEvent )
#            clientthread.start()

    def startClientThread( self ):
        global clientthread
        if clientthread is None:
            clientthread = ClientApp( GlobalOptions.server,
                                      GlobalOptions.port,
                                      self.generateClientEvent )
            clientthread.start()

    def terminateClientThread( self ):
        global clientthread
        if clientthread is not None:
            if not self.pendingTransactions:
                clientthread.terminate()  

    def onReloadNodeListButtonClick( self ):
        self.startClientThread()
        if clientthread:
            if self.shouldRequestNodeList():
                self.pendingTransactions = list()
                clientthread.requestNodeListAll()
        else:
            ErrorDialog( self, 'ERROR: Client Thread Off-Line' )

    def shouldRequestNodeList( self ):
        if self.localChanges:
            dlg = YesNoDialog( self, 'Local changes exist which will be lost, Continue Anyway?', 'Continue?' )
            if dlg.yes:
                return True
            else:
                return False
        else:
            if self.pendingTransactions:
                transstr = "["
                for i in self.pendingTransactions:
                    transstr += " "
                    transstr += i.__class__.__name__
                transstr += " ]"

                dlg = YesNoDialog( self, 'You have %d pending transactions: %s, Continue Anyway?' % ( len( self.pendingTransactions ), transstr ), 'Continue?' )
                if dlg.yes:
                    return True
                else:
                    return False
            else:
                return True


    def claimedNode( self, transaction ):
        # this code should go in the claimed node confirmation handler
        commit = True
        try:
            nodefp = open( '../config/node.properties', 'w' )
            try:
                try:
                    self.statusPrint( 'creating node.properties' )
                    for item in self.activeNodeInfoFrame.nodeEditorTable:
                        # item[0] is key, item[1] is value
                        nodeproperty = "node.%s=" % ( str( item[0].get() ) )
                        ival = str( item[1].get() )
                        try:
                            ival = int( ival )
                        except( ValueError ):
                            ival = "%s" % ( ival )

                        nodeproperty += str( ival )
                        self.statusPrint( 'adding entry %s' % ( nodeproperty ) )
                        print >> nodefp, '%s' % nodeproperty

                    self.statusPrint( 'created node.properties' )

                except( IOError ), arg:
                    self.statusPrint( "error writing node.properties: %s" % arg[1] )
                    commit = False

            finally:
                nodefp.close()

        except( IOError ), arg:
            ErrorDialog( self, "error opening node.properties: %s, unable to claim node" % arg[1] )
            commit = False

        if commit:
            globalNodeListData.set( transaction.nodelist )

    def releasedNode( self, transaction ):
        self.statusPrint( "deleting node.properties" )
        deletecmd = "mv -f ../config/node.properties ../config/node.properties.OLD"
        status = commands.getstatusoutput( deletecmd )
        if status[0]:
            self.statusPrint( "failure deleting old node.properties: %s" % status[1] )
        else:
            self.statusPrint( "successfully deleted old node.properties" )

    def onReleaseNodeButtonClick( self ):
        sel = self.nodelistbox.curselection()
        if sel:
            english_name = self.nodelistbox.get( sel[0] )
            nodelist = globalNodeListData.get()
            idx = self.getNodeListIndex( english_name )
            
            if nodelist[idx].claimed.value and nodelist[idx].claimed_by.value == clientAddressName:
                dlg = YesNoDialog( self, "Release node %s and delete node.properties?" % ( english_name ), "Question" )
                if not dlg.yes:
                    return

                self.startClientThread()

                nodelist[idx].claimed.value = False
                nodelist[idx].claimed_by.value = None

                self.pendingTransactions.insert( 0, ReleaseNodeTransaction( idx,  nodelist, self.transactionID ) )
                clientthread.saveNodeListData( nodelist, self.transactionID )

                self.pendingTransactions.insert( 0, CommitTransaction( self.transactionID ) )
                clientthread.commitTransaction( self.transactionID )
                
    
    def onCreateNodePropertiesButtonClick( self ):
        sel = self.nodelistbox.curselection()
        if sel:
            english_name = self.nodelistbox.get( sel[0] )
            dlg = YesNoDialog( self, "Claim node %s and write node.properties?" % ( english_name ), "Question" )
            if not dlg.yes:
                return
        else:
            return
        
        self.startClientThread()
        if clientthread:
            if self.activeNodeInfoFrame is not None:

                sel = self.nodelistbox.curselection()
                if not sel:
                    return

                english_name = self.nodelistbox.get( sel )

                nodelist = globalNodeListData.get()
                idx = self.getNodeListIndex( english_name )
                nodelist[ idx ].claimed.value = True
                nodelist[ idx ].claimed_by.value = clientAddressName

                self.pendingTransactions.insert( 0, ClaimNodeTransaction( idx, nodelist, self.transactionID ) )
                clientthread.saveNodeListData( nodelist, self.transactionID )
                
                self.pendingTransactions.insert( 0, CommitTransaction( self.transactionID ) )
                clientthread.commitTransaction( self.transactionID )
                
        else:
            ErrorDialog( self, "client thread off-line, unable to claim node" )


    def onNodeSelect( self, event ):
        sel = self.nodelistbox.curselection()
        if sel:
            self.selectNodeInfoWidgets( int( sel[0] ) )
            english_name = self.nodelistbox.get( sel[0] )
            nodelist = globalNodeListData.get()
            idx = self.getNodeListIndex( english_name )
            if nodelist[idx].claimed.value and nodelist[idx].claimed_by.value == clientAddressName:
                self.setClaimButtons( True )
            else:
                if self.canClaim():
                    self.setClaimButtons( False )
                else:
                    self.disableClaimButtons()

            self.enableButtonsHook()

    def canClaim( self ):
        nodelist = globalNodeListData.get()
        for node in nodelist:
            if node.claimed.value and node.claimed_by.value == clientAddressName:
                break
        else:
            return True

        return False

    def onAboutClick( self ):
        AboutBox( self.winfo_toplevel(), title="About Node Configuration Editor" )

    def getNodeListIndex( self, english_name ):
        nodelist = globalNodeListData.get()
        idx = None
        for idx in range( len( nodelist ) ):
            if nodelist[idx].english_name == english_name:
                break
        return idx
        
class AddSingleEntryDialog( GridDialog ):
    def __init__( self, parent, title='Enter Key and Value' ):
        self.key = None
        self.value = None
        GridDialog.__init__( self, parent, title )

    def body( self, master ):
        master.columnconfigure( 0, weight=1 )
        master.columnconfigure( 1, weight=1 )
        
        Label( master, text='Name' ).grid( row=0, column=0 )
        self.keyentry = Entry( master )
        self.keyentry.grid( row=1, column=0, sticky=E+W )

        Label( master, text='Default Value' ).grid( row=0, column=1 )
        self.valueentry = Entry( master )
        self.valueentry.grid( row=1, column=1, sticky=E+W )

        return self.keyentry

    def buttonbox( self, master ):

        self.okbuttonimage = PhotoImage( file='icons/ok.gif' )
        self.okbutton = Button( master, text="OK", compound=LEFT, image=self.okbuttonimage, command=self.ok, default=ACTIVE )
        self.okbutton.grid( row=0, column=0 )
        self.cancelbuttonimage = PhotoImage( file='icons/cancel.gif' )
        self.cancelbutton = Button( master, text="Cancel", compound=LEFT, image=self.cancelbuttonimage, command=self.cancel)
        self.cancelbutton.grid( row=0, column=1 )
        
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)


    def validate( self ):
        return len( self.keyentry.get() )

    def apply( self ):
        self.key = self.keyentry.get()
        self.value = self.valueentry.get()

class AddMenuEntryDialog( GridDialog ):
    def __init__( self, parent, title='Enter Option Name' ):
        self.option = None
        GridDialog.__init__( self, parent, title )

    def body( self, master ):
        Label( master, text='Option Name' ).grid( row=0, column=0 )
        self.optionentry = Entry( master )
        self.optionentry.grid( row=1, column=0, sticky=E+W )

        return self.optionentry

    def validate( self ):
        return len( self.optionentry.get() ) > 0

    def apply( self ):
        self.option = self.optionentry.get()
        
class AddMultiEntryDialog( GridDialog ):
    def __init__( self, parent, title='Enter Key and Values' ):
        self.key = None
        self.values = None
        GridDialog.__init__( self, parent, title )

    def body( self, master ):
        Label( master, text='Name' ).grid( row=0, column=0 )
        Label( master, text='Values' ).grid( row=0, column=1 )
        self.keyentry = Entry( master )
        self.keyentry.grid( row=1, column=0, sticky=E+W )
        self.createValuesMenu()

        self.addOptionButtonImage = PhotoImage( file='icons/add.gif' )
        self.addOptionButton = Button( master,
                                       image=self.addOptionButtonImage,
                                       command=self.onAddOptionButtonClick )

        self.addOptionButton.grid( row=1, column=2, sticky=W )

        return self.keyentry
                                    

    def onAddOptionButtonClick( self ):
        dlg = AddMenuEntryDialog( self )
        if dlg.option:
            if not self.values:
                self.values = list()
                
            self.values.append( dlg.option )
            self.createValuesMenu()
    
    def createValuesMenu( self ):
        if self.values:
            self.valuesmenu = ExtendedOptionMenu( self.bodyframe, StringVar(), *(tuple( self.values )) )
            self.valuesmenu.set( self.valuesmenu.get_values()[0] )
        else:
            self.valuesmenu = ExtendedOptionMenu( self.bodyframe, StringVar(), None )

        self.valuesmenu.grid( row=1, column=1, sticky=E+W )

    def buttonbox( self, master ):

        self.okbuttonimage = PhotoImage( file='icons/ok.gif' )
        self.okbutton = Button( master, text="OK", compound=LEFT, image=self.okbuttonimage, command=self.ok, default=ACTIVE )
        self.okbutton.grid( row=0, column=0 )
        self.cancelbuttonimage = PhotoImage( file='icons/cancel.gif' )
        self.cancelbutton = Button( master, text="Cancel", compound=LEFT, image=self.cancelbuttonimage, command=self.cancel)
        self.cancelbutton.grid( row=0, column=1 )
        
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

    def validate( self ):
        return ( len( self.keyentry.get() ) > 0 and self.values )

    def apply( self ):
        self.key = self.keyentry.get()
        
class CreateNodeDialog( GridDialog ):
    def __init__( self, parent, title = None ):
        nodelist = globalNodeListMeta.get()
        self.nodelocal = nodelist[0]
        self.node = None
        self.localChanges = False
        GridDialog.__init__( self, parent, title )

    def body( self, master ):
        # create dialog body.  return widget that should have initial focus
        master.rowconfigure( 0, weight=0 )
        master.rowconfigure( 1, weight=1 )
        master.columnconfigure( 0, weight=1 )

        self.toolbar = Frame( master, relief=RAISED, borderwidth=2 )
        self.buttongroup = Frame( self.toolbar )
        self.entriesframe = Frame( master )
        self.entriestable = list()

        self.toolbar.columnconfigure( 0, weight=0 )
        self.toolbar.columnconfigure( 1, weight=1 )
        self.toolbar.grid( row=0, column=0, sticky=NSEW )
        self.buttongroup.grid( row=0, column=0, sticky=NSEW )
        
        self.entriesframe.grid( row=1, column=0, sticky=NSEW )

        self.tbbutton1image = PhotoImage( file='icons/addsingle.gif' )
        self.tbbutton1 = Button( self.buttongroup,
                                 compound=LEFT,
                                 image=self.tbbutton1image,
                                 text="Add Key/Value Pair",
                                 command=self.onAddSingleClick )
        
        self.tbbutton1.grid( row=0, column=0, sticky=W )

        self.tbbutton2image = PhotoImage( file='icons/addmulti.gif' )
        self.tbbutton2 = Button( self.buttongroup,
                                 compound=LEFT,
                                 image=self.tbbutton2image,
                                 text="Add Multivalued Attribute",
                                 command=self.onAddMultiClick )
        
        self.tbbutton2.grid( row=0, column=1, sticky=W )

        self.deleteEntryButtonImage = PhotoImage( file='icons/delete.gif' )

        self.createEntriesTable()
        self.displayEntriesTable()
        
        return None


    def buttonbox( self, master ):

        self.okbuttonimage = PhotoImage( file='icons/ok.gif' )
        self.okbutton = Button( master, text="OK", compound=LEFT, image=self.okbuttonimage, command=self.ok, default=ACTIVE )
        self.okbutton.grid( row=0, column=0 )
        self.cancelbuttonimage = PhotoImage( file='icons/cancel.gif' )
        self.cancelbutton = Button( master, text="Cancel", compound=LEFT, image=self.cancelbuttonimage, command=self.cancel)
        self.cancelbutton.grid( row=0, column=1 )
        
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

    def validate( self ):
        for item in self.entriestable:
            if item[0].get() == 'english_name':
                break
        else:
            ErrorDialog( self, 'Node must contain english_name attribute' )
            return False

        if self.localChanges:
            dlg = YesNoDialog( self, "Apply Changes To All Existing Nodes?", "Verify" )
            if not dlg.yes:
                return False
            
        return True
        
    def apply( self ):
        if self.localChanges:
            self.node = self.nodelocal

        # update the nodelist based on changes in the nodeInfoFrames
#        nodelist = globalNodeListMeta.get()
#        for item in self.entriestable:
#            if hasattr( nodelist[ 0 ], item[0].get() ):
#                if isinstance( nodelist[ idx ].__dict__[ item[0].get() ], MultiEntry ):
#                    nodelist[ 0 ].__dict__[ item[0].get() ].entry = item[1].get()
#                    nodelist[ 0 ].__dict__[ item[0].get() ].valid_entries = list( item[1].get_values() )
#                else:
#                    nodelist[ 0 ].__dict__[ item[0].get() ] = item[1].get()

#        self.node = nodelist[0]
   

    def onAddSingleClick( self, event=None ):
        dlg = AddSingleEntryDialog( self )
        if dlg.key is not None:
            if hasattr( self.nodelocal, dlg.key ):
                ErrorDialog( self, "Node alread contains attribute %s" % dlg.key )
                return

            self.nodelocal.__dict__[ dlg.key ] = dlg.value
            
            e1 = StringVar()
            e2 = StringVar()
            idx = len( self.entriestable )
            self.entriestable.append( [ Entry( self.entriesframe, textvariable=e1, disabledforeground='Black' ),
                                        Entry( self.entriesframe, textvariable=e2 ),
                                        Button( self.entriesframe,
                                                compound=LEFT,
                                                image=self.deleteEntryButtonImage,
                                                command=(lambda idx=idx: self.onDeleteEntryButtonClick( idx )) )] )
            e1.set( dlg.key )
            e2.set( dlg.value )
            
            self.displayEntriesTable()
            self.localChanges = True
            
    def onAddMultiClick( self, event=None ):
        dlg = AddMultiEntryDialog( self )
        if dlg.key is not None:
            if hasattr( self.nodelocal, dlg.key ):
                ErrorDialog( self, "Node alread contains attribute %s" % dlg.key )
                return

            self.nodelocal.__dict__[ dlg.key ] = MultiEntry( dlg.values[0], dlg.values )

            e1 = StringVar()
            e2 = StringVar()
            idx = len( self.entriestable )
            self.entriestable.append( [ Entry( self.entriesframe, textvariable=e1, disabledforeground='Black' ),
                                        ExtendedOptionMenu( self.entriesframe, e2, *(tuple( dlg.values )) ),
                                        Button( self.entriesframe,
                                                compound=LEFT,
                                                image=self.deleteEntryButtonImage,
                                                command=(lambda idx=idx: self.onDeleteEntryButtonClick( idx )) )] )
            e1.set( dlg.key )
            e2.set( dlg.values[0] )
            
            self.displayEntriesTable()
            self.localChanges = True

    def createEntriesTable( self ):
        idx = 0
        for key in self.nodelocal.keys():

            value = self.nodelocal.__dict__[ key ]
            if isinstance( value, MetaEntry ):
                continue
            
            e1 = StringVar()
            e2 = StringVar()
            optionentry = StringVar()

            if isinstance( value, MultiEntry ):
                self.entriestable.append( [ Entry( self.entriesframe,
                                                   textvariable=e1,
                                                   disabledforeground='Black' ),

                                            ExtendedOptionMenu( self.entriesframe,
                                                                optionentry,
                                                                *(tuple(value.valid_entries) ) ),

                                            Button( self.entriesframe,
                                                    compound=LEFT,
                                                    image=self.deleteEntryButtonImage,
                                                    command=(lambda idx=idx: self.onDeleteEntryButtonClick( idx )) ) ] )
                e1.set( key )
                optionentry.set( value.entry )
            else:
                self.entriestable.append( [ Entry( self.entriesframe,
                                                   textvariable=e1,
                                                   disabledforeground='Black' ),

                                            Entry( self.entriesframe,
                                                   textvariable=e2 ),

                                            Button( self.entriesframe,
                                                    compound=LEFT,
                                                    image=self.deleteEntryButtonImage,
                                                    command=(lambda idx=idx: self.onDeleteEntryButtonClick( idx ))) ] )
                e1.set( key )
                e2.set( value )

            for i in range( len( self.entriestable ) ):
                createToolTip( self.entriestable[i][2], "Delete Entry" )

            idx += 1


    def onDeleteEntryButtonClick( self, idx ):
        if idx >= len( self.entriestable ) or idx < 0:
            return

        keyname = self.entriestable[ idx ][0].get()
        del self.nodelocal.__dict__[ keyname ]
        self.clearEntriesTable()
        self.createEntriesTable()
        self.displayEntriesTable()
        self.localChanges = True
        
    def clearEntriesTable( self ):
        self.undisplayEntriesTable()
        self.entriestable = list()

    def undisplayEntriesTable( self ):
        for i in range( len( self.entriestable ) ):
            self.entriestable[i][0].grid_remove()
            self.entriestable[i][1].grid_remove()
            self.entriestable[i][2].grid_remove()

    def displayEntriesTable( self ):
        for i in range( len( self.entriestable ) ):
            self.entriestable[i][0].config( state=DISABLED )
            self.entriestable[i][0].grid( row=i, column=0, sticky=NSEW )
            self.entriestable[i][1].grid( row=i, column=1, sticky=NSEW )
            self.entriestable[i][2].grid( row=i, column=2, sticky=NSEW )

        self.entriesframe.grid( row=1, column=0, sticky=NSEW )

class AdvancedConfigEditorWindow( StandardConfigEditorWindow ):
    def __init__( self, parent=None, **kwargs ):
        StandardConfigEditorWindow.__init__( self, parent, readonly=False, **kwargs )
        self.winfo_toplevel().title( "Node Configuration Editor -- Advanced Mode" )

    def createWidgetsHook( self ):

        self.commitNodeListButtonImage = PhotoImage( file='icons/commit.gif' )
        self.commitNodeListButton = Button( self.nodelistbuttonsgroup,
                                    compound=LEFT,
                                    text='Commit Changes',
                                    image=self.commitNodeListButtonImage,
                                    command=self.onCommitNodeListButtonClick,
                                    state=DISABLED )

        self.commitNodeListButton.grid( row=0, column=2, sticky=W )

        self.spacerFrame1 = Frame( self.nodelistbuttonsgroup, width=10 );
        self.spacerFrame1.grid( row=0, column=3, sticky=W )

        self.addNodeButtonImage = PhotoImage( file='icons/addnode.gif' )
        self.addNodeButton = Button( self.nodelistbuttonsgroup,
                                     compound=LEFT,
                                     image=self.addNodeButtonImage,
                                     command=self.onAddNodeButtonClick,
                                     state=DISABLED )

        self.addNodeButton.grid( row=0, column=4, sticky=W )


        self.deleteNodeButtonImage = PhotoImage( file='icons/deletenode.gif' )
        self.deleteNodeButton = Button( self.nodelistbuttonsgroup,
                                        compound=LEFT,
                                        image=self.deleteNodeButtonImage,
                                        command=self.onDeleteNodeButtonClick,
                                        state=DISABLED )

        self.deleteNodeButton.grid( row=0, column=5, sticky=W )

        self.copyNodeButtonImage = PhotoImage( file='icons/copy.gif' )
        self.copyNodeButton = Button( self.nodelistbuttonsgroup,
                                      compound=LEFT,
                                      image=self.copyNodeButtonImage,
                                      command=self.onCopyNodeButtonClick,
                                      state=DISABLED )
        
        self.copyNodeButton.grid( row=0, column=6, sticky=W )

        self.editGlobalNodeAttributesButtonImage = PhotoImage( file='icons/editattributes.gif' )
        self.editGlobalNodeAttributesButton = Button( self.nodelistbuttonsgroup,
                                                      compound=LEFT,
                                                      image=self.editGlobalNodeAttributesButtonImage,
                                                      command=self.onEditGlobalNodeAttributesButtonClick,
                                                      state=DISABLED )

        self.editGlobalNodeAttributesButton.grid( row=0, column=7, sticky=W )

        self.spacerFrame2 = Frame( self.nodelistbuttonsgroup, width=10 )
        self.spacerFrame2.grid( row=0, column=8, sticky=W )

        self.reclaimNodeButton = Button( self.nodelistbuttonsgroup,
                                         compound=LEFT,
                                         image=self.releaseNodeButtonImage,
                                         command=self.onReclaimNodeButtonClick,
                                         state=DISABLED )

        self.reclaimNodeButton.grid( row=0, column=9, sticky=W )

        self.saveNodeListButtonImage = PhotoImage( file='icons/save.gif' )
        self.saveNodeListButton = Button( self.nodelistbuttonsgroup,
                                          compound=LEFT,
                                          image=self.saveNodeListButtonImage,
                                          command=self.onSaveNodeListButtonClick,
                                          state=DISABLED )

        self.saveNodeListButton.grid( row=0, column=10, sticky=W )


        self.refreshNodeListButtonImage = PhotoImage( file='icons/refresh.gif' )
        self.refreshNodeListButton = Button( self.nodelistbuttonsgroup,
                                             compound=LEFT,
                                             image=self.refreshNodeListButtonImage,
                                             command=self.onRefreshNodeListButtonClick,
                                             state=DISABLED )

        self.refreshNodeListButton.grid( row=0, column=11, sticky=W )

        # make the scrollbar

        self.nodestatusboxscrollbar = AutoScrollbar( self.nodelistpane )
        self.nodestatusboxscrollbar.grid( row=1, column=3, sticky=N+S )

        self.nodestatusbox = SelectionControlListbox( self.nodelistpane,
                                                      yscrollcommand=self.nodestatusboxscrollbar.set,
                                                      exportselection=False,
                                                      state=DISABLED,
                                                      disabledforeground='black' )


        self.nodelistpane.columnconfigure( 2, weight=1 )
        self.nodestatusbox.grid( row=1, column=2, sticky=NSEW )

        self.nodestatusboxlabel = Label( self.nodelistpane, text="Owner" )
        self.nodestatusboxlabel.grid( row=0, column=2, sticky=E+W )


        createToolTip( self.addNodeButton, 'Add New Node' )
        createToolTip( self.deleteNodeButton, 'Delete Node' )
        createToolTip( self.copyNodeButton, 'Copy Existing Node' )
        createToolTip( self.editGlobalNodeAttributesButton, 'Edit Global Node Attributes' )
        createToolTip( self.reclaimNodeButton, 'Reclaim Node From Owner' )
        createToolTip( self.commitNodeListButton, 'Commit Changes To Server' )
        createToolTip( self.saveNodeListButton, 'Save Changes Temporarily' )
        createToolTip( self.refreshNodeListButton, 'Refresh Changes From Cache' )        

    def onRefreshNodeListButtonClick( self ):
        if self.transactionID:
            self.startClientThread()
            if clientthread:
                clientthread.requestNodeListData( self.transactionID )
                clientthread.requestNodeListMeta( self.transactionID )
            else:
                ErrorDialog( self, 'ERROR: Client Thread Off-Line' )

    def onReclaimNodeButtonClick( self ):
        sel = self.nodelistbox.curselection()
        if sel:
            english_name = self.nodelistbox.get( sel[0] )
            nodelist = globalNodeListData.get()
            idx = self.getNodeListIndex( english_name )
            
            self.startClientThread()
            
            nodelist[idx].claimed.value = False
            nodelist[idx].claimed_by.value = None

            self.nodestatusbox.config( state=NORMAL )
            self.nodestatusbox.delete( idx )
            self.nodestatusbox.insert( idx, 'Unclaimed' )
            self.nodestatusbox.config( state=DISABLED )
            
            self.pendingTransactions.insert( 0, ReleaseNodeTransaction( idx, nodelist, self.transactionID ) )
            clientthread.saveNodeListData( nodelist, self.transactionID )

    def claimedNodeTransactionHandler( self, transaction ):
        self.nodestatusbox.config( state=NORMAL )
        self.nodestatusbox.delete( transaction.idx )
        self.nodestatusbox.insert( transaction.idx, transaction.nodelist[transaction.idx].claimed_by.value )
        self.nodestatusbox.config( state=DISABLED )

        self.nodelistbox.itemconfig( transaction.idx, foreground='green', selectbackground='green' )

        self.claimedNode( transaction )
        self.onNodeSelect( None )

    def releaseNodeTransactionHandler( self, transaction ):
        globalNodeListData.set( transaction.nodelist )

        self.nodestatusbox.config( state=NORMAL )
        self.nodestatusbox.delete( transaction.idx )
        self.nodestatusbox.insert( transaction.idx, 'Unclaimed' )
        self.nodestatusbox.config( state=DISABLED )
 
        self.releasedNode( transaction )
        self.onNodeSelect( None )


    def onEditGlobalNodeAttributesButtonClick( self ):
        addDlg = CreateNodeDialog( self.parent, 'Enter Global Node Attributes' )
        metanode = addDlg.node
        if metanode:
            nl = globalNodeListMeta.get()
            nl[0] = metanode
            globalNodeListMeta.set( nl )
            self.localChanges = True

            # remove attributes not in meta from nodes
            nl = globalNodeListData.get()
            for node in nl:
                for attr in node.__dict__.keys():
                    if attr not in metanode.__dict__.keys():
                        del node.__dict__[ attr ]  # remove it

            # add attributes in meta, but not in nodes
            for node in nl:
                for attr in metanode.__dict__.keys():
                    if attr not in node.__dict__.keys():
                         # set to default value
                        node.__dict__[ attr ] = metanode.__dict__[ attr ]

            globalNodeListData.set( nl )
            self.cleanupNodeInfoWidgets()
            for node in nl:
                self.createNodeInfoWidgets( node )

    def onAddNodeButtonClick( self ):
        import copy
        nodelist = globalNodeListMeta.get()
        node = copy.deepcopy( nodelist[0] )

        for key in node.keys():
            value = node.__dict__[ key ]
            if isinstance( value, MetaEntry ):
                continue
            elif isinstance( value, MultiEntry ):
                continue
            elif key == 'english_name':
                node.__dict__[ key ] = "NewNode"
            else:
                node.__dict__[ key ] = ''

        nl = globalNodeListData.get()

        self.insertNodeListBoxEntry( END, node )
        self.createNodeInfoWidgets( node )

        nl.append( node )
        globalNodeListData.set( nl )

        self.nodelistbox.selection_clear( 0, END )
        self.nodelistbox.selection_set( END )
        self.onNodeSelect( None )

        if self.nodesReceivedCount:
            self.localChanges = True

    def onDeleteNodeButtonClick( self ):
        sel = self.nodelistbox.curselection()
        if sel:
            english_name = self.nodelistbox.get( sel[0] )
            if clientthread is None:
                self.startClientThread()

            nodelist = globalNodeListData.get()
            for node in nodelist:
                if node.english_name == english_name:
                    nodelist.remove( node )
                    break

            idx = int( sel[0] )
            for widget in self.nodeInfoFrames[ idx ].nodeEditorTable:
                widget[0].grid_remove()
                widget[1].grid_remove()

            self.nodeInfoFrames[ idx ].grid_remove()
            self.nodelistbox.delete( idx )

            self.nodestatusbox.config( state=NORMAL )
            self.nodestatusbox.delete( idx )
            self.nodestatusbox.config( state=DISABLED )

            self.nodeInfoFrames.remove( self.nodeInfoFrames[ idx ] )
            self.activeNodeInfoFrame = None

            if idx == len( self.nodeInfoFrames ):
                idx = max( idx-1, 0 )
                                                          
            self.nodelistbox.selection_clear( 0, END )

            if len( self.nodeInfoFrames ):
                self.nodelistbox.selection_set( idx )
                self.onNodeSelect( None )

                self.activeNodeInfoFrame = self.nodeInfoFrames[ idx ]
            else:
                self.createNodePropertiesButton.config( state=DISABLED )
                self.disableButtonsHook()

            if self.nodesReceivedCount:
                self.localChanges = True
                
            globalNodeListData.set( nodelist )

    def onCommitNodeListButtonClick( self ):
        self.startClientThread()
        if clientthread is not None:

            self.onSaveNodeListButtonClick()
            
            self.pendingTransactions.insert( 0, CommitTransaction( self.transactionID ) )
            clientthread.commitTransaction( self.transactionID )
        
    def onSaveNodeListButtonClick( self ):
#        import pdb; pdb.set_trace()
        self.startClientThread()
        if clientthread is not None:
            nodelist = globalNodeListData.get()

            # update the nodelist based on changes in the nodeInfoFrames
            for idx in range( len( nodelist ) ):
                for item in self.nodeInfoFrames[ idx ].nodeEditorTable:
                    if hasattr( nodelist[ idx ], item[0].get() ):
                        if isinstance( nodelist[ idx ].__dict__[ item[0].get() ], MultiEntry ):
                            nodelist[ idx ].__dict__[ item[0].get() ].entry = item[1].get()
                            nodelist[ idx ].__dict__[ item[0].get() ].valid_entries = list( item[1].get_values() )
                        else:
                            nodelist[ idx ].__dict__[ item[0].get() ] = item[1].get()

            self.pendingTransactions.insert( 0, SaveDataTransaction( nodelist, self.transactionID ) )
            clientthread.saveNodeListData( nodelist, self.transactionID )

            nodelist = globalNodeListMeta.get()
            self.pendingTransactions.insert( 0, SaveMetaTransaction( nodelist, self.transactionID ) )
            clientthread.saveNodeListMeta( nodelist, self.transactionID )

    def onCopyNodeButtonClick( self ):
        sel = self.nodelistbox.curselection()
        if sel:
            english_name = self.nodelistbox.get( sel[0] )

            nl = globalNodeListData.get()
            
            idx = self.getNodeListIndex( english_name )

            import copy
            node = copy.deepcopy( nl[ idx ] )

            self.insertNodeListBoxEntry( idx, node )
            self.createNodeInfoWidgets( node )

            nl.append( node )
            globalNodeListData.set( nl )

            self.nodelistbox.selection_clear( 0, END )
            self.nodelistbox.selection_set( END )
            self.onNodeSelect( None )

            self.localChanges = True

    def clearNodeListBoxEntries( self ):
        self.nodelistbox.delete( 0, END )
        self.nodestatusbox.config( state=NORMAL )
        self.nodestatusbox.delete( 0, END )
        self.nodestatusbox.config( state=DISABLED )

    def insertNodeListBoxEntry( self, index, node ):
        self.nodelistbox.insert( index, node.english_name )
        claimstr = "Unclaimed"
        if node.claimed.value:
            claimstr = node.claimed_by.value

        self.nodestatusbox.config( state=NORMAL )
        self.nodestatusbox.insert( index, claimstr )
        self.nodestatusbox.config( state=DISABLED )
            

#    def modifyNodeListBoxEntry( self, index, node ):
#        pass
#        if node.claimed.value:
#            if node.claimed_by.value == socket.getfqdn():
#                self.nodelistbox.itemconfig( idx, foreground='green', selectbackground='green' )
#            else:
#                self.nodelistbox.disable( idx )

    def enableButtonsHook( self ):
        StandardConfigEditorWindow.enableButtonsHook( self )
        
        self.commitNodeListButton.config( state=NORMAL )
        self.addNodeButton.config( state=NORMAL )
        self.saveNodeListButton.config( state=NORMAL )
        self.editGlobalNodeAttributesButton.config( state=NORMAL )
        self.reclaimNodeButton.config( state=NORMAL )
        self.deleteNodeButton.config( state=NORMAL )
        self.copyNodeButton.config( state=NORMAL )
        self.refreshNodeListButton.config( state=NORMAL )        

    def disableButtonsHook( self ):
        StandardConfigEditorWindow.disableButtonsHook( self )
        self.createNodePropertiesButton.config( state=DISABLED )
        self.deleteNodeButton.config( state=DISABLED )
        self.copyNodeButton.config( state=DISABLED )
        self.reclaimNodeButton.config( state=DISABLED )
        #self.commitNodeListButton.config( state=DISABLED )
        #self.createNodeButton.config( state=DISABLED )


    
    def handleReceivedNodeListMetaEvent( self, event ):
        StandardConfigEditorWindow.handleReceivedNodeListMetaEvent( self, event )
        
        self.addNodeButton.config( state=NORMAL )
        self.editGlobalNodeAttributesButton.config( state=NORMAL )

    def handleReceivedNodeListCheckoutEvent( self, event ):
        StandardConfigEditorWindow.handleReceivedNodeListCheckoutEvent( self, event )

        if event.nodelist_meta:
            self.addNodeButton.config( state=NORMAL )
            self.editGlobalNodeAttributesButton.config( state=NORMAL )

def main( argc, argv ):

    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option( "-p", "--port",
                       dest="port",
                       type="int",
                       help="specify server port",
                       default=5007,
                       metavar="PORT" )
    parser.add_option( "-s", "--server",
                       dest="server",
                       type="string",
                       help="server address",
                       default="localhost",
                       metavar="ADDRESS" )

    parser.add_option( "-a", "--advanced",
                       dest="advanced",
                       action="store_true",
                       default=False,
                       help="run in advanced mode allowing node additions to master list" )

    parser.add_option( "-d", "--debug",
                       dest="debug",
                       action="store_true",
                       default=False,
                       help="extra debug info print to status pane" )

    ( options, args ) = parser.parse_args()

    GlobalOptions.server = options.server
    GlobalOptions.port = options.port
    GlobalOptions.debug = options.debug

    root = Tk()

    if options.advanced:
        GlobalOptions.advanced = True
        mainframe = AdvancedConfigEditorWindow( root )
    else:
        GlobalOptions.advanced = False
        mainframe = StandardConfigEditorWindow( root )
    
    mainframe.mainloop();

    return 0


if __name__ == "__main__":
    import sys
    sys.exit( main( len( sys.argv ), sys.argv ) )
