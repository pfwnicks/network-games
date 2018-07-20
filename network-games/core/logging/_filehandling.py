import os


def create_output_directory(start_time):
    for f_path in ["./data/results/%s/" % start_time,
                   "./data/results/%s/vertexData/" % start_time,
                   "./data/results/%s/graphs" % start_time]:
        if not os.path.isdir(f_path):
            os.makedirs(f_path)
    return
