'''
@date 20131005
@author: mjbommar
'''

# Load standard packages
import csv
import itertools
import operator
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
    rrt_histories = {}

    # Can you play your own agents?
    play_self = False

    # Path to result output
    results_path = 'results'

    def __init__(self, entrant_path='entrants', engagements_per_bout=21,
                 num_rrt=11, play_self=False, results_path='results'):
        '''
        Constructor
        '''
        # Set parameters
        self.engagements_per_bout = engagements_per_bout
        self.num_rrt = num_rrt
        self.play_self = play_self
        self.results_path = results_path

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

        # Check if we should remove self plays
        if not self.play_self:
            # Now remove pairs that are from the same player.
            bad_pairs = []

            for pair in all_pairs:
                player_a = pair[0].identifyYourself().split("_")[0].strip()
                player_b = pair[1].identifyYourself().split("_")[0].strip()
                if player_a == player_b:
                    bad_pairs.append(pair)

            all_pairs = [pair for pair in all_pairs if pair not in bad_pairs]

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
                except Exception:
                    pass

        # Return the player list
        return player_list

    def get_engagement_history(self):
        '''
        Return the engagement history.
        '''
        return self.engagement_history

    def get_rrt_histories(self):
        '''
        Return the histories.
        '''
        return self.rrt_histories

    def print_total_scores(self):
        '''
        Print total scores for all players.
        '''
        # for p in self.player_pool :
        for p in sorted(self.player_pool,
                        key=operator.attrgetter('total_score')):
            print(p)

    def run_bout(self, player_a, player_b):
        '''
        Run a single bout, which is one or more engagements.
        '''
        # Run the bout
        for i in range(self.engagements_per_bout):
            '''
            Run the engagement and record the outcome, a
            list of two GameRecord objects so each player can be a
            '''
            outcome = self.referee.run_engagement(player_a, player_b)
            self.engagement_history.extend(outcome)

    def run_tournament(self):
        '''
        Run a tournament by loading entrants from a given path and using
        the specified tournament strategy.
        numRRTs = number of round robin tournaments. each one gets an
          engagement history
        '''

        for rrt in range(self.num_rrt):
            print "rrt {0} of {1}".format(rrt, self.num_rrt)
            self.engagement_history = []

            # Get a round robin pair list.
            pair_sequence = self.get_round_robin_pairs()

            # Iterate over all pairs
            for player_a, player_b in pair_sequence:
                # Get players
                self.run_bout(player_a, player_b)

            # Round robin is over, store history key by RRT number
            self.rrt_histories[rrt] = self.engagement_history

        # Now output final history
        self.output_history()

    def output_history(self):
        '''
        Output the complete history of a tournament.
        '''
        rrt_history = self.get_rrt_histories()

        # Build row output
        history_data = []
        for tournament_key in sorted(rrt_history.keys()):
            engagement_counter = 0
            # Iterate over all tournmanets
            for engagement in rrt_history[tournament_key]:
                if engagement_counter % 2 == 0:
                    # Only output even rows
                    history_row = [tournament_key,
                                   engagement_counter / 2,
                                   engagement.aNameId,
                                   engagement.aMove,
                                   engagement.aScore,
                                   engagement.bNameId,
                                   engagement.bMove,
                                   engagement.bScore]

                    history_data.append(history_row)

                engagement_counter += 1

        # Write data out
        try:
            os.makedirs(self.results_path)
        except Exception:
            pass

        # Output results to a CSV file in the specified path.
        results_file = os.path.join(self.results_path, 'results.csv')
        csv_writer = csv.writer(open(results_file, 'w'))
        csv_writer.writerow(('RRT_Number', 'Engagement_Number',
                             'aNameId', 'aMove', 'aScore',
                             'bNameId', 'bMove', 'bScore'))
        csv_writer.writerows(history_data)

    def __repr__(self):
        '''
        String representation
        '''
        return "Tournament (player_pool={0}, match_count={1})"\
            .format(len(self.player_pool), len(self.engagement_history))


def output_help():
    '''
    TODO: Output help.
    '''


def process_cmd_args(args):
    '''
    Process command line arguments.
    '''
    # Set default arguments
    entrant_path = 'entrants/'
    engagements_per_bout = 21
    num_rrt = 5
    play_self = False

    # Iterate over args
    for arg in args:
        # Output help
        if arg == '-h' or arg == '--help':
            output_help()
            sys.exit(0)

        # Split about the equal sign, into name and value of the argument.
        tokens = arg.split('=')
        name = tokens[0]
        value = tokens[1]

        # Setup switch/case statement by argument
        if name == 'numRRTs' or name == 'N':
            num_rrt = int(value)
        elif name == 'ep' or name == 'entrant_path':
            entrant_path = value
        elif name == 'epb' or name == 'engagements_per_bout':
            engagements_per_bout = int(value)
        elif name == 'ps' or name == 'play_self':
            play_self = bool(value)
        else:
            print  " Unknown name in arg='%s'name='%s' value='%s'\n" % \
                (arg, name, value)
            output_help()

    # Return rows
    return [entrant_path, engagements_per_bout, num_rrt, play_self]


if __name__ == "__main__":
    # Process command line arguments
    entrant_path, engagements_per_bout, num_rrt, play_self = \
        process_cmd_args(sys.argv[1:])

    # Create tournament
    tournament = Tournament(entrant_path=entrant_path,
                         engagements_per_bout=engagements_per_bout,
                         num_rrt=num_rrt,
                         play_self=play_self)

    print("\nThe players:")
    tournament.print_total_scores()
    tournament.run_tournament()

    print("\nFinal scores:")
    tournament.print_total_scores()

    print("All done.")
