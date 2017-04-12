class RoutingTable:
    def __init__( self, numRouters, coordinates=[] ):
        self.table       = [ [ None for i in range( numRouters ) ] for j in range( numRouters ) ]
        self.coordinates = coordinates

    def setCost( self, to, via, cost ):
        self.table[to - 1][via - 1] = cost
