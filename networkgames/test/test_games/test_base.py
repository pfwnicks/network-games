
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

if __name__ == "__main__":
    test_base(True)
