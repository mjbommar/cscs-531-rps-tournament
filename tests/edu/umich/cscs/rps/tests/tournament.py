'''
@date 20131006
@author: mjbommar
'''

# Import unittest
import unittest

# Import standard libraries
import random

# Import agents
from edu.umich.cscs.rps.agents import Player, Referee
from edu.umich.cscs.rps.tournament import load_entrants

class TournamentTest(unittest.TestCase):
    '''
    Test out a tournament.
    '''
    
    def setUp(self):
        # Setup the player pool
        self.player_pool = load_entrants('/users/mjbommar/workspace/cscs-531-rps-tournament/entrants')

        # Setup the referee
        # Create referee
        self.referee = Referee(self.player_pool)

    def tearDown(self):
        pass

    def testPairCoverage(self):
        '''
        Test that our pair selection is working properly.
        '''
        # Initialize coverage sampling
        players_seen = set()

        # Sample a few pairs.
        for i in range(100):
            # Sample
            players_chosen = self.referee.choose_pair()
            #print("Matchup between {0} and {1}".format(players_chosen[0],
            #                                           players_chosen[1]))

            # Update
            players_seen.update(players_chosen)

        # Make sure we got the full count.
        self.assertEqual(len(self.player_pool), len(players_seen))

    def testEngagement(self):
        '''
        Test that our engagement logic is working properly.
        '''
        # Number of engagements
        num_engagements = 10

        # Sample a few pairs.
        for i in range(num_engagements):
            # Sample players
            players_chosen = self.referee.choose_pair()

            # Run the engagement
            self.referee.run_engagement(players_chosen[0],
                                        players_chosen[1])

        # Test on names
        for player in self.player_pool:
            if player.identifyYourself() == "Jones_1":
                self.assertEqual(player.getTotalScore(), float(num_engagements))
            elif player.identifyYourself() == "Smith_1":
                self.assertEqual(player.getTotalScore(), 0.0)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()