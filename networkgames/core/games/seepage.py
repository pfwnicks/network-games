from .base import Games
from collections import namedtuple as nt

class Seepage(Games):
    """
    A class to hold all specialized attributes for Seepage.
    """

    __slots__ = ()

    def __init__(self, test_graph, sim_range, sim_runs, green_algo, sludge_algo):
        """

        :param g: graph to be tested
        :param sim_range: list of vertices on which to run seepage sim
        :param sim_runs: number of times to run seepage sim per vertex
        :param green_algo: vertex selection algo for green
        :param sludge_algo: vertex selection algo for sludge
        """

        self.info = nt("Seepage_Info", ['test_graph', 'sim_range', 'sim_runs',
                                        'green_algo', 'sludge_algo'])

        self.info._make([test_graph, sim_range, sim_runs, green_algo, sludge_algo])





