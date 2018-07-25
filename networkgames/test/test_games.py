def base_games():
    from networkgames.core.games.base import Games
    mg = Games()
    print(mg)
    print(mg.players.player_0._fields, mg.players.player_1)

base_games()

def seepage_games():
    from networkx import generators as gg
    from networkgames.core.games.seepage import Seepage

    sg = Seepage(gg.caveman_graph(2, 2), 'test', 'test', 'test', 'test')

    print(sg.info)
    print(sg.info._fields)
    print(sg.info.test_graph)
    print(sg.players.player_0.name)
    print(sg.players.player_0.strategy)

# seepage_games()

#TODO: Add check functions for all test functions
