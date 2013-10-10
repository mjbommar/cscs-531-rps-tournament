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
from edu.umich.cscs.rps.tournament import Tournament

class TournamentTest(unittest.TestCase):
    '''
    Test out a tournament.
    '''

    def setUp(self):
        # Setup the tournament
        self.tournament = Tournament('/users/mjbommar/workspace/cscs-531-rps-tournament/entrants')

    def tearDown(self):
        pass

    def testPairCoverage(self):
        '''
        Test that our pair selection is working properly.
        '''
        # Initialize coverage sampling
        players_seen = set()

        # Pass
        self.tournament.run_tournament()

        # Iterate over engagement history
        for match in self.tournament.get_engagement_history():
            players_seen.add(match['player_a'])
            players_seen.add(match['player_b'])

        # Make sure we got the full count.
        self.assertEqual(len(self.tournament.player_pool), len(players_seen))

    def testTournament(self):
        '''
        Test that our engagement logic is working properly.
        '''
        # Pass
        self.tournament.run_tournament()

        # All test players should have score equal to num_engagements.
        for player in self.tournament.player_pool:
            self.assertEqual(player.getTotalScore(),
                             float(self.tournament.engagements_per_bout))
        
        # Print match history
        print(self.tournament.get_engagement_history())
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()