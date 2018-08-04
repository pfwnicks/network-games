def test_out_dir_creation():
    from networkgames.core.util._filehandling import create_output_locs
    from networkgames.data import results
    import shutil
    import os

    create_output_locs('123456')
    test_dir_loc = "%s/123456" % os.path.dirname(results.__file__)
    print(test_dir_loc)
    print(os.path.isdir(test_dir_loc))

test_out_dir_creation()
