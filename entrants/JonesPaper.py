'''
@date 20131006
@author: mjbommar

'''

from edu.umich.cscs.rps.agents import Player


class JonesPaper(Player):
    '''
    Sample player for Jones; always plays paper. 
    '''

    def __init__(self):
        '''
        Constructor
        '''
        # Set name and number, then call parent constructor.
        name = "Smith"
        number = "1"
        super(JonesPaper, self).__init__(name, number)

    def makeYourMove(self):
        '''
        Always play rock.
        '''
        return 'R'

if __name__ == "__main__":
    p0 = JonesPaper()
    print(p0.identifyYourself())
    print(p0.makeYourMove())