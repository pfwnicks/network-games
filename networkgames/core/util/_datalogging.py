# from networkgames.core.games.base import Games
from importlib import import_module
from time import ctime
output = print

def start_string(cur_game=import_module('networkgames.core.games.base').Games()):



    print(cur_game)
    player_cout = "Player Names and Strategies: \n %s" % \
        ("".join(["""
            Name: %s :--: Strategy: %s \n""" % (player.name, player.strategy) for player in cur_game.player_info]))

    cout = """\n
    Experiment started: %s \n\n
    Testing the %s on the %s which has %s vertices. \n
    Each vertex in the range %s will be tested %s times. \n
    %s \n
    """ % (ctime(), cur_game.name, cur_game.sim_info.test_graph.name,
           cur_game.sim_info.test_graph.order, cur_game.sim_info.sim_range, cur_game.sim_info.sim_runs, player_cout)

    return cout

def loc_string(cur_game=import_module('networkgames.core.games.base').Games()):
    cout = """
     The directory for this results can be found here: \n %s \n
     The overall contamination number data for this experiment is in: \n
     combined_experiment_data.txt\n
     The directory containing detailed information for the tests on each
     vertex is: \n %s \n
     The directory containing the graphs of the maximal seepage
     situation is: \n %s \n\n
     """  % (file_path, vertex_file_path, graph_file_path)
