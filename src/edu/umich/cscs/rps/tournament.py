'''
@date 20131005
@author: mjbommar
'''

# Load standard packages
import itertools
import os
import random
import sys

# Load our agents module
import edu.umich.cscs.rps.agents


class Tournament(object):
    '''
    The Tournament class defines the base tournament class.
    '''

    # Pool of possible players
    player_pool = []

    # History of engagements
    engagement_history = []

    def __init__(self, entrant_path='entrants', engagements_per_bout=21):
        '''
        Constructor
        '''
        # Set parameters
        self.engagements_per_bout = engagements_per_bout

        # Load players
        self.player_pool = self.load_entrants(entrant_path)

        # Create a referee
        self.referee = edu.umich.cscs.rps.agents.Referee()

    def set_pool(self, player_pool):
        '''
        Inform the referee of the player pool.
        '''
        # Set the player pool
        self.player_pool = player_pool

    def get_round_robin_pairs(self):
        '''
        Get a list of pairs corresponding to a round robin for
        the given player pool.
        '''

        # Get all pairs
        all_pairs = [item for item in \
                        itertools.combinations(self.player_pool, 2)]

        # Shuffle the list in place
        random.shuffle(all_pairs)

        # Now return the shuffled list
        return all_pairs

    def choose_pair(self):
        '''
        Return a pair of players from the current pool.
        '''
        # Sample two random players without replacement
        player_sample = random.sample(self.player_pool, 2)

        # Return them in a tuple
        return (player_sample[0], player_sample[1])

    def load_entrants(self, path):
        '''
        Load all tournament entrants from a given path.
        '''

        # Initialize player list
        player_list = []

        # Add path to the system path
        sys.path.append(path)

        # Load all the files in path
        for file_name in os.listdir(path):
            # Skip non-py files
            if not file_name.lower().endswith('.py'):
                continue

            # Get module name
            module_name = os.path.basename(file_name).replace(".py", "")

            # Import the module
            __import__(module_name, globals(), locals(), ['*'])

            # Now iterate over module contents.
            for object_name in dir(sys.modules[module_name]):
                object_value = getattr(sys.modules[module_name], object_name)
                try:
                    # Instantiate.
                    object_instance = object_value()

                    # If the variable matches the Player class type, include.
                    if isinstance(object_instance,
                                  edu.umich.cscs.rps.agents.Player):
                        # Set ourself as the tournament
                        object_instance.tournament = self
                        # Add to list
                        player_list.append(object_instance)
                except Exception, E:
                    pass

        # Return the player list
        return player_list

    def get_engagement_history(self):
        '''
        Return the engagement history.
        '''
        return self.engagement_history

    def run_tournament(self):
        '''
        Run a tournament by loading entrants from a given path and using
        the specified tournament strategy.
        '''

        # Get a round robin pair list.
        pair_sequence = self.get_round_robin_pairs()

        # Iterate over all pairs
        for pair in pair_sequence:
            # Get players
            player_a, player_b = pair

            # Run the bout
            for i in range(self.engagements_per_bout):
                # Run the engagement and record the outcome.
                outcome = self.referee.run_engagement(player_a, player_b)
                self.engagement_history.append(outcome)

    def __repr__(self):
        '''
        String representation
        '''
        return "Tournament (player_pool={0}, match_count={1})"\
            .format(len(self.player_pool), len(self.engagement_history))