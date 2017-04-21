#!/usr/bin/python3

import math, re, sys

from event import Event, EventQueue
from graph import Graph, Edge
from router import RoutingTable

BASIC                        = 0
SPLIT_HORIZON                = 1
SPLIT_HORIZON_POISON_REVERSE = 2

def file_to_undirected_graph( filename ):
    global num_routers, updates

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

def tableize( network, on_round_0=False ):
    global num_routers

    ret_table = [ [ None for i in range( num_routers ) ] for j in range( num_routers ) ]

    for router in range( 0, num_routers ):
        routing_table = network.vertices[router + 1]

        for i in range( 0, len( routing_table.coordinates ) ):
            if i == router:
                next_hop  = i + 1
                cost      = 0
                hop_count = 0
            elif routing_table.coordinates[i] is None:
                next_hop  = -1
                cost      = -1
                hop_count = -1
            else:
                x, y      = routing_table.coordinates[i]
                next_hop  = routing_table.hops[i]
                cost      = routing_table.table[x - 1][y - 1]
                hop_count = routing_table.numHops[x - 1][y - 1]

            ret_table[router][i] = ( next_hop, cost, hop_count )

    return ret_table

def is_count_to_infinity( table ):
    for i in table:
        for j in i:
            if j[1] >= 100 and j[1] != math.inf:
                return True

    return False

def print_network( network ):
    for vertex in network.vertices:
        print( 'Router ' + str( vertex ) + ':' )
        print( str( network.vertices[vertex] ) )
        print( str( network.vertices[vertex].coordinates ) )
        print( '\n' )

def pretty_print( table ):
    global num_routers

    retval = ''

    s = [ [ '{},{}'.format( e[0], e[2] ) for e in row ] for row in table ]
    # s.insert( 0, [ str( i ) for i in range( 1, num_routers + 1 ) ] )

    lens  = [ max( map( len, col ) ) for col in zip( *s ) ]
    fmt   = '    '.join( '{{:{}}}'.format( x ) for x in lens )
    table = [ fmt.format( *row ) for row in s ]

    for i in range( 0, len( table ) ):
        retval += '{}  '.format( i + 1 ) + table[i] + '\n'

    return retval

def setup_network( network, verbose ):
    for vertex in network.vertices:
        vertexNeighbors = network.getNeighbors( vertex )

        for x in vertexNeighbors.keys():
            network.vertices[vertex].setCost( x, x, vertexNeighbors[x] )
            network.vertices[vertex].setCoordinate(x, x)
            network.vertices[vertex].setHop( x, x )
            network.vertices[vertex].setNumHops( x, x, 1 )

def iter_basic( network ):
    global updates

    changed = False
    cloned  = {}

    for vertex in network.vertices:
        cloned[vertex] = network.vertices[vertex].clone()

    for vertex in network.vertices:
        if not updates[vertex]:
            continue

        vertex_neighbors = network.getNeighbors( vertex )

        for neighbor in vertex_neighbors.keys():
            for to in range( 0, len( network.vertices[vertex].table ) ):
                to_router = to + 1

                if to_router == vertex:
                    continue
                if network.vertices[vertex].coordinates[to_router - 1] is not None:
                    via = network.vertices[vertex].coordinates[to_router - 1][1]
                    existing_cost = cloned[vertex].getCost( to_router, via )

                    if existing_cost is not None:
                        new_cost  = existing_cost + network.vertices[neighbor].getCost( vertex, vertex )
                        didChange = network.vertices[neighbor].setCost( to_router, vertex, new_cost )

                        if didChange:
                            hop_count = 1 + cloned[vertex].getNumHops( to_router, via )
                            network.vertices[neighbor].setNumHops( to_router, vertex, hop_count )
                            updates[neighbor] = True

                        if not changed and didChange:
                            changed = True

    return changed

def iter_split_horizon( network ):
    global updates

    changed = False
    cloned  = {}

    for vertex in network.vertices:
        cloned[vertex] = network.vertices[vertex].clone()

    for vertex in network.vertices:
        if not updates[vertex]:
            continue

        vertex_neighbors = network.getNeighbors( vertex )

        for neighbor in vertex_neighbors.keys():
            for to in range( 0, len( network.vertices[vertex].table ) ):
                to_router = to + 1

                if to_router == vertex:
                    continue

                if network.vertices[vertex].coordinates[to_router - 1] is not None:
                    via = network.vertices[vertex].coordinates[to_router - 1][1]
                    existing_cost = cloned[vertex].getCost( to_router, via )
                    if existing_cost is not None:
                        additional_cost = network.vertices[neighbor].getCost( vertex, vertex )

                        if network.vertices[vertex].hops[to] != neighbor:
                            new_cost  = existing_cost + additional_cost
                            didChange = network.vertices[neighbor].setCost( to_router, vertex, new_cost )

                            if didChange:
                                hop_count = 1 + cloned[vertex].getNumHops( to_router, via )
                                network.vertices[neighbor].setNumHops( to_router, vertex, hop_count )
                                updates[neighbor] = True

                            if not changed and didChange:
                                changed = True

    return changed

def iter_split_horizon_poison_reverse( network ):
    global updates

    changed = False
    cloned  = {}

    for vertex in network.vertices:
        cloned[vertex] = network.vertices[vertex].clone()

    for vertex in network.vertices:
        if not updates[vertex]:
            continue

        vertex_neighbors = network.getNeighbors( vertex )

        for neighbor in vertex_neighbors.keys():
            for to in range( 0, len( network.vertices[vertex].table ) ):
                to_router = to + 1

                if to_router == vertex:
                    continue

                if network.vertices[vertex].coordinates[to_router - 1] is not None:
                    via = network.vertices[vertex].coordinates[to_router - 1][1]
                    existing_cost = cloned[vertex].getCost( to_router, via )

                    if existing_cost is not None:
                        additional_cost = network.vertices[neighbor].getCost( vertex, vertex )

                        if network.vertices[vertex].hops[to] != neighbor:
                            new_cost  = existing_cost + additional_cost
                        else:
                            new_cost = math.inf

                        didChange = network.vertices[neighbor].setCost( to_router, vertex, new_cost )

                        if didChange:
                            hop_count = 1 + cloned[vertex].getNumHops( to_router, via )
                            network.vertices[neighbor].setNumHops( to_router, vertex, hop_count )
                            updates[neighbor] = True

                        if not changed and didChange:
                            changed =  True

    return changed

def update_network( network, events ):
    global num_routers, updates

    network.updateGraph( events )

    for e in events:
        r1   = e.router1
        r2   = e.router2
        cost = e.cost

        if cost < 0:
            cost = None

        if cost is None:
            for i in range( 1, num_routers + 1 ):
                print( '{}: to {} via {} -> {}'.format( r1, i, r2, cost ) )
                network.vertices[r1].setCostFromEvent( i, r2, None )
                print( '{}: to {} via {} -> {}'.format( r2, i, r1, cost ) )
                network.vertices[r2].setCostFromEvent( i, r1, None )
        else:
            network.vertices[r1].setCostFromEvent( r2, r2, cost )
            network.vertices[r2].setCostFromEvent( r1, r1, cost )
            network.vertices[r1].setNumHops( r2, r2, 1 )
            network.vertices[r2].setNumHops( r1, r1, 1 )

        updates[r1] = True
        updates[r2] = True

        r1_neighbors = network.getNeighbors( r1 )
        r2_neighbors = network.getNeighbors( r2 )

        for neighbor in r1_neighbors.keys():
            if neighbor == r2:
                continue

            neighbor_r2_cost = network.getEdgeCost( neighbor, r2 )
            neighbor_r1_cost = network.getEdgeCost( neighbor, r1 )

            if neighbor_r2_cost is not None:
                new_cost = cost + neighbor_r2_cost if cost is not None else None
                # print( '{}: to {} via {} -> {}'.format( neighbor, r1, r2, new_cost ) )
                network.vertices[neighbor].setCostFromEvent( r1, r2, new_cost )
                updates[neighbor] = True

            if neighbor_r1_cost is not None:
                new_cost = cost + neighbor_r1_cost if cost is not None else None
                # print( '{}: to {} via {} -> {}'.format( neighbor, r2, r1, new_cost ) )
                network.vertices[neighbor].setCostFromEvent( r2, r1, new_cost )
                updates[neighbor] = True

        for neighbor in r2_neighbors.keys():
            if neighbor == r1:
                continue

            neighbor_r2_cost = network.getEdgeCost( neighbor, r2 )
            neighbor_r1_cost = network.getEdgeCost( neighbor, r1 )

            if neighbor_r2_cost is not None:
                new_cost = cost + neighbor_r2_cost if cost is not None else None
                # print( '{}: to {} via {} -> {}'.format( neighbor, r1, r2, new_cost ) )
                network.vertices[neighbor].setCostFromEvent( r1, r2, new_cost )
                updates[neighbor] = True

            if neighbor_r1_cost is not None:
                new_cost = cost + neighbor_r1_cost if cost is not None else None
                # print( '{}: to {} via {} -> {}'.format( neighbor, r2, r1, new_cost ) )
                network.vertices[neighbor].setCostFromEvent( r2, r1, new_cost )
                updates[neighbor] = True

def dv_run( network, events, verbose, algoType, outfile ):
    global updates

    changed         = True
    round_num       = 2
    last_event_time = 0

    setup_network( network, verbose )

    str_buf = ''

    if verbose:
        str_buf += 'Round 1\n'
        table = tableize( network, True )
        str_buf += pretty_print( table )

    while True:
        round_events = events.getEvents( round_num )

        if len( round_events ) > 0:
            update_network( network, round_events )
            last_event_time = round_num

        if algoType == BASIC:
            changed = iter_basic( network )
        elif algoType == SPLIT_HORIZON:
            changed = iter_split_horizon( network )
        elif algoType == SPLIT_HORIZON_POISON_REVERSE:
            changed = iter_split_horizon_poison_reverse( network )

        for vertex in network.vertices:
            updates[vertex] = network.vertices[vertex].updateCoordinates()

        if not changed and not events.hasEvents():
            break

        table = tableize( network )

        if verbose:
            str_buf += 'Round {}\n'.format( round_num )
            str_buf += pretty_print( table )
            #print( '\n' )
            #print_network( network )

        if is_count_to_infinity( table ):
            sys.exit( 'Encountered a count-to-infinity instability.' )

        round_num += 1

    if not verbose:
        table = tableize( network )
        str_buf += pretty_print( table )

    final_convergence_delay = round_num - 1 - last_event_time

    str_buf += '\nConvergence Delay: {} round{}'.format( final_convergence_delay, 's' if final_convergence_delay != 1 else '' )
    # print( str_buf )

    outfile.write( str_buf )

def main( argv ):
    global updates

    if len( argv ) != 3:
        usage()

    topology_filename           = argv[0]
    topological_events_filename = argv[1]
    verbose                     = int( argv[2] ) == 1

    updates = {}

    outfile_name = 'output-detailed.txt' if verbose else 'output.txt'
    outfile      = open( outfile_name, 'w' )

    outfile.write( 'Variation 1: Basic algorithm\n\n' )
    topology           = file_to_undirected_graph( topology_filename )
    topological_events = file_to_topological_events( topological_events_filename )
    dv_run( topology, topological_events, verbose, BASIC, outfile )

    outfile.write( '\n\n*********************\n\n' )

    outfile.write( 'Variation 2: Algorithm with split horizon\n\n' )
    topology           = file_to_undirected_graph( topology_filename )
    topological_events = file_to_topological_events( topological_events_filename )
    dv_run( topology, topological_events, verbose, SPLIT_HORIZON, outfile )

    outfile.write( '\n\n*********************\n\n' )

    outfile.write( 'Variation 3: Algorithm with split horizon and poison reverse\n\n' )
    topology           = file_to_undirected_graph( topology_filename )
    topological_events = file_to_topological_events( topological_events_filename )
    dv_run( topology, topological_events, verbose, SPLIT_HORIZON_POISON_REVERSE, outfile )

    outfile.close()

if __name__ == "__main__":
    main( sys.argv[1:] )

sys.exit( 0 )
