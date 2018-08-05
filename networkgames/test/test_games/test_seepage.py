
def test_init(cout=False):
    from networkx import generators as gg
    from networkgames.core.games.seepage import Seepage

    seepage_game = \
        Seepage(gg.caveman_graph(2, 2), 'test_sim_range', 'test_sim_runs', 'test_green_algo', 'test_sludge_algo')
    
    if cout:
        print(seepage_game.name)
        print(seepage_game.sim_info)
        #print(seepage_game.info._fields)
        print(seepage_game.sim_info.test_graph)
        print(seepage_game.player_info.player_0.name)
        print(seepage_game.player_info.player_0.strategy)

    return seepage_game

def test_seepage_game():
    test_game = test_init()
    test_game.seepage_game()


if __name__ == "__main__":

    test_init(True)
    test_seepage_game()

#TODO: Add check functions for all test functions
