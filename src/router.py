from copy import deepcopy

class RoutingTable:
    def __init__( self, numRouters, router ):
        self.table       = [ [ None for i in range( numRouters ) ] for j in range( numRouters ) ]
        self.coordinates = [ None for i in range( numRouters ) ]
        self.router      = router

    def getCost( self, to, via ):
        return self.table[to - 1][via - 1]

    def setCost( self, to, via, cost ):
        if to == self.router or via == self.router:
            return False

        if self.table[to - 1][via - 1] != cost:
            self.table[to - 1][via - 1] = cost
            return True

        return False

    def setCoordinate(self, index1, index2):
        self.coordinates[index1 - 1] = (index1, index2)

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
