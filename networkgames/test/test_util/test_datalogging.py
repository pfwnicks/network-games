
def test_start_string():
    from networkgames.core.util._datalogging import start_string
    from networkgames.test.test_games.test_seepage import test_init

    print(start_string())
    print(start_string(test_init()))

if __name__  == "__main__":

    test_start_string()
