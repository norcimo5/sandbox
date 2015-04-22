#!/usr/bin/env python

class RoutingError:
    def __init__( self, msg ):
        self.msg = msg
    def __str__( self ):
        return self.msg

class RequestRouter:
    def __init__( self, thesocket ):
        self.handlers = dict()
        self.socket = thesocket
        
    def add_handler( self, regex, handler ):
        self.handlers[ regex ] = handler

    def route( self, command ):
        routed = False
        for i in self.handlers.keys():
            mo = i.search( command )
            if mo:
                routed = self.handlers[ i ]( self.socket, command )
                break
        else:
            raise RoutingError( "no handler found for " + command )

        return routed
                
def main( argc, argv ):
    return 0


if __name__ == "__main__":
    import sys
    sys.exit( main( len( sys.argv ), sys.argv ) )
