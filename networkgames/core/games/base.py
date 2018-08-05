from collections import namedtuple as nt
from importlib import import_module
from networkgames.core.util import _filehandling
# from networkx.classes.graph import Graph
import sys



class Games(object):
    """
    A general class to hold all base attributes for combinatorial games.
    """
    #TODO: Add baseclass attributes to be used for all games.

    __slots__ = ['name', 'log', 'player_info', 'sim_info', 'exp_info', '_number_of_players', '_base_player',
                 'output_loc']

    def __init__(self,
                 name='default_game',
                 number_of_players=2,
                 player_list=[['default_player_0', 'default_strategy', []],
                              ['default_player_1', 'default_strategy', []]],
                 sim_info_list = [import_module('networkx.classes.graph').Graph(), [], []]):
        """

        :type graph_info_list: object
        """


        self.name = name
        self.log = print
        self._number_of_players = number_of_players

        self.player_info \
            = nt("Players", ["player_%s" % player_number for player_number in range(self._number_of_players)])

        _base_player = nt("Player", ['name', 'strategy', 'moves'])

        self.player_info = self.player_info(*[_base_player(*p) for p in player_list])

        _sim_info = nt("Sim_Info", ['test_graph', 'sim_range', 'sim_runs'])
        self.sim_info = nt("Sim_Info", ['test_graph', 'sim_range', 'sim_runs'])
        self.sim_info = self.sim_info(*sim_info_list)

        class obj(object): pass

        self.exp_info = obj

        self.output_loc = _filehandling.create_output_locs()
        # self.exp_info.start_time = time.now()