from collections import namedtuple as nt
from networkx.classes.graph import Graph
import sys

Player = nt("Player", ['name', 'strategy', 'moves', 'node_list'])

class Games(object):
    """
    A general class to hold all base attributes for combinatorial games.
    """
    #TODO: Add baseclass attributes to be used for all games.

    __slots__ = ['name', 'player_info', 'graph_info', '_number_of_players', '_base_player']

    def __init__(self,
                 name='default',
                 number_of_players=1,
                 player_list=[['default_player', 'default_strategy', []]],
                 graph_info_list=[Graph(), [], []]):
        """

        :type graph_info_list: object
        """
        self.name = name
        self._number_of_players = number_of_players
        self._base_player = nt("Player", ['name', 'strategy', 'moves'])

        self.player_info \
            = nt("Players", ["player_%s" % player_number for player_number in range(self._number_of_players)])
        self.player_info = self.player_info(*[self._base_player(*p) for p in player_list])

        self.graph_info = nt("Graph_Info", ['test_graph', 'sim_range', 'sim_runs'])
        self.graph_info = self.graph_info(*graph_info_list)
