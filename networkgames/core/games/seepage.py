from .base import Games
from collections import namedtuple as nt


class Seepage(Games):
    """
    A class to hold all specialized attributes for Seepage.
    """

    def __init__(self, test_graph, sim_range, sim_runs, green_algo, sludge_algo):
        """

        :param g: graph to be tested
        :param sim_range: list of vertices on which to run seepage sim
        :param sim_runs: number of times to run seepage sim per vertex
        :param green_algo: vertex selection algo for green
        :param sludge_algo: vertex selection algo for sludge
        """
        player_list = [['sludge', sludge_algo], ['green', green_algo]]

        super(Seepage, self).__init__(number_of_players=2, player_list=player_list)

        self.name = 'seepage'

        self.info = nt("Seepage_Info", ['test_graph', 'sim_range', 'sim_runs'])

        self.info = self.info(test_graph, sim_range, sim_runs)

        print(self.players.player_0.name)

        # self.player_0 = self.players.player_0('sludge', sludge_algo, [], [])

        # self.player_1 = self.players.player_1('green', green_algo, [], [])

        self.player_0.moves = [0, 1, 2]

