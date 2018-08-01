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

        __slots__ = []

        super(Seepage, self).__init__(
            name='Seepage',
            number_of_players=2,
            player_list=[['sludge', sludge_algo, []], ['green', green_algo, []]],
            graph_info_list=[test_graph, sim_range, sim_runs])



