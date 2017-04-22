"""
Class to represent a network graph, with vertices and edges.
Contains method needed to update the graph.
"""
class Graph:
    def __init__( self ):
        self.vertices = {}
        self.edges    = set()

    #adds a vertex to the graph
    def addVertex( self, label, data ):
        self.vertices[label] = data

    #adds an edge to the graph
    def addEdge( self, e ):
        self.edges.add( e )

    #removes an edge from the graph
    def removeEdge( self, e ):
        self.edges.remove( e )

    #updates a graph's affected edges and vertices from a given list of events.
    def updateGraph(self, e):
        for event in e:
            edge = Edge(event.router1, event.router2, event.cost)

            if event.cost >= 0:
                if edge in self.edges:
                    self.edges.remove( edge )

                self.addEdge(edge)
            else:
                self.removeEdge(edge)

    #returns if a vertex is in this graph
    def containsVertex( self, v ):
        return v in self.vertices.keys()

    #returns vertex data
    def getVertexData( self, v ):
        return self.vertices[v]

    #returns a list of neighbor vertices to the passed in vertice
    def getNeighbors( self, v ):
        neighbors = {}

        for edge in self.edges:
            if edge.v1 == v:
                neighbors[edge.v2] = edge.cost
            elif edge.v2 == v:
                neighbors[edge.v1] = edge.cost

        return neighbors

    #reutrns the cost of the edge between two nodes, if it exists
    def getEdgeCost( self, v1, v2 ):
        for edge in self.edges:
            if    ( edge.v1 == v1 and edge.v2 == v2 ) \
               or ( edge.v1 == v2 and edge.v2 == v1 ):
                return edge.cost

        return None

    def __str__( self ):
        vStr = ''

        for vertex in self.vertices.keys():
            vStr += str( vertex ) + ', '

        vStr = vStr.strip( ', ' )
        eStr = ''

        for edge in self.edges:
            eStr += str( edge ) + ', '

        eStr = eStr.strip( ', ' )
        return 'Vertices: {' + vStr + '}\nEdges: {' + eStr + '}'

"""
Class to represent an edge in the graph. Consists of two vertices and the edge
cost.
"""
class Edge:
    def __init__( self, v1, v2, cost ):
        self.v1   = v1
        self.v2   = v2
        self.cost = cost

    def __hash__( self ):
        hashCode = 1
        hashCode = 31 * hash( self.v1 )
        hashCode = hashCode + ( 31 * hash( self.v2 ) )
        return hashCode

    def __eq__( self, other ):
        if self.v1 == other.v1:
            if self.v2 == other.v2:
                return True
            else:
                return False
        elif self.v1 == other.v2:
            if self.v2 == other.v1:
                return True
            else:
                return False
        else:
            return False

    def __str__( self ):
        return '([' + str( self.cost ) + '] ' + str( self.v1 ) + ', ' + str( self.v2 ) + ')'
