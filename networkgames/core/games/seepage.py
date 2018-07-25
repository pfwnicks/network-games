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

        super(Seepage, self).__init__()

        self.name = 'seepage'

        self.info = nt("Seepage_Info", ['test_graph', 'sim_range', 'sim_runs'])

        self.info = self.info(test_graph, sim_range, sim_runs)

        self.players.player_0 = self.players.player_0('sludge', sludge_algo, [], [])

        self.players.player_1 = self.players.player_1('green', green_algo, [], [])

