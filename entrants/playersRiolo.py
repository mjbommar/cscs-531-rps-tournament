# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>


# Import standard libraries
import random

from edu.umich.cscs.rps.agents import Player




class  PlayerR( Player ):
    def __init__( self ):
        # Set name and number, then call parent constructor.
        name = "riolo"
        number = "3"
        super(PlayerR, self).__init__(name, number)

        #super ( PlayerR, self ).__init__( name, idnumber )
        #Player.__init__( self, name, idnumber )
        self.strategy = [ 0.333, 0.667 ]

    def makeYourMove (self):
        r = random.random()    # uniform( 0.0, 1.0 ]
        if r < self.strategy[0]:
            return 'R'
        elif r < self.strategy[1]:
            return 'P'
        else:
            return 'S'

# <codecell>


class  PlayerR1( Player ):
    '''

    '''
    def __init__( self ):
        # Set name and number, then call parent constructor.
        name = "riolo"
        number = "0"
        super(PlayerR1, self).__init__(name, number)

        #super ( PlayerR, self ).__init__( name, idnumber )
        #Player.__init__( self, name, idnumber )
        self.strategy = [ 0.05, 0.10 ]

    def makeYourMove (self):
        r = random.random()    # uniform( 0.0, 1.0 ]
        if r < self.strategy[0]:
            return 'R'
        elif r < self.strategy[1]:
            return 'P'
        else:
            return 'S'



class  PlayerR2( Player ):
    def __init__( self ):
        # Set name and number, then call parent constructor.
        name = "riolo"
        number = "2"
        super(PlayerR2, self).__init__(name, number)
        self.strategy = [ 0.2, 0.50 ]
        print "player rr2 ini:"

    def makeYourMove (self):
        r = random.random()    # uniform( 0.0, 1.0 ]
        if r < self.strategy[0]:
            return 'R'
        elif r < self.strategy[1]:
            return 'P'
        else:
            return 'S'


class  PlayerR3( Player ):
    def __init__( self ):
        # Set name and number, then call parent constructor.
        name = "riolo"
        number = "3"
        super(PlayerR3, self).__init__(name,number)
        # set default and current strat
        self.defaultstrategy = [ 0.2, 0.50 ]
        self.strategy = [ 0.2, 0.50 ]
        # to keep track of when a new bout starts, i see when opp changes
        self.curOppNameId = ''
        self.prevOppNameId = ''
        self.engagementsThisBout = 0
        self.totalEngagementsPlayed = 0
        self.boutsThisRRT = 0
        self.numOthers  = 0
        self.numRRTPlayed = 0
        print "player rr3 ini:"

    def makeYourMove (self):
        r = random.random()    # uniform( 0.0, 1.0 ]
        if r < self.strategy[0]:
            move = 'R'
        elif r < self.strategy[1]:
            move = 'P'
        else:
            move = 'S'
        print "move=" + move
        return move


    def yourOpponentsId(self, lastname_id):
        '''
        Handler for being informed of opponent's identity.
           incement counts at start of event
           numOthers is number of other players
           oppsThisRRT is number  of opp agents played in curRRT
           numRRTPlayed is number of RRTs completed
        '''
        print "---------------------------\nyourOppId is ..." + lastname_id
        if self.totalEngagementsPlayed == 0:   # first eengage,bout.rrt!
            self.numOthers = len(self.tournament.player_pool) - 1
            print "First engagement of 1st  bout of first rrt; numOthers={0}".format(self.numOthers)
            self.totalEngagementsPlayed = 1
            self.oppsThisRRT = 1
            self.numRRTPlayed += 1
            self.engagementsThisBout = 1
            self.curOppNameId = lastname_id

        elif self.oppsThisRRT == self.numOthers:
                # played everyonr once,  so startong new rrt
            print "played all {0} others in rrt {1}. start new rrt...".format(\
                    self.numOthers, self.numRRTPlayed  )
            self.oppsThisRRT = 1
            self.numRRTPlayed += 1
            self.engagementsThisBout = 1
            self.totalEngagementsPlayed += 1
            self.prevOppNameId = self.curOppNameId
            self.curOppNameId = lastname_id

        elif lastname_id != self.curOppNameId :
            # new opp, new bout,
            self.prevOppNameId = self.curOppNameId
            self.curOppNameId = lastname_id
            self.engagementsThisBout = 1
            self.oppsThisRRT += 1
            self.totalEngagementsPlayed += 1

        else:
            #  same last name  , so just another enngagenment
            self.engagementsThisBout += 1
            self.totalEngagementsPlayed += 1

        print "numRRTplayed={0}, numOppThisRRT={1}, opp={2}, engThisBout={3}, toteng={4}".format (\
    self.numRRTPlayed,self.oppsThisRRT,self.curOppNameId,self.engagementsThisBout,self.totalEngagementsPlayed)

    # ask the tournanent for the information so you can make a SINGLE list with
    # with  GameRecords for every engagement, in order. So you basicaly have
    # to combine one or more lists into one list.
    # The list you need to comibine are:
    #    engagement_history = []  - a list wit records from the currentRRT
    #    rrthistories = {}  - a dictionary whose keys are RRT numbers (0,1,...)
    # each of which maps to a list with all the GRs from the RRT with
    # that  number.  So to combine all those conceptually
    # 0. create fields  in Player.py (why there?) to keep track of
    #     the rrthistories, the current list of GRs AND one thqt
    #      will hold the full list uyou construct.
    # 1. get the dictionary of lists and loop over the RRT#s, the keys to the
    #    ditionary.   google eg python dictionary keys
    #  2. google python list combine append concatenate
    #  3. after you loop over the completed lists  of rrts,
    #     appenf the current rrt.
    # Note it will probably b easier to rebuilt the w hile list
    # from scratch each move then try to append the correct new moves.
    ##
    #
    #



##################################################################
# to test, run as follows
#     python entrants/playersRiolo.py


if __name__ == "__main__":
    p0 = PlayerR2()
    print(p0.identifyYourself())
    print(p0.makeYourMove())

    p0 = PlayerR3()
    print(p0.identifyYourself())
    print(p0.makeYourMove())



