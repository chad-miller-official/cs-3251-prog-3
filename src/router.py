import math
from copy import deepcopy

"""
Class to represent a router's routing table and other stored values.
Specifically, it contains a routing table, a table of number of hops for certain
paths, pinters to the least cost values in the table, itself's label, and the
next hops for the lowest cost paths.
"""
class RoutingTable:
    def __init__( self, numRouters, router ):
        self.table       = [ [ None for i in range( numRouters ) ] for j in range( numRouters ) ]
        self.numHops     = [ [ 0 for i in range( numRouters ) ] for j in range( numRouters ) ]
        self.coordinates = [ None for i in range( numRouters ) ]
        self.router      = router
        self.hops        = [ None for i in range( numRouters ) ]

    #sets the number of hops it takes to get to a destination
    def setNumHops( self, to, via, hops ):
        self.numHops[to - 1][via - 1] = hops

    #returns the number of hops to a destination
    def getNumHops( self, to, via ):
        return self.numHops[to - 1][via - 1]

    #returns the cost of a certain path in the routing table
    def getCost( self, to, via ):
        return self.table[to - 1][via - 1]

    #sets the cost in the routing table based on an event
    def setCostFromEvent( self, to, via, cost ):
        self.table[to - 1][via - 1] = cost

    #sets cost in the routing table to given value
    def setCost( self, to, via, cost ):
        #print ('From vertex {} telling {} about path to vertex {} with cost: {}'.format(via, self.router, to, cost) )
        if to == self.router or via == self.router:
            return False

        #set if non-existent, a lower cost, or it is an override from previous
        #node of least cost
        if    self.table[to - 1][via - 1] is None \
           or self.table[to - 1][via - 1] >= cost \
           or self.coordinates[to - 1] == ( to, via ):
            self.table[to - 1][via - 1] = cost
            return True

        return False

    #sets the next hop for a given path
    def setHop( self, to, via ):
        if to == self.router or via == self.router:
            self.hops[to-1] = via
        elif to == via:
            self.hops[to-1] = via
        else:
            self.hops[to-1] = via

    #sets the coordinates of the least cost path in a row of the routing table
    def setCoordinate(self, index1, index2):
        self.coordinates[index1 - 1] = (index1, index2)

    #updates all coordinates for least cost paths in each row of the routing table
    def updateCoordinates( self ):
        ret = False

        for c in range( 0, len( self.table ) ):
            if not any( self.table[c] ):
                self.coordinates[c] = None
                self.hops[c]        = 0
                continue

            col = self.table[c].index( min( x for x in self.table[c] if x is not None ) )
            self.setHop( c + 1, col + 1 )

            if self.coordinates[c] != (c + 1, col + 1):
                self.coordinates[c] = (c + 1, col + 1)
                ret = True

        return ret

    #clones this router
    def clone( self ):
        return deepcopy( self )

    def __str__( self ):
        tableStr = ''

        for i in range( 0, len( self.table ) ):
            for j in range( 0, len( self.table[i] ) ):
                if self.table[i][j] is None:
                    tableStr += 'X, '
                else:
                    tableStr += str( self.table[i][j] ) + ', '

            tableStr = tableStr.strip( ', ' )
            tableStr += '\n'

        tableStr  = tableStr.strip( ', \n' )
        tableStr += ''

        return tableStr
