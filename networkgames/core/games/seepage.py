from .base import Games
from time import clock, ctime

from networkgames.core.util import _filehandling, _datalogging
import networkx as nx
from networkx import Graph
# from networkx import generators
from networkx.algorithms.distance_measures import center

import time



# import matplotlib as mp
# from random import choice
# import sys
# import numpy as np
# from line_profiler import LineProfiler



class Seepage(Games):
    """
    A class to hold all specialized attributes for Seepage.
    """

    def __init__(self, test_graph, sim_range, sim_runs, green_algo, sludge_algo):
        """

        :param g: graph to be tested
        :param sim_range: list of vertices on which to run seepage sim
        :param sim_runs: number of times to run seepage sim per vertex
        :param green_algo: vertex selection algo for green
        :param sludge_algo: vertex selection algo for sludge
        """

        __slots__ = ['seepage_problem', '_output_loc']

        super(Seepage, self).__init__(
            name='Seepage',
            number_of_players=2,
            player_list=[['sludge', sludge_algo, []], ['green', green_algo, []]],
            sim_info_list=[test_graph, sim_range, sim_runs])

    def seepage_problem(self):
        start_time = clock()
        hum_start_time = ctime()
        lap_time = start_time

        # Experiment Initialization
        k = 0
        ell = 10
        num_of_exper = self.sim_info.sim_runs  # Set number of experiments

        # create experiment folders
        self.output_loc = _filehandling.create_output_loc(start_time)
        print(_datalogging.start_string(cur_game=self))
        self.log(_datalogging.loc_string)


    def next_steps(self):
        g = nx.convert_node_labels_to_integers(g)
        center_list = center(g)

        contam_num_data = []
        # graph_pos_data = []
        graph_data = []
        sludge_move_data = []
        green_move_data = []

        polluted_vertices_data = []
        green_vertices_data = []
        temp_contam_num_dict = {}
        extended_experiment_data = []
        vertex_time_data = []

        # begin testing loop
        for i in range_of_test:

            v_s_start_time = time.clock()
            j_time_data = []
            # print(i)
            v_s = i
            nx.classes.function.set_node_attributes(g,
                                                    {v_s, 'Source'}, 'label')

            # Clear Local Lists
            local_contam_num_data = []
            # local_graph_pos_data = []
            local_graph_data = []
            local_sludge_move_data = []
            local_green_move_data = []
            local_pol_vertices_data = []
            local_green_vertices_data = []

            # --- begin results loop for source vertex
            for j in range(num_of_exper):
                j_start_time = time.clock()
                k = k + 1

                # initiate move lists
                sludge_move_num = 0
                green_move_num = 0
                sludge_move_list = []
                green_move_list = []
                sludge_move_list.append((sludge_move_num, v_s))

                # initiate thr vertices
                list_thr = list(g.neighbors(v_s))
                V_thr = g.subgraph(g.neighbors(v_s))

                # initiate pol vertices
                V_pol = g.subgraph(v_s)
                list_pol = list(V_pol.nodes())

                # initiate Green Vertices
                V_pro = nx.generators.classic.empty_graph(0)
                list_green_vertices = []

                # --- Sludge Move

                sludge_move_num = sludge_move_num + 1
                v_i = Functions.sludge_vertex_selector(
                    g, V_pol, V_pro, sludge_algo,
                    list_thr, center_list, v_s)
                # print 'The vertex selected by Sludge is: ' + str(max_deg_thr)

                # pollute vertex v_i
                nx.classes.function.set_node_attributes(
                    g, {v_i: "POL"}, 'label')

                # print(list_thr)

                list_thr.remove(v_i)
                list_pol.append(v_i)  # update polluted list
                V_pol = g.subgraph(list_pol)  # update polluted vertices
                for v in g.neighbors(v_i):  # update threatened list
                    if (v in list_green_vertices
                            or v in list_pol
                            or v in list_thr):
                        continue
                    else:
                        list_thr.append(v)
                V_thr = g.subgraph(list_thr)  # update threatened subgraph
                sludge_move_list.append((sludge_move_num, v_i))

                # --- Green-Sludge Move Sequence
                while len(list_thr) > 0:

                    # Check to see if Green can move
                    if len(list_thr) == 0:
                        break

                    # --- Green's Move
                    else:
                        green_move_num = green_move_num + 1
                        v_i = Functions.green_vertex_selector(
                            g, V_pol, V_pro, green_algo,
                            list_thr, center_list, v_s)
                        # print 'The vertex selected by Green is: ' + str(v_i)
                        nx.classes.function.set_node_attributes(
                            g, {v_i: "GRN"}, 'label')
                        # g.set_vertex(v_i, "GRN") # protect vertex v_i
                        list_thr.remove(v_i)
                        V_thr = g.subgraph(list_thr)

                        # update data tracking
                        list_green_vertices.append(v_i)
                        V_pro = g.subgraph(list_green_vertices)
                        green_move_list.append((green_move_num, v_i))

                    # Check to see if Sludge can move
                    if len(list_thr) == 0:
                        break

                    # --- Sludge's Move
                    else:
                        sludge_move_num = sludge_move_num + 1
                        v_i = Functions.sludge_vertex_selector(
                            g, V_pol, V_pro, sludge_algo,
                            list_thr, center_list, v_s)
                        # print 'The vertex slected by Sludge is: ' + str(v_i)
                        nx.classes.function.set_node_attributes(
                            g, {v_i: "POL"}, 'label')
                        # g.set_vertex(v_i, "POL") #pollute vertex v_i
                        list_pol.append(v_i)
                        list_thr.remove(v_i)

                        # update polluted vertices subgraph
                        V_pol = g.subgraph(list_pol)

                        # update threatened list
                        for v in g.neighbors(v_i):
                            if (v in list_green_vertices
                                    or v in list_pol
                                    or v in list_thr):
                                continue
                            else:
                                list_thr.append(v)
                        # update threatened subgraph
                        V_thr = g.subgraph(list_thr)

                        # update Sludge's move tracker
                        sludge_move_list.append((sludge_move_num, v_i))

                # log results time
                j_end_time = time.clock()
                j_time = j_end_time - j_start_time
                j_time_data.append((j, j_time))

                # Update Local Contamination Number Data

                local_contam_num_data.append((j, V_pol.order()))
                # print('Contam num data(local):' + str(local_contam_num_data))
                # local_graph_pos_data.append((j, g.get_pos()))
                local_graph_data.append((j, nx.convert.to_dict_of_lists(g)))
                local_sludge_move_data.append((j, sludge_move_list))
                local_green_move_data.append((j, green_move_list))
                local_pol_vertices_data.append((j, V_pol))
                local_green_vertices_data.append((j, list_green_vertices))

            # log vertex time data
            v_s_end_time = time.clock()
            v_s_time = v_s_end_time - v_s_start_time
            vertex_time_data.append((v_s, v_s_time))

            # --- Map Local Data

            local_contam_num_dict = {}
            local_graph_pos_dict = {}
            local_graph_dict = {}
            local_sludge_move_dict = {}
            local_green_move_dict = {}
            local_pol_vertices_dict = {}
            local_green_vertices_dict = {}
            local_contam_num_dict.update(local_contam_num_data)
            # local_graph_pos_dict.update(local_graph_pos_data)
            local_graph_dict.update(local_graph_data)
            local_sludge_move_dict.update(local_sludge_move_data)
            local_green_move_dict.update(local_green_move_data)
            local_pol_vertices_dict.update(local_pol_vertices_data)
            local_green_vertices_dict.update(local_green_vertices_data)

            # --- Process Data and Transfer to Global Lists

            # print(local_contam_num_dict)
            local_max_key = max(local_contam_num_dict,
                                key=lambda key: local_contam_num_dict[key])
            contam_num_data.append((v_s, local_contam_num_dict[local_max_key]))
            # print(local_max_key)
            # graph_pos_data.append((v_s,local_graph_pos_dict[local_max_key]))
            graph_data.append(
                (v_s, local_graph_dict[local_max_key]))
            sludge_move_data.append(
                (v_s, local_sludge_move_dict[local_max_key]))
            green_move_data.append(
                (v_s, local_green_move_dict[local_max_key]))
            polluted_vertices_data.append(
                (v_s, local_pol_vertices_dict[local_max_key]))
            green_vertices_data.append(
                (v_s, local_green_vertices_dict[local_max_key]))

            # Store and Write Vertex Data

            extended_experiment_data.append((v_s, local_contam_num_dict))
            vertex_experiment_data = {
                'Log_time': str(time.ctime()),
                'abs_time': time.clock(),
                'vertex_time': v_s_time,
                'j_test_time': j_time_data,
                'local_max_key': local_max_key,
                'local_contam_num_dict': local_contam_num_dict,
                'local_graph_pos_dict': local_graph_pos_dict,
                'local_graph_dict': local_graph_dict,
                'local_sludge_move_dict': local_sludge_move_dict,
                'local_green_move_dict': local_green_move_dict,
                'local_pol_vertices_dict': local_pol_vertices_dict,
                'local_green_vertices_dict': local_green_vertices_dict}

            v_s_file_name = vertex_file_path + str(v_s)
            v_s_file_out = open(v_s_file_name, 'w')
            v_s_file_out.write(str(vertex_experiment_data))
            v_s_file_out.close()

            # Progress Outputs

            progress = k / (num_of_exper * len(range_of_test)) * 100
            if int(progress) > 0 and (int(progress) % ell == 0):
                # temporary data for updates
                temp_contam_num_dict.update(contam_num_data)
                # temporary max vertex
                v_temp_max = max(temp_contam_num_dict,
                                 key=(lambda key: temp_contam_num_dict[key]))
                current_time = time.clock()
                elapsed_time = current_time - lap_time
                lap_time = current_time
                print((
                        "Progress: %s percent. With %s/%s with an interval of %s"
                        "seconds, the vertex with the highest contamination "
                        "number is %s"
                        % (progress, k, str(num_of_exper * len(range_of_test)),
                           elapsed_time, v_temp_max)))
                ell = ell + 10

            # Clear Local Data (Optional)

            local_contam_num_dict = {}
            local_graph_pos_dict = {}
            local_graph_dict = {}
            local_sludge_move_dict = {}
            local_green_move_dict = {}
            local_pol_vertices_dict = {}
            local_green_vertices_dict = {}
            local_contam_num_data = []
            # local_graph_pos_data = []
            local_graph_data = []
            local_sludge_move_data = []
            local_green_move_data = []
            local_pol_vertices_data = []
            local_green_vertices_data = []
            # print 'Data Cleared'

            # --- Data for File

            # --- Prepare Experiment Data

            # Time Measurements
            experiment_end_time = time.ctime()
            end_time = time.clock()
            elapsed_time = (end_time) - (start_time)

            # data for storage
            experiment_data_list = []
            experiment_data_list.extend(contam_num_data)
            experiment_dict = {}
            experiment_dict.update(experiment_data_list)
            extended_experiment_dict = {}
            extended_experiment_dict.update(extended_experiment_data)
            combined_experiment_data = {
                'extended_experiment_dict': extended_experiment_dict,
                'experiment_dict': experiment_dict}

            # write data to file
            file_name = str(
                './Data/SageGraphs/Sage-Output-Files/Test_Results/' +
                str(start_time) + '/combined_experiment_data.txt')
            file_out = open(file_name, 'w')
            file_out.write(str(combined_experiment_data))
            file_out.close()

            # --- Find Contamination Number
            contam_num_dict = dict(contam_num_data)
            # graph_pos_dict = dict(graph_pos_data)
            graph_dict = dict(graph_data)
            sludge_move_dict = dict(sludge_move_data)
            green_move_dict = dict(green_move_data)
            # polluted_vertices_dict = dict(polluted_vertices_data)
            # green_vertices_dict = dict(green_vertices_data)
            contam_num_key = max(contam_num_dict,
                                 key=lambda key: contam_num_dict[key])

        # --- Experiment Results Output

        results_string = (
                """\n Results: \n\n' +
            'The vertex with the highest contamination number was %s
            with a contamination number of \n
    
            The mean contamination number for the vertices tested is %s \n"""
                % (contam_num_key, contam_num_dict[contam_num_key]))
        # print results_string

        # --- Test for graphing and evidence collection ###
        sludge_moves = sludge_move_dict[contam_num_key]
        green_moves = green_move_dict[contam_num_key]

        # polluted_vertices_subgraph = polluted_vertices_dict[contam_num_key];
        #  polluted_vertices_subgraph.remove_node(contam_num_key)
        # list_orange = polluted_vertices_subgraph.nodes()
        # list_green = green_vertices_dict[contam_num_key]

        # --- Print Graph for reference
        # GP = Graph(graph_dict[contam_num_key])
        # GP.set_pos(graph_pos_dict[contam_num_key]);

        # d = {'#00FF00':list_green,
        #      '#FF9900':list_orange, '#FF0000':[contam_num_key]};

        # GP.graphplot(vertex_colors=d).show(figsize=[10, 10])

        file_types = ['.eps', '.pdf', '.png', '.ps', '.sobj', '.svg']

        for i in file_types:
            # graph_plot_file_name = graph_file_path+'Maximal-Seepage-Game'+i
            graph_plot = Graph(graph_dict[contam_num_key])
            nx.drawing.nx_pylab.draw_networkx(graph_plot)
            # graph_plot.set_pos(graph_pos_dict[contam_num_key]);
            # graph_plot.graphplot(vertex_colors=d).plot(figsize \
            #   = [10, 10]).save(graph_plot_file_name)

        conclusion_string = (
                """\n Conclusion: \n\n
             These were Sludge's Moves: \n %s \n\n
             These were Green's moves: \n %s \n\n
             The directory for this results can be found here: \n %s \n
             The overall contamination number data for this experiment is in: \n
             combined_experiment_data.txt\n
             The directory containing detailed information for the tests on each
             vertex is: \n %s \n
             The directory containing the graphs of the maximal seepage
             situation is: \n %s \n\n
             The experiment ended at: %s after %s seconds of computation.\n\n
             Experiment conducted by: Peter Nicks"""
                % (sludge_moves, green_moves,
                   file_path, vertex_file_path, graph_file_path,
                   experiment_end_time, elapsed_time))

        experiment_log_file_name = file_path + 'experiment_log.txt'
        experiment_log_file = open(experiment_log_file_name, 'w')
        experiment_log_file.write(start_string + '\n' + results_string +
                                  '\n' + conclusion_string + '\n')
        experiment_log_file.close()

        return

