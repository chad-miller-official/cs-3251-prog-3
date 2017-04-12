class Graph:
    def __init__( self ):
        self.vertices = set()
        self.edges    = set()

    def addVertex( self, v, e=[] ):
        self.vertices.add( v )

        for edge in e:
            self.edges.add( e )

    def addEdge( self, e ):
        self.edges.add( e )

    def removeEdge(self, e):
        self.edges.remove(e)

    def containsVertex( self, v ):
        return v in self.vertices

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
        return hashCode

    def __eq__( self, other ):
        if self.label != other.label:
            return False

        return True

    def __str__( self ):
        return '(' + str( self.label ) + ': ' + str( self.data ) + ')'

class Edge:
    def __init__( self, v1, v2, cost ):
        self.v1   = v1
        self.v2   = v2
        self.cost = cost

    def __hash__( self ):
        hashCode = 1
        hashCode = 31 * hash( self.v1 )
        hashCode = 31 * hash( self.v2 )
        return hashCode

    def __eq__( self, other ):
        if self.v1 != other.v1:
            return False

        if self.v2 != other.v2:
            return False

        return True

    def __str__( self ):
        return '([' + str( self.cost ) + '] ' + str( self.v1.label ) + ', ' + str( self.v2.label ) + ')'
