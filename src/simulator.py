#!/usr/bin/python3

import re, sys

from event import Event, EventQueue
from graph import Graph, Edge

BASIC                        = 0
SPLIT_HORIZON                = 1
SPLIT_HORIZON_POISON_REVERSE = 2

def parse_initial_topology( filename ):
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
            topology.addVertex( router1, [ [ None for i in range( num_routers ) ] for j in range( num_routers ) ] )

        if not topology.containsVertex( router2 ):
            topology.addVertex( router2, [ [ None for i in range( num_routers ) ] for j in range( num_routers ) ] )

        topology.addEdge( edge )

    return topology

def parse_topological_events( filename ):
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

def dv_run( network, events, verbose, algoType ):
    changed  = True
    roundNum = 0

    while changed and events.hasEvents():
        print( 'Round ' + str( roundNum ) + '\n' + str( network ) + '\n' )

        roundEvents = events.getEvents( roundNum )
        network.updateGraph( roundEvents )

        if algoType == BASIC:
            # TODO
            pass
        elif algoType == SPLIT_HORIZON:
            # TODO
            pass
        elif algoType == SPLIT_HORIZON_POISON_REVERSE:
            # TODO
            pass

        roundNum += 1

def main( argv ):
    if len( argv ) != 3:
        usage()

    topology           = parse_initial_topology( argv[0] )
    topological_events = parse_topological_events( argv[1] )
    verbose            = int( argv[2] ) == 1

    dv_run( topology, topological_events, verbose, BASIC )
    dv_run( topology, topological_events, verbose, SPLIT_HORIZON )
    dv_run( topology, topological_events, verbose, SPLIT_HORIZON_POISON_REVERSE )

if __name__ == "__main__":
    main( sys.argv[1:] )

sys.exit( 0 )
