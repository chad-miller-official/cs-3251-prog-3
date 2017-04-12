class RoutingTable:
    def __init__( self, numRouters ):
        self.table       = [ [ None for i in range( numRouters ) ] for j in range( numRouters ) ]
        self.coordinates = [ None for i in range( numRouters ) ]

    def setCost( self, to, via, cost ):
        self.table[to - 1][via - 1] = cost

    def setCoordinate(self, index1, index2):
        self.coordinates[index1 - 1] = (index1, index2)

    def __str__( self ):
        tableStr = '['

        for i in range( 0, len( self.table ) ):
            for j in range( 0, len( self.table[i] ) ):
                tableStr += self.table[i][j] + ', '

            tableStr = tableStr.strip( ', ' )
            tableStr += '\n'

        tableStr  = tableStr.strip( ', ' )
        tableStr += ']'

        return tableStr
