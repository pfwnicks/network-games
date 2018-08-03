def base_games():
    from networkgames.core.games.base import Games
    mg = Games()
    print(mg)
    print(mg.player_info)
    print(mg.sim_info)
    print(mg.sim_info.test_graph)
    print(mg.player_info.player_0.name)
    print(mg.player_info.player_0.strategy)

base_games()

def seepage_games():
    from networkx import generators as gg
    from networkgames.core.games.seepage import Seepage

    sg = Seepage(gg.caveman_graph(2, 2), 'test', 'test', 'test', 'test')

    print(sg.sim_info)
    #print(sg.info._fields)
    print(sg.sim_info.test_graph)
    print(sg.player_info.player_0.name)
    print(sg.player_info.player_0.strategy)
    return sg

seepage_games()

#TODO: Add check functions for all test functions
