def test_base(cout=False):
    from networkgames.core.games.base import Games
    base_game = Games()
    
    if cout:
        print(base_game)
        print(base_game.player_info)
        print(base_game.sim_info)
        print(base_game.sim_info.test_graph)
        print(base_game.player_info.player_0.name)
        print(base_game.player_info.player_0.strategy)

    return base_game

def test_seepage(cout=False):
    from networkx import generators as gg
    from networkgames.core.games.seepage import Seepage

    seepage_game = \
        Seepage(gg.caveman_graph(2, 2), 'test_sim_range', 'test_sim_runs', 'test_green_algo', 'test_sludge_algo')
    
    if cout:
        print(seepage_game.sim_info)
        #print(seepage_game.info._fields)
        print(seepage_game.sim_info.test_graph)
        print(seepage_game.player_info.player_0.name)
        print(seepage_game.player_info.player_0.strategy)

    return seepage_game

if __name__ == "__main__":
    test_base(True)
    test_seepage(True)

#TODO: Add check functions for all test functions
