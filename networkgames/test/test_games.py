def base_games():
    from networkgames.core.games.base import Games
    mg = Games()
    print(mg, mg.player_0, mg.player_1)

base_games()

def seepage_games():
    import networkx as nx
    from networkx import generators as gg
    from networkgames.core.games.seepage import Seepage

    sg = Seepage(gg.caveman_graph(2, 2), 'test', 'test', 'test', 'test')

    print(sg.info, sg.info._fields)

seepage_games()

#TODO: Add check functions for all test functions
