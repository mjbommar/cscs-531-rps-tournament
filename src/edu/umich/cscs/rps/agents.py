'''
@date 20131005
@author: mjbommar

This module defines the agents in our Rock-Paper-Scissors (RPS) world:
    * Player base class
    * Referee
'''

# Import standard libraries
import random


class Player(object):
    '''
    The Player class is a base class, meant to be extended by
    our individual competitors in the RPS tournament.

    The Player class defines a shared set of methods and variables
    that the Referee needs to assume are available to "run" the
    tournament.
    '''

    # Initialize the player's total score to 0.
    total_score = 0.0

    # Initialize the player's strategy variable to a string coding for rock.
    strategy = 'R'

    def __init__(self, name, number):
        '''
        Constructor, which initializes our player ID.
        '''
        # Set name_id
        self.name_id = "{0}_{1}".format(name, number)

    def  identifyYourself(self):
        '''
        Return our identity.
        '''
        return self.name_id

    def yourOpponentsId(self, lastname_id):
        '''
        Handler for being informed of opponent's identity.
        '''
        pass

    def makeYourMove(self):
        '''
        Default throw strategy.
        '''
        return self.strategy

    def yourScoreWas(self, score):
        '''
        Handler for being informed of the engagement outcome.
        '''
        self.total_score += score

    def getTotalScore(self):
        '''
        Return our total score.
        '''
        return self.total_score

    def __repr__(self):
        '''
        String representation for our Player.
        '''
        return "Player {0} (total_score={1})".format(self.identifyYourself(),
                                                     self.getTotalScore())


class Referee(object):
    '''
    The Referee class is the base class for our tournament arbiter.
    The Referee handles the mechanics of each game:
        1. Selecting a pair of players from a given pool
        2. Determining the identity of the players
        3. Informing each of the players of their opponent's identity
        4. Asking the players for their respective throws
        5. Determining the outcome/score of the engagement
        6. Informing the players of the outcome
    '''

    # Pool of possible players
    player_pool = []

    # History of engagements
    engagement_history = []

    def __init__(self, player_pool=[]):
        '''
        Constructor, optionally taking the initial player pool.
        '''
        self.player_pool = player_pool

    def set_pool(self, player_pool):
        '''
        Inform the referee of the player pool.
        '''
        # Set the player pool
        self.player_pool = player_pool

    def choose_pair(self):
        '''
        Return a pair of players from the current pool.
        '''
        # Sample two random players without replacement
        player_sample = random.sample(self.player_pool, 2)

        # Return them in a tuple
        return (player_sample[0], player_sample[1])

    def run_engagement(self, player_a, player_b):
        '''
        Run a single engagement by getting the throws from each player
        and determining the winner.
        '''
        # Ask the players who they are.
        name_a = player_a.identifyYourself()
        name_b = player_b.identifyYourself()

        # Tell them who their opponents are.
        player_a.yourOpponentsId(name_b)
        player_b.yourOpponentsId(name_a)

        #  Ask them for their throws.
        throw_a = player_a.makeYourMove()
        throw_b = player_b.makeYourMove()

        # Check that we got valid throws back.
        if throw_a not in ['R', 'P', 'S']:
            raise Exception("Invalid throw received from player A: {0}"
                            .format(throw_a))

        if throw_b not in ['R', 'P', 'S']:
            raise Exception("Invalid throw received from player B: {0}"
                            .format(throw_b))

        '''
        We are essentially evaluating the following payoff matrix
        (w.r.t. player A):

                        Player A
             |    R      |    P      |    S      |
        ------------------------------------------
        R    |    0.5    |    1.0    |    0.0    |
        ------------------------------------------
        P    |    0.0    |    0.5    |    1.0    |
        ------------------------------------------
        S    |    1.0    |    0.0    |    0.5    |
        ------------------------------------------
        '''

        # Set the scores up
        score_a = None

        payoff_matrix = {('R', 'P'): 0.0,
                         ('R', 'S'): 1.0,
                         ('P', 'R'): 1.0,
                         ('P', 'S'): 0.0,
                         ('S', 'R'): 0.0,
                         ('S', 'P'): 1.0}

        # Check the diagonal; all are a tie.
        if throw_a == throw_b:
            score_a = 0.5
        # Otherwise, use our payoff matrix
        else:
            score_a = payoff_matrix[(throw_a, throw_b)]

        # Now inform the players of their scores.
        player_a.yourScoreWas(score_a)
        player_b.yourScoreWas(1.0 - score_a)

        # And then record the game history.
        #TODO: Record game history using OOP data record.
