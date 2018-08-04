import os
from networkgames.data import results

def create_output_locs(start_time, data_path=os.path.dirname(results.__file__)):

    for f_path in ["%s/%s/" % (data_path, start_time),
                   "%s/%s/vertexData/" % (data_path, start_time),
                   "%s/%s/graphs" % (data_path, start_time)]:
        if not os.path.isdir(f_path):
            os.makedirs(f_path)
    return
