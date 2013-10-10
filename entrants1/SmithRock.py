'''
@date 20131006
@author: mjbommar

'''
import random

from edu.umich.cscs.rps.agents import Player


class SmithRock(Player):
    '''
    Sample player for Smith; always plays rock.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        # Set name and number, then call parent constructor.
        name = "Smith"
        number = "1"
        super(SmithRock, self).__init__(name, number)

    def makeYourMove(self):
        '''
        Always play rock.
        '''
        return 'R'



class  PlayerR2( Player ):
    def __init__( self ):
        # Set name and number, then call parent constructor.
        name = "riolo"
        number = "2"
        super(PlayerR2, self).__init__(name, number)

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





if __name__ == "__main__":
    p0 = SmithRock()
    print(p0.identifyYourself())
    print(p0.makeYourMove())
