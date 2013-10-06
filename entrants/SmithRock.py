'''
@date 20131006
@author: mjbommar

'''

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

if __name__ == "__main__":
    p0 = SmithRock()
    print(p0.identifyYourself())
    print(p0.makeYourMove())