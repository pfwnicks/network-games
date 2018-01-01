from collections import namedtuple as nt

Player = nt("Player", ['name', 'strategy', 'moves', 'node_list'])

class Games(object):
    """
    A general class to hold all base attributes for combinatorial games.
    """
    #TODO: Add baseclass attributes to be used for all games.

    __slots__ = ['name', '_number_of_players', 'player_info', '_base_player']

    def __init__(self, number_of_players=2, player_list=[]):

        self.name = 'base'
        self._number_of_players = number_of_players
        self._base_player = nt("Player", ['name', 'strategy'])
        self.player_info = nt("Players", ["player_%s" % player_number for player_number in range(self._number_of_players)])
        # print(self.players._fields)
        self.player_info = self.player_info(*list(map(lambda p: self._base_player(*p), player_list)))

        # print(self.players._fields)
        # print(self.players.player_0)

        # setattr([lambda for lambda in self.players], nt("Player", ['name', 'strategy', 'moves', 'node_list']) ) lambda in self.players)
        # map(lambda player: setattr(self.players.player, nt("Player", ['name', 'strategy', 'moves', 'node_list'])),
        #     self.players._fields)


        # for player_number in range(self._number_of_players):
        #     setattr(self.players, "player_%s" % player_number,
        #             nt("Player", ['name', 'strategy', 'moves', 'node_list']))

