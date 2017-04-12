#!/usr/bin/python

import re, sys
from event import Event, EventQueue

def parse_initial_topology( filename ):
    handle      = open( filename, 'r' )
    num_routers = int( handle.readline() )

    for line in handle:
        match   = re.match( r'(\d+)\s+(\d+)\s+(\d+)', line )
        router1 = int( match.group( 1 ) )
        router2 = int( match.group( 2 ) )
        cost    = int( match.group( 3 ) )

        # TODO put in graph

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
    print 'Usage: ./simulator.py <topology file> <event file> <verbose value>'
    exit( 0 )

def main( argv ):
    # Parse arguments
    if len( argv ) != 3:
        usage()

    topology           = parse_initial_topology( argv[0] )
    topological_events = parse_topological_events( argv[1] )
    verbose            = int( argv[2] ) == 1

    for i in range( 0, 40 ):
        events    = topological_events.getEvents( i )
        event_str = ''

        for event in events:
            event_str += str( event ) + ', '

        event_str = event_str.strip( ', ' )
        print 'Events at round ' + str( i ) + ': ' + event_str

    # TODO

if __name__ == "__main__":
    main( sys.argv[1:] )

sys.exit( 0 )
