# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>


# Import standard libraries
import random

from edu.umich.cscs.rps.agents import Player

##################################################################
# to test, run as follows
#     python entrants/playersRiolo.py

class  PlayerR4( Player ):
    def __init__( self ):
        # Set name and number, then call parent constructor.
        name = "riolo"
        number = "4"
        super(PlayerR4, self).__init__(name, number)
        self.oppfreqR = 0.0
        self.oppfreqP = 0.0
        self.oppfreqS = 0.0
        self.strategy = [ 0.2, 0.5]
        self.defaultStrategy = [ 0.2, 0.5]
        
        
    def yourOpponentsId(self, lastname_id):
        '''
        Handler for being informed of opponent's identity.
        '''
        self.oppId = lastname_id

    def makePureRandomMove(self):
        '''
        Make an equal probability random move.
        '''
        r = random.random()    # uniform( 0.0, 1.0 ]
        if r < self.strategy[0]:
            return 'R'
        elif r < self.strategy[1]:
            return 'P'
        else:
            return 'S'

    def makeYourMove (self):
        # collect some info about my opponent
        self.processHistory( )

        
        '''
        If we've played at least one tournament entirely,
        then let's use our "adaptive" strategy to make our move.
        '''
        if len(self.tournament.get_rrt_histories()) > 0:
            if self.oppfreqR > self.oppfreqP and self.oppfreqR > self.oppfreqS:
                return 'P'
            elif self.oppfreqP > self.oppfreqR and self.oppfreqP > self.oppfreqS:
                return 'S'
            elif self.oppfreqS > self.oppfreqR and self.oppfreqS > self.oppfreqP:
                return 'R'
            else:
                return self.makePureRandomMove()
        else:
            '''
            Otherwise, we're in our first tournament and we don't have enough
            information to use our adaptive strategy.  Let's just play
            equal probability throws.
            '''
            return self.makePureRandomMove()            

    def processHistory( self ):
        # as a test, get all opps  past moves
        # these are terriuble var names
        # reprocessing all the data each move is silly
        allpastHist = self.tournament.get_rrt_histories()
        
        if len(allpastHist) == 0:
            return
        curhist = self.tournament.get_engagement_history()
        totrecs = 0
        self.allrecs = []
        for r in allpastHist.keys():
            h = allpastHist[r]   # h is list of ga,me records
            totrecs += len( h )
            alist = [rec for rec in h if rec.aNameId == self.oppId ]
            self.allrecs = self.allrecs + alist

        numallrecs = len(self.allrecs)

        # count opps moves
        numR = 0
        numP = 0
        numS = 0
        for rec in self.allrecs :  
            if rec.aMove == 'R':
                numR  += 1
            elif rec.aMove == 'P':
                numP += 1
            else:
                numS += 1
                
        if numallrecs > 0: 
           self.oppfreqR = float(numR) / numallrecs
           self.oppfreqP = float(numP) / numallrecs
           self.oppfreqS = float(numS) / numallrecs
        else:
           self.oppfreqR = 0.0
           self.oppfreqP = 0.0
           self.oppfreqS = 0.0
           
