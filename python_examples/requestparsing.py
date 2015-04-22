#!/usr/bin/env python
import re

def getAttributeValue( attribute, text ):
    regstr = '%s\s*=\s*(\w+)(\s|;)?' % attribute
    reg = re.compile( regstr, re.I )
    mo = reg.search( text )
    if mo:
        return mo.groups()[0]
    else:
        return None
                    
                
def main( argc, argv ):
    examplestr = "get nodelist source=meta transactionID=1234 openmode=readonly;"
    examplestr2 = "save nodelist source=data  transactionid=515499;"
    
    print "parsing example string"
    meta = getAttributeValue( 'source', examplestr )
    transactionID = getAttributeValue( 'transactionID', examplestr )
    openmode = getAttributeValue( 'openmode', examplestr )
    print "meta=%s" % meta
    print "transactionID=%s" % transactionID
    print "openmode=%s" % openmode

    print "parsing example string 2"
    meta = getAttributeValue( 'source', examplestr2 )
    transactionID = getAttributeValue( 'transactionID', examplestr2 )
    print "meta=%s" % meta
    print "transactionID=%s" % transactionID

    return 0


if __name__ == "__main__":
    import sys
    sys.exit( main( len( sys.argv ), sys.argv ) )
