#!/usr/bin/python3

import re, sys

from event import Event, EventQueue
from graph import Graph, Edge
from router import RoutingTable

BASIC                        = 0
SPLIT_HORIZON                = 1
SPLIT_HORIZON_POISON_REVERSE = 2

updates = {}

def file_to_undirected_graph( filename ):
    global num_routers

    handle      = open( filename, 'r' )
    num_routers = int( handle.readline() )

    topology = Graph()

    for line in handle:
        match   = re.match( r'(\d+)\s+(\d+)\s+(\d+)', line )
        router1 = int( match.group( 1 ) )
        router2 = int( match.group( 2 ) )
        cost    = int( match.group( 3 ) )

        edge = Edge( router1, router2, cost )

        if not topology.containsVertex( router1 ):
            topology.addVertex( router1, RoutingTable( num_routers, router1 ) )

        if not topology.containsVertex( router2 ):
            topology.addVertex( router2, RoutingTable( num_routers, router2 ) )

        topology.addEdge( edge )
        updates[router1] = True
        updates[router2] = True

    return topology

def file_to_directed_graph( filename ):
    handle      = open( filename, 'r' )
    num_routers = int( handle.readline() )

    topology = Graph()

    for line in handle:
        match   = re.match( r'(\d+)\s+(\d+)\s+(\d+)', line )
        router1 = int( match.group( 1 ) )
        router2 = int( match.group( 2 ) )
        cost    = int( match.group( 3 ) )

        edge1 = Edge( router1, router2, cost )
        edge2 = Edge( router2, router1, cost )

        if not topology.containsVertex( router1 ):
            topology.addVertex( router1, RoutingTable( num_routers, router1 ) )

        if not topology.containsVertex( router2 ):
            topology.addVertex( router2, RoutingTable( num_routers, router2 ) )

        topology.addEdge( edge1 )
        topology.addEdge( edge2 )
        updates[router1] = True
        updates[router2] = True

    return topology

def file_to_topological_events( filename ):
    handle = open( filename, 'r' )

    event_queue = EventQueue()

    for line in handle:
        match     = re.match( r'(\d+)\s+(\d+)\s+(\d+)\s+(-?\d+)', line )
        round_num = int( match.group( 1 ) )
        router1   = int( match.group( 2 ) )
        router2   = int( match.group( 3 ) )
        cost      = int( match.group( 4 ) )

        to_add = Event( round_num, router1, router2, cost )
        event_queue.addEvent( to_add )

    event_queue.prepare()
    return event_queue

def usage():
    print( 'Usage: ./simulator.py <topology file> <event file> <verbose value>' )
    exit( 0 )

def print_network( network ):
    for vertex in network.vertices:
        print( 'Router ' + str( vertex ) + ':' )
        print( str( network.vertices[vertex] ) )
        print( str( network.vertices[vertex].coordinates ) )
        print( '\n' )

def pretty_print( network ):
    global num_routers

    str_2d_array = [ [ None for i in range( num_routers ) ] for j in range( num_routers ) ]

    for router in range( 0, num_routers ):
        routing_table = network.vertices[router + 1]

        for i in range( 0, len( routing_table.coordinates ) ):
            if i == router:
                next_hop = 0
                cost     = 0
            elif routing_table.coordinates[i] is None:
                next_hop = -1
                cost     = -1
            else:
                x, y     = routing_table.coordinates[i]
                next_hop = routing_table.hops[i]
                cost     = routing_table.table[x - 1][y - 1]

            str_2d_array[router][i] = '{},{}'.format( next_hop, cost )

    s = [ [ str( e ) for e in row ] for row in str_2d_array ]
    s.insert( 0, [ str( i ) for i in range( 1, num_routers + 1 ) ] )

    lens  = [ max( map( len, col ) ) for col in zip( *s ) ]
    fmt   = '  '.join( '{{:^{}}}'.format( x ) for x in lens )
    table = [ fmt.format( *row ) for row in s ]

    for i in range( 0, len( table ) ):
        print( '{}  '.format( ' ' if i == 0 else i ) + table[i] )

def setup_network( network, verbose, algoType ):
    for vertex in network.vertices:
        vertexNeighbors = network.getNeighbors( vertex, algoType != BASIC )

        for x in vertexNeighbors.keys():
            network.vertices[vertex].setCost( x, x, vertexNeighbors[x] )
            network.vertices[vertex].setCoordinate(x, x)

def iter_basic( network, verbose ):
    changed = False
    cloned  = {}

    for vertex in network.vertices:
        cloned[vertex] = network.vertices[vertex].clone()

    for vertex in network.vertices:
        if not updates[vertex]:
            continue

        vertex_neighbors = network.getNeighbors( vertex, False )

        for neighbor in vertex_neighbors.keys():
            for to in range( 0, len( network.vertices[vertex].table ) ):
                to_router = to + 1

                if to_router == vertex:
                    continue

                for via in range( 0, len( network.vertices[vertex].table[to] ) ):
                    via_router = via + 1

                    if via_router == vertex:
                        continue

                    existing_cost = cloned[vertex].getCost( to_router, via_router )

                    if existing_cost is not None:
                        new_cost  = existing_cost + network.vertices[neighbor].getCost( vertex, vertex )
                        didChange = network.vertices[neighbor].setCost( to_router, vertex, new_cost )

                        if not changed and didChange:
                            changed = True

    for vertex in network.vertices:
        updates[vertex] = network.vertices[vertex].updateCoordinates()

    return changed

def iter_split_horizon( network, verbose ):
    # TODO
    return True

def iter_split_horizon_poison_reverse( network, verbose ):
    # TODO
    return True

def dv_run( network, events, verbose, algoType ):
    changed  = True
    roundNum = 1

    setup_network( network, verbose, algoType )

    if verbose:
        print( 'Round: 0' )
        pretty_print( network )

    while changed or events.hasEvents():
        if verbose:
            print( '\nRound: ' + str( roundNum ))

        roundEvents = events.getEvents( roundNum )
        network.updateGraph( roundEvents, algoType != BASIC )

        if algoType == BASIC:
            changed = iter_basic( network, verbose )
        elif algoType == SPLIT_HORIZON:
            changed = iter_split_horizon( network, verbose )
        elif algoType == SPLIT_HORIZON_POISON_REVERSE:
            changed = iter_split_horizon_poison_reverse( network, verbose )

        if verbose:
            pretty_print( network )

        roundNum += 1

    if not verbose:
        pretty_print( network )

    print( '\nConvergence Delay: ' + str( roundNum - 1 ) )

def main( argv ):
    if len( argv ) != 3:
        usage()

    topology_filename           = argv[0]
    topological_events_filename = argv[1]
    verbose                     = int( argv[2] ) == 1

    print( 'Variation 1: Basic algorithm\n' )
    topology           = file_to_undirected_graph( topology_filename )
    topological_events = file_to_topological_events( topological_events_filename )
    dv_run( topology, topological_events, verbose, BASIC )

    #print( 'Variation 2: Algorithm with split horizon\n' )
    #topology           = file_to_directed_graph( topology_filename )
    #topological_events = file_to_topological_events( topological_events_filename )
    #dv_run( topology, topological_events, verbose, SPLIT_HORIZON )

    #print( 'Variation 3: Algorithm with split horizon and poison reverse\n' )
    #topology           = file_to_directed_graph( topology_filename )
    #topological_events = file_to_topological_events( topological_events_filename )
    #dv_run( topology, topological_events, verbose, SPLIT_HORIZON_POISON_REVERSE )

if __name__ == "__main__":
    main( sys.argv[1:] )

sys.exit( 0 )
