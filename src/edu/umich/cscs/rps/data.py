'''
Created on Oct 5, 2013

@author: mjbommar
'''


class GameRecord(object):
    '''
    This is the record of a single engagement
    To make lookup faster, store two records per engagement.
    '''

    def __init__(self, aNameId, aMove, aScore, bNameId, bMove, bScore):
        '''
        Constructor
        '''
        self.aNameId = aNameId  # player pointer
        self.aMove = aMove
        self.aScore = aScore
        self.bNameId = bNameId
        self.bMove = bMove
        self.bScore = bScore

    def __repr__(self):
        '''
        String representation of the object
        '''
        return "GameRecord(aNameId={0}, aMove={1}, aScore={2}, bNameId={3}, bMove={4}, outcome={4})".format(\
                     self.aNameId, self.aMove, self.aScore, self.bNameId, self.bMove, self.bScore)
