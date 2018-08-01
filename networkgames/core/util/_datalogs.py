output = print

def start_string(cur_game):

    player_cout = "Player Info: \n"

    for player in cur_game.players:


    str(
        '\n Experiment started: ' + str(cur_game.info.experiment_start_time) + '\n\n' +
        'Testing the seepage problem on the ' + str(g) + ' which has ' +
        str(cur_game.info.test_graph.order) + ' vertices.\n' + 'The vertices to be tested are: ' +
        str(cur_game.info.sim_range) + '\n' + 'These vertices will be tested ' +
        str(cur_game.info.sim_runs) + ' time(s) each with Green using the ' +
        str(cur_game.info.green_algo) + ' strategy, and Sludge using the ' +
        str(cur_game.info.sludge_algo) + ' strategy.')

    cout = """\n
    Experiment started: %s \n\n
    Testing the %s on the %s which has %s vertices. \n
    Each vertex in the range %s will be tested %s times. \n
    %s \n
    """ % (cur_game.info.experiment_start_time, cur_game.name, cur_game.info.test_graph.name,
           cur_game.info.test_graph.order, cur_game.info.sim_range, cur_game.info.sim_runs, player_cout)

    return cout
