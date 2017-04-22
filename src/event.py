import functools

"""
This class holds a queue of events based on the passed in events file, and
allows access to queue members.
"""
class EventQueue:
    def __init__( self ):
        self.queue = []

    #add events to the queue
    def addEvent( self, event ):
        self.queue.append( event )

    #prepare the queue
    def prepare( self ):
        self.queue = sorted(
            self.queue,
            key=functools.cmp_to_key( lambda x, y: ( x.roundNum > y.roundNum ) - ( x.roundNum < y.roundNum ) )
        )

    #get events for a given round number, return as a list
    def getEvents( self, roundNum ):
        events = []

        while self.queue and self.queue[0].roundNum == roundNum:
            events.append( self.queue[0] )
            self.queue = self.queue[1:]

        return events

    #returns if there are any events
    def hasEvents( self ):
        return len( self.queue ) > 0

    def __str__( self ):
        return str( self.queue )

#class to represent an event. Holds the round num, involved nodes, and cost
class Event:
    def __init__( self, roundNum, router1, router2, cost ):
        self.roundNum = roundNum
        self.router1  = router1
        self.router2  = router2
        self.cost     = cost

    def __str__( self ):
        return str( ( self.roundNum, self.router1, self.router2, self.cost ) )
