#!/usr/bin/env python

class MultiEntry:
    def __init__( self, entry, valid_entries ):
        self.entry = entry
        self.valid_entries = valid_entries
        self.iter = 0

    def valid( self ):
        return self.entry in self.valid_entries

    def __str__( self ):
        return self.entry

    def __iter__( self ):
        return self

    def next( self ):
        if self.iter >= len( self.valid_entries ):
            raise StopIteration
        olditer = self.iter
        self.iter += 1
        return self.valid_entries[ olditer ]

class MetaEntry:
    def __init__( self, name, mtype, value ):
        self.name = name
        self.type = mtype.lower()
        if self.type == 'bool':
            if type( value ) is bool:
                self.value = value
            elif type( value ) is str:
                if value.lower() == 'false':
                    self.value = False
                elif value.lower() == 'true':
                    self.value = True
                else:
                    raise Exception( 'unsupported value %s for type %s' % ( value, self.type ) )
            else:
                raise Exception( 'unable to convert from value type (%s) to to type (%s)' % ( type( value ), self.type ) )

        elif self.type == 'str':
            self.value = value
        else:
            raise Exception( 'unrecognized type %s in meta entries field' % self.type )
            


    def to_dict( self ):
        return { self.name : [ {'type': self.type}, {'value':self.value} ] }
        

class Node:

    def __init__( self, nodedict ):
        self.exclude_slots = [ 'iter', 'exclude_slots' ]  # things we dont want in the yaml dictionary
        self.iter = 0
        
        for i in nodedict.keys():
            if type( nodedict[ i ] ) is str:
                self.__dict__[ i ] = nodedict[ i ]
            elif type( nodedict[ i ] ) is list:
                if i == 'meta_entries':
                    for meta_entry in nodedict[ i ]:
                        attrname = meta_entry.keys()[0]
                        if not type( meta_entry[ attrname ] ) is list:
                            raise Exception( 'mal-formed meta_entries field, expected list type for attribute: ' + attrname )

                        typedesc = meta_entry[ attrname ][0]['type']
                        valuedesc = meta_entry[ attrname ][1]['value']

                        self.__dict__[ attrname ] = MetaEntry( attrname, typedesc, valuedesc )
                else:
                    entry_dict = nodedict[ i ][ 0 ]
                    valid_entries_dict = nodedict[ i ][ 1 ]
                    if entry_dict[ 'entry' ] in valid_entries_dict[ 'valid_entries' ]:
                        self.__dict__[ i ] = MultiEntry( entry_dict[ 'entry' ],
                                                         valid_entries_dict[ 'valid_entries' ] )
                    else:
                        raise Exception( 'invalid entry in field %s' % ( i ) )

    def keys( self ):
        from sets import Set as set
        keylist = list( set( self.__dict__.keys() ) - set( self.exclude_slots ) )
        keylist.sort()
        return keylist
        

    def __iter__( self ):
        return self

    def next( self ):
        if self.iter >= len( self.__dict__.keys() ):
            self.iter = 0
            raise StopIteration

        while self.__dict__.items()[ self.iter ][0] in self.exclude_slots:
            self.iter += 1
            if self.iter >= len( self.__dict__.keys() ):
                self.iter = 0
                raise StopIteration
        
        olditer = self.iter
        self.iter += 1

        currentkey = self.__dict__.items()[ olditer ][0]
        currentvalue = self.__dict__[ currentkey ]

        if isinstance( currentvalue, MultiEntry ):
            return ( currentkey, [ { 'entry' : currentvalue.entry },
                                   { 'valid_entries' : currentvalue.valid_entries } ] )
        elif isinstance( currentvalue, MetaEntry ):
            return currentvalue
        else:
            return self.__dict__.items()[ olditer ]

    def to_dict( self ):

        nodedict = dict()
        metaentries = list()
        for item in self.__dict__.keys():
            if item in self.exclude_slots:
                continue
            
            currentkey = item
            currentvalue = self.__dict__[ item ]
            if isinstance( currentvalue, MultiEntry ):
                nodedict[ currentkey ] = [ { 'entry' : currentvalue.entry },
                                           { 'valid_entries' : currentvalue.valid_entries } ]
                
            elif isinstance( currentvalue, MetaEntry ):
                metaentries.append( { currentvalue.name : [ { 'type' : currentvalue.type }, { 'value' : currentvalue.value } ] } )
            else:
                nodedict[ currentkey ] = currentvalue

        if metaentries:
            nodedict[ 'meta_entries' ] = list()

        for item in metaentries:
            nodedict[ 'meta_entries' ].append( item )

        return nodedict


class NodeList( list ):

    def __init__( self ):
        self.iterator = 0
        self.descriptor = 'NodeList_data'

    def copy( self ):
        import copy
        return copy.deepcopy( self )

    def initialize( self, yamldict, descriptor ):
        self.iterator = 0
        self.descriptor = descriptor
        for item in yamldict[ self.descriptor ]:
            self.append( Node( item ) )
        
    def __repr__( self ):
        s = "%s:\n" % self.__class__.__name__
        for i in self:
            s += "\titem:\n"
            s += "\t\t%s\n" % i

        return s

    def to_dict( self ):
        nodedict = dict()
        nodedict[ self.descriptor ] = list()
        for item in self:
            nodedict[ self.descriptor ].append( item.to_dict() )

        sorteddict = dict()
        keys = nodedict.keys()
        keys.sort()
        for item in keys:
            sorteddict[ item ] = nodedict[ item ]

        return sorteddict

class NodeListSynchronizer:
    def __init__( self, nodelist=None ):
        import threading
        self.lock = threading.RLock()
        if nodelist is not None:
            self.nodelist = nodelist.copy()
        else:
            self.nodelist = NodeList()

    def get( self ):
        try:
            self.lock.acquire()
            return self.nodelist.copy()
        finally:
            self.lock.release()


    def set( self, nodelist ):
        try:
            self.lock.acquire()
            self.nodelist = nodelist.copy()
        finally:
            self.lock.release()


def main( argc, argv ):
    # test code
#    import pdb; pdb.set_trace()
    import yaml
    print "opening nodelist_data.yaml"
    fil = open( "nodelist_data.yaml" )
    print "reading nodelist_data.yaml"
    buf = yaml.load( fil )
    print "creating NodeList object from:\n\n", buf
    n = NodeList()
    n.initialize( buf, 'NodeList_data' )
    print "NodeList Object:\n\n"
    print n

    print "Dumping NodeList Object to dict:\n\n"
#    import pdb; pdb.set_trace()
    d = n.to_dict()
    print d

    print "Dumping Generated dict to yaml:\n\n"
    ddoc = yaml.dump( d, default_flow_style=False )
    print ddoc
    
    print "Creating second NodeList object from generated yaml:\n\n"
    d = yaml.load( ddoc )
    n2 = NodeList()
    n2.initialize( d, 'NodeList_data' )
    print "Dumping second NodeList Object to dict:\n\n"
    d2 = n2.to_dict()
    print d2

    print "Generating yaml from second dict:\n\n"
    ddoc2 = yaml.dump( d2, default_flow_style=False )
    print "Generated yaml:\n\n"
    print ddoc2

    print "\nNodeList[0]:\n\n"
    for item in n2[0]:
        if isinstance( item, MetaEntry ):
            print "MetaEntry: name=%s type=%s value=%s" % ( item.name, item.type, item.value )
        else:
            print item
        

    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit( main( len( sys.argv ), sys.argv ) )
