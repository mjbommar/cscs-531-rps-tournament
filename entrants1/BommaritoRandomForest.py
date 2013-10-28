'''
@date 20131028
@author: mjbommar
'''

import numpy.random
import sklearn.ensemble
import sklearn.metrics
from edu.umich.cscs.rps.agents import Player


class BommaritoRandomForest(Player):
    '''
    Sample player for Brown; always plays scissors. 
    '''

    # Variables
    current_opponent = None
    current_feature_row = None
    current_prediction = None
    random_forest_classifier = None
    
    
    def __init__(self):
        '''
        Constructor
        '''
        # Set name and number, then call parent constructor.
        name = "Bommarito"
        number = "1"
        super(BommaritoRandomForest, self).__init__(name, number)

    def yourOpponentsId(self, lastname_id):
        '''
        Handler for being informed of opponent's identity.
        '''
        self.current_opponent = lastname_id

    def make_random_move(self):
        '''
        Make an equal probability random move.
        '''
        r = numpy.random.random()
        if r < self.strategy[0]:
            return 'R'
        elif r < self.strategy[1]:
            return 'P'
        else:
            return 'S'
    
    def make_feature_record(self, engagement, engagement_history):
        '''
        Get a feature record from the individual engagement
        and the entire engagement history up to then.
        '''
        # Player pool ID list
        player_id_list = [player.identifyYourself() for player in self.tournament.player_pool]
        
        # Get some features
        engagement_count = 0
        score_total = 0.0
        move_counts = {'R': 0, 'P': 0, 'S': 0}
        score_counts = {'R': 0.0, 'P': 0.0, 'S': 0.}
        for game in engagement_history:
            if game.aNameId == self.current_opponent:
                engagement_count += 1
                score_total += game.aScore
                score_counts[game.aMove] += game.aScore
                move_counts[game.aMove] += 1

        # Normalize move counts and scores
        if move_counts['R'] > 0:
            score_counts['R'] /= float(move_counts['R'])
        if move_counts['P'] > 0:
            score_counts['P'] /= float(move_counts['P'])
        if move_counts['S'] > 0:
            score_counts['S'] /= float(move_counts['S'])
        if engagement_count > 0:
            move_counts['R'] /= float(engagement_count)
            move_counts['P'] /= float(engagement_count)
            move_counts['S'] /= float(engagement_count)

        # Determine ranks
        most_r = 0
        most_p = 0
        most_s = 0
        if move_counts['R'] > move_counts['P'] and move_counts['R'] > move_counts['S']:
            most_r = 1
        elif move_counts['P'] > move_counts['R'] and move_counts['P'] > move_counts['S']:
            most_p = 1
        elif move_counts['S'] > move_counts['R'] and move_counts['S'] > move_counts['P']:
            most_s = 1
                
        return [int(engagement_count/self.tournament.engagements_per_bout),
                engagement_count,
                score_total,
                score_counts['R'],
                score_counts['P'],
                score_counts['S'],
                move_counts['R'],
                move_counts['P'],
                move_counts['S'],
                player_id_list.index(engagement.bNameId)]
    
    def process_history(self):
        '''
        Process tournament history to update various data structures.
        '''
        # Get current and previous tournament engagements
        current_engagements = self.tournament.get_engagement_history()
        past_engagements = self.tournament.get_rrthistories()
        
        # Build the engagement list
        engagement_list = []
        opponent_engagement_list = []
        
        feature_list = []
        target_list = []
        
        # Handle past tournaments
        for tournament_key in sorted(past_engagements.keys()):
            for engagement in past_engagements[tournament_key]:
                if engagement.aNameId == self.current_opponent:
                    opponent_engagement_list.append(engagement)
                    feature_list.append(self.make_feature_record(engagement, engagement_list))
                    target_list.append(engagement.aMove)
                engagement_list.append(engagement)
        
        # Handle current tournament
        for engagement in current_engagements:
            if engagement.aNameId == self.current_opponent:
                opponent_engagement_list.append(engagement)
                feature_list.append(self.make_feature_record(engagement, engagement_list))
                target_list.append(engagement.aMove)
            engagement_list.append(engagement)
        
        
        if len(target_list) > 1 and len(set(target_list)) == 1:
            # Handle zero-variance players
            if target_list[0] == 'R':
                self.current_prediction = {'R': 1.0, 'P': 0.0, 'S': 0.0}
            elif target_list[0] == 'P':
                self.current_prediction = {'R': 0.0, 'P': 1.0, 'S': 0.0}
            else:
                self.current_prediction = {'R': 0.0, 'P': 0.0, 'S': 1.0}
        elif len(target_list) > 10:
            # Otherwise, if we have some variance and samples, run an RFC.
            self.random_forest_classifier = sklearn.ensemble.RandomForestClassifier(n_estimators=25)
            self.random_forest_classifier.fit(feature_list, target_list)
            #test_targets = random_forest_classifier.predict(feature_list)
            #print(sklearn.metrics.classification_report(target_list, test_targets))
        
            # Update last feature row and prediction
            self.current_feature_row = feature_list[-1]
            player_id_list = [player.identifyYourself() for player in self.tournament.player_pool]
            self.current_feature_row[-1] = player_id_list.index(self.identifyYourself())
            pred = list(self.random_forest_classifier.predict_proba(self.current_feature_row)[0])
            
            # Make sure we get all possible classes in the dictionary.
            self.current_prediction = {'R': 0.0, 'P': 0.0, 'S': 0.0}
            self.current_prediction.update(dict(zip(self.random_forest_classifier.classes_, pred)))

    def makeYourMove(self):
        '''
        Always play paper.
        '''
        # Update history and model
        self.process_history()
        
        threshold = 0.25
        
        # Make our move based on samples
        if self.current_prediction is not None:
            # Check for each case past the threshold
            if self.current_prediction['R'] - self.current_prediction['P'] >= threshold \
                and self.current_prediction['R'] - self.current_prediction['S'] >= threshold:
                return 'P'
            elif self.current_prediction['P'] - self.current_prediction['R'] >= threshold \
                and self.current_prediction['P'] - self.current_prediction['S'] >= threshold:
                return 'S'
            elif self.current_prediction['S'] - self.current_prediction['R'] >= threshold \
                and self.current_prediction['S'] - self.current_prediction['P'] >= threshold:
                return 'R'
            else:
                return self.make_random_move()
        else:
            return self.make_random_move()

if __name__ == "__main__":
    p0 = BrownScissors()
    print(p0.identifyYourself())
    print(p0.makeYourMove())
