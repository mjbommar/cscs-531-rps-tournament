'''
Created on Nov 3, 2013

@author: mjbommar
'''

# Standard imports
import os

# Tournament imports
import edu.umich.cscs.rps.tournament
from edu.umich.cscs.rps.tournament import Tournament


class Simulation(object):
    '''
    A simulation is one or more tournaments,
    combined with the result output logic.
    '''

    def __init__(self, num_samples=5, epb_values=[7], num_rtt_values=[21],
                 output_path='simulation'):
        '''
        Constructor
        '''
        # Set arguments
        self.epb_values = epb_values
        self.num_rtt_values = num_rtt_values
        self.output_path = output_path

        # Ensure the directory exists
        try:
            os.makedirs(self.output_path)
        except Exception, E:
            pass

        # Iterate over epb and num_rtt values
        for epb_value in self.epb_values:
            for num_rtt_value in self.num_rtt_values:
                for n in xrange(num_samples):
                    # Output path
                    results_path = "results/sample_{0}_epb_{1}_num_rtt_{2}"\
                        .format(n, epb_value, num_rtt_value)
                    print(results_path)
                    # Create a tournament
                    tournament = Tournament(engagements_per_bout=epb_value,
                                            numRRTs=num_rtt_value,
                                            play_self=True,
                                            results_path=results_path)
                    tournament.run_tournament()

if __name__ == "__main__":
    s = Simulation()