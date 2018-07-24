from collections import namedtuple as nt

Player = nt("Player", ['name', 'strategy', 'moves', 'node_list'])

class Games(object):
    """
    A general class to hold all base attributes for combinatorial games.
    """
    #TODO: Add baseclass attributes to be used for all games.

    def __init__(self, number_of_players=2):

        for player_number in range(number_of_players):
            setattr(self, "player_%s" % player_number,
                    nt("Player", ['name', 'strategy', 'moves', 'node_list']))