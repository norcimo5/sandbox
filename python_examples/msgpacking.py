#!/usr/bin/env python

import struct
  
controlcode = [ 251923723, 185205511 ]
headerlength = 20

def pack( text, sequence_number=1, total_messages=1 ):
    return struct.pack( '!2L 3L ' + str( len( text ) ) + 's',
                        controlcode[0],
                        controlcode[1],
                        len( text ),
                        sequence_number,
                        total_messages,
                        text )
                        
def unpack_header( text ):
    umsg = Msg
    ( cc1, cc2, msgsize, seqno, total ) = struct.unpack( '!2L 3L', text[ : headerlength ] )
    return ( msgsize, seqno, total )


class Msg:
    def __init__( self, text, sequence_number, total_messages ):
        self.text = text
        self.sequence_number = sequence_number
        self.total_messages = total_messages

class MsgStream:
    def __init__( self, text = str() ):
        self.stream = text

    def __iter__( self ): return self

    def append( self, text ):
        self.stream +=  text

    def next( self ):

        if not self.stream:
            raise StopIteration

        workingset = self.stream
        if len( self.stream ) < headerlength:
            raise StopIteration
        else:
            try:
                ( msgsize, seqno, total ) = unpack_header( self.stream )
                if len( self.stream ) < headerlength + msgsize:
                    raise StopIteration
                else:
                    text = self.stream[headerlength:headerlength+msgsize]
                    msg = Msg( text, seqno, total )
                    self.stream = self.stream[headerlength+msgsize:]
                    return msg
            except struct.error, msg:
                print "MsgStream encountered invalid bytes in stream, parse error=", msg
                self.stream = self.stream[headerlength+msgsize:]
                raise StopIteration
        
            

def main( argc, argv ):

    return 0;


if __name__ == "__main__":
    import sys
    sys.exit( main( len( sys.argv ), sys.argv ) )
