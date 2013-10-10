'''
@date 20131005
@author: mjbommar
'''

# Import unittest
import unittest

# Import standard libraries
import random

# Import agents
from edu.umich.cscs.rps.agents import Player, Referee


class  PlayerR(Player):
    '''
    Subclass of Player that defines our specific strategy.
    '''

    def __init__(self, name, number):
        super(PlayerR, self).__init__(name, number)
        self.strategy = [0.333, 0.667]
        self.opponent_id = None

    def yourOpponentsId(self, opponent_id):
        self.opponent_id = opponent_id

    def makeYourMove(self):
        r = random.random()  # uniform( 0.0, 1.0 ]
        if r < self.strategy[0]:
            return 'R'
        elif r < self.strategy[1]:
            return 'P'
        else:
            return 'S'


class PlayerTest(unittest.TestCase):
    '''
    PlayerTest tests to make sure that our Player class
    is functioning as expected.
    '''

    player_name = "Riolo"
    player_number = 1

    def setUp(self):
        '''
        Set up some objects before we run tests.
        '''
        # Create our test player
        self.test_player = PlayerR(self.player_name, self.player_number)

    def tearDown(self):
        '''
        Clean up after our tests.
        '''
        pass

    def testName(self):
        '''
        Test that our name is working properly.
        '''
        # Set our expected name
        expected_name = "{0}_{1}".format(self.player_name, self.player_number)

        # Get our subclass name
        actual_name = self.test_player.identifyYourself()

        # Check that they match
        self.assertEqual(actual_name, expected_name)

    def testScore(self):
        '''
        Make sure our class reports the proper score initially.
        '''
        self.assertEqual(self.test_player.getTotalScore(), 0.0)


class RefereeTest(unittest.TestCase):
    '''
    RefereeTesttests to make sure that our Referee class
    is functioning as expected.
    '''

    # Initialize referee and player pool.
    referee = None
    player_pool = []

    def setUp(self):
        '''
        Set up some objects before we run tests.
        '''
        # Create our test players and seed the pool.
        player_a = PlayerR("Riolo", 1)
        player_b = PlayerR("Bommarito", 1)
        player_c = PlayerR("Alfaro", 1)
        self.player_pool.append(player_a)
        self.player_pool.append(player_b)
        self.player_pool.append(player_c)

        # Now create our referee
        self.referee = Referee(self.player_pool)

    def tearDown(self):
        '''
        Clean up after our tests.
        '''
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
