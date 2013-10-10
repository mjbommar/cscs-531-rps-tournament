'''
@date 20131009
@author: mjbommar

'''

from edu.umich.cscs.rps.agents import Player


class BrownScissors(Player):
    '''
    Sample player for Brown; always plays scissors. 
    '''

    def __init__(self):
        '''
        Constructor
        '''
        # Set name and number, then call parent constructor.
        name = "Brown"
        number = "1"
        super(BrownScissors, self).__init__(name, number)

    def makeYourMove(self):
        '''
        Always play paper.
        '''
        return 'S'

if __name__ == "__main__":
    p0 = BrownScissors()
    print(p0.identifyYourself())
    print(p0.makeYourMove())
