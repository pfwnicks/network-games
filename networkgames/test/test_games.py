def base_games():
    from networkgames.core.games.base import Games
    mg = Games()
    print(mg)
    print(mg.player_info)

base_games()

def seepage_games():
    from networkx import generators as gg
    from networkgames.core.games.seepage import Seepage

    sg = Seepage(gg.caveman_graph(2, 2), 'test', 'test', 'test', 'test')

    print(sg.graph_info)
    #print(sg.info._fields)
    print(sg.graph_info.test_graph)
    print(sg.player_info.player_0.name)
    print(sg.player_info.player_0.strategy)

seepage_games()

#TODO: Add check functions for all test functions
