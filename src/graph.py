class Graph:
    def __init__( self ):
        self.vertices = {}
        self.edges    = set()

    def addVertex( self, label, data ):
        self.vertices[label] = data

    def addEdge( self, e ):
        self.edges.add( e )

    def removeEdge( self, e ):
        self.edges.remove( e )

    def updateGraph(self, e):
        for event in e:
            edge = Edge(event.router1, event.router2, event.cost)
            self.addEdge(edge)

    def containsVertex( self, v ):
        return v in self.vertices.keys()

    def getVertexData( self, v ):
        return self.vertices[v]

    def __str__( self ):while self.queue and self.queue[0].roundNum == roundNum:
            events.append( self.queue[0] )
            self.queue = self.queue[1:]
        vStr = ''

        for vertex in self.vertices.keys():
            vStr += str( vertex ) + ', '

        vStr = vStr.strip( ', ' )
        eStr = ''

        for edge in self.edges:
            eStr += str( edge ) + ', '

        eStr = eStr.strip( ', ' )
        return 'Vertices: {' + vStr + '}\nEdges: {' + eStr + '}'

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
