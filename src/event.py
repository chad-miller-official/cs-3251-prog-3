import functools

class EventQueue:
    def __init__( self ):
        self.queue = []

    def addEvent( self, event ):
        self.queue.append( event )

    def prepare( self ):
        self.queue = sorted(
            self.queue,
            key=functools.cmp_to_key( lambda x, y: ( x.roundNum > y.roundNum ) - ( x.roundNum < y.roundNum ) )
        )

    def getEvents( self, roundNum ):
        events = []

        while self.queue and self.queue[0].roundNum == roundNum:
            events.append( self.queue[0] )
            self.queue = self.queue[1:]

        return events

    def hasEvents( self ):
        return len( self.queue ) > 0

    def __str__( self ):
        return str( self.queue )

class Event:
    def __init__( self, roundNum, router1, router2, cost ):
        self.roundNum = roundNum
        self.router1  = router1
        self.router2  = router2
        self.cost     = cost

    def __str__( self ):
        return str( ( self.roundNum, self.router1, self.router2, self.cost ) )
