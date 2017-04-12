class Graph:
    def __init__( self ):
        self.vertices = set()
        self.edges    = set()

    def addVertex( self, v, e=[] ):
        self.vertices.add( v )

        for edge in e:
            self.edges.add( e )

    def addEdge( self, v1, v2, cost ):
        self.edges.add( Edge( v1, v2, cost ) )

    def removeEdge( self, v1, v2 ):
        self.edges.remove( Edge( v1, v2 ) )

    def __str__( self ):
        vStr = ''

        for vertex in self.vertices:
            vStr += str( vertex ) + ', '

        vStr = vStr.strip( ', ' )
        eStr = ''

        for edge in self.edges:
            eStr += str( edge ) + ', '

        eStr = eStr.strip( ', ' )
        return 'Vertices: {' + vStr + '}\nEdges: {' + eStr + '}'

class Vertex:
    def __init__( self, label, data ):
        self.label = label
        self.data  = data

    def __hash__( self ):
        hashCode = 1
        hashCode = 31 * hash( self.label )
        hashCode = 31 * hash( self.data )
        return hashCode

    def __eq__( self, other ):
        if self.label != other.label:
            return False

        if self.data != other.data:
            return False

        return True

    def __str__( self ):
        return '(' + self.label + ': ' + str( self.data ) + ')'

class Edge:
    def __init__( self, v1, v2, cost=None ):
        self.v1   = v1
        self.v2   = v2
        self.cost = cost

    def __hash__( self ):
        hashCode = 1
        hashCode = 31 * hash( self.v1 )
        hashCode = 31 * hash( self.v2 )
        hashCode = 31 * hash( self.cost )
        return hashCode

    def __eq__( self, other ):
        if self.v1 != other.v1:
            return False

        if self.v2 != other.v2:
            return False

        return True

    def __str__( self ):
        return '([' + str( self.cost ) + '] ' + self.v1.label + ', ' + self.v2.label + ')'
