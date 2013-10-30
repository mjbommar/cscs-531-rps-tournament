'''
@date 20131030
@author: mjbommar

This module defines basic report output for a tournament's results. 
'''

# Imports
import numpy
import pandas
import matplotlib.pyplot

class Report(object):
    '''
    Basic Report.
    '''

    # Initialize variables
    players = []
    total_score = {}
    cumulative_score = []
    move_counts = {'R': 0, 'P': 0, 'S': 0}
    cumulative_move_counts = []
    matchup_scores = {}


    def update_cumulative_score(self):
        '''
        Update cumulative score
        '''
        self.cumulative_score.append([self.total_score[player] for player in self.players])
        
    def update_cumulative_moves(self):
        '''
        Update cumulative moves
        '''
        self.cumulative_move_counts.append([self.move_counts[move] for move in ('R', 'P', 'S')])

    def load_players(self):
        '''
        Load the player information.
        '''
        # Get the unique player list
        self.players.extend(self.result_data['aNameId'].unique())
        self.players.extend(self.result_data['bNameId'].unique())
        self.players = sorted(list(set(self.players)))

        # Setup the total score
        for player in self.players:
            # Setup total score
            self.total_score[player] = 0.0
            
        # Setup matchup matrix
        #self.matchup_scores = [[0.0] * len(self.players)] * len(self.players)

        # Update cumulative score        
        self.update_cumulative_score()


    def update_score_matrix(self):
        '''
        Convert and update the scores to a matrix for pairwise outcome.
        '''
        self.score_matrix = []
        for i in xrange(len(self.players)):
            self.score_matrix.append([0.0] * len(self.players))
            player_i = self.players[i]
            for j in xrange(len(self.players)):
                player_j = self.players[j]
                if (player_i, player_j) in self.matchup_scores:
                    self.score_matrix[i][j] = self.matchup_scores[player_i, player_j]

    def load_data(self, file_name):
        # Read the result data
        self.result_data = pandas.DataFrame.from_csv(file_name, index_col=None)
        
        # Setup player data
        self.load_players()

        # Iterate by tournament
        for rrt_number, rrt_rows in self.result_data.groupby('RRT_Number'):
            # Iterate through engagements
            for engagement_number, engagement_row in rrt_rows.iterrows():
                # Increment scores
                self.total_score[engagement_row['aNameId']] += engagement_row['aScore']
                self.total_score[engagement_row['bNameId']] += engagement_row['bScore']
                
                # Increment move counts
                self.move_counts[engagement_row['aMove']] += 1
                self.move_counts[engagement_row['bMove']] += 1
                
                # Increment matchup tracking
                matchup_id_a = (engagement_row['aNameId'], engagement_row['bNameId'])
                matchup_id_b = (engagement_row['bNameId'], engagement_row['aNameId'])
                if matchup_id_a in self.matchup_scores:
                    self.matchup_scores[matchup_id_a] += engagement_row['aScore']
                    self.matchup_scores[matchup_id_b] += engagement_row['bScore']
                else:
                    self.matchup_scores[matchup_id_a] = engagement_row['aScore']
                    self.matchup_scores[matchup_id_b] = engagement_row['bScore']
                
            # Update cumulatives at end of each RRT
            self.update_cumulative_score()
            self.update_cumulative_moves()
            
        # Update score matrix
        self.update_score_matrix()                

    def __init__(self, file_name='results.csv'):
        '''
        Constructor
        '''
        # Load data
        self.load_data(file_name)
        
        # Get the score time series and write to CSV
        score_ts = pandas.DataFrame(self.cumulative_score, columns=self.players)
        score_ts.to_csv('score_time_series.csv')
        
        # Score matrix
        score_matrix = pandas.DataFrame(self.score_matrix, index=self.players, columns=self.players)
        score_matrix.to_csv('score_matrix.csv')
        
        # Plot the time series of scores
        f = matplotlib.pyplot.figure()
        for player in self.players:
            matplotlib.pyplot.plot(range(len(self.cumulative_score)), score_ts[player], '--', label=player)            
        matplotlib.pyplot.legend(loc='best', shadow=True)
        matplotlib.pyplot.savefig('score_ts.png')
        
        
if __name__ == "__main__":
    r = Report()