#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 10:11:52 2018

@author: imac
"""
import networkx as nx
from networkx import Graph
from networkx import generators
from networkx.algorithms.distance_measures import center
import os
import time
# import matplotlib as mp
from random import choice
import sys
import numpy as np
from line_profiler import LineProfiler

global green_algo
global sludge_algo

lp = LineProfiler()

'''


graph_list = [graphs.LjubljanaGraph(), graphs.WorldMap(), graphs.TutteGraph(),
graphs.WatkinsSnarkGraph(), graphs.WellsGraph(), graphs.WienerArayaGraph(),
 graphs.BidiakisCube(), graphs.Balaban10Cage(), graphs.Balaban11Cage()]

print 'Graph List Initialized'

for ladder_length in range(10):
    graph_list.append(graphs.LadderGraph(ladder_length+1))

print 'Ladders added'

for grid_width in range(7):
    for grid_length in range(7):
        graph_list.append(graphs.GridGraph([(grid_width+1)*2,
                                            (grid_length + 1)*2]))

print 'Grids added'

for grid_width in range(7):
    for grid_length in range(7):
        graph_list.append(graphs.ToroidalGrid2dGraph((grid_width+1)*2,
                                                     (grid_length +2)*2))

print 'Toroidals added'

for grid_width in range(3):
    for grid_length in range(4):
        graph_list.append(graphs.BalancedTree((grid_length+1), (grid_width+1)))

print 'Balanced Trees added'


#g = graphs.Balaban10Cage()
#g.graphplot().show()

# seepage_problem(g,
#                (range(order(g))),
#                1,
#                'max_weighted_vertex',
#                'random_vertex')


grn_strategy = ['new_vertex_selector', 'max_deg_thr_vertex',
                'max_weighted_vertex', 'closest_to_center_vertex']
sludge_strategy = ['random_vertex', 'max_deg_thr_vertex',
                   'max_weighted_vertex', 'closest_to_center_vertex']

print 'Starting Tests'

for reps in [5, 7, 10, 13, 17]:
    for grn in grn_strategy:
        for sludge in sludge_strategy:
                for g in graph_list:
                    experiment_data = seepage_problem(g,
                    (range(ceil(order(g)/2))), reps, grn, sludge)

'''


def perfect_k_tree(k_ary, height):
    t = Graph()
    print(t)

    t.add_node(0)
    # t.add_edges([(0, 1), (0, 2)])
    # t.plot()
    print(t)
    # cnt, k = var('cnt', 'k')
    cnt = 1

    parents = []
    new_parents = []
    new_parents.append(0)

    for h in range(height):
        parents.extend(new_parents)
        # print parents
        del (new_parents[:])
        # print new_parents
        for p in parents:
            # print p
            k = 0
            while k < k_ary:
                t.add_node(cnt)
                t.add_edge(p, cnt)
                new_parents.append(cnt)
                # print 'This is new_parents'+str(new_parents)
                cnt = cnt + 1
                k = k + 1
        parents = []
    return t


# g = perfect_k_tree(4, 3)
#


# print(g.nodes())

class Functions:

    def usable_hood_selector(local_g, V_pol_local, V_pro_local, list_thr):

        usable_hood_data = []
        for v_thr in list_thr:
            hood = []
            hood_list = []
            hood.extend(local_g.neighbors(v_thr))
            for v_h in hood:
                if (V_pol_local.has_vertex(v_h) is True
                        or V_pro_local.has_vertex(v_h) is True):
                    continue
                else:
                    hood_list.append(v_h)
            length = len(hood_list)
            usable_hood_data.append((v_thr, length))
        return dict(usable_hood_data)

    def max_deg_thr_vertex(local_g, V_pol_local, V_pro_local, list_thr):
        usable_hood_dict = {}
        usable_hood_data = []
        for v_thr in list_thr:
            hood = []
            hood_list = []
            hood.extend(local_g.neighbors(v_thr))
            for v_h in hood:
                if (V_pol_local.has_vertex(v_h) is True
                        or V_pro_local.has_vertex(v_h) is True):
                    continue
                else:
                    hood_list.append(v_h)
            length = len(hood_list)
            usable_hood_data.append((v_thr, length))
        usable_hood_dict.update(usable_hood_data)
        # return maximum usable degree of the threatened vertices
        return max(usable_hood_dict,
                   key=lambda key: usable_hood_dict[key])

    def closest_to_center_vertex(
            local_g, V_pol_local, V_pro_local, center_list):

        usable_hood_dict = Functions.usable_hood_selector(
            local_g, V_pol_local, V_pro_local)
        max_key = max(usable_hood_dict, key=lambda key: usable_hood_dict[key])
        max_usable_hood_list = []
        for v in usable_hood_dict:
            if usable_hood_dict[v] == usable_hood_dict[max_key]:
                max_usable_hood_list.append(v)
            else:
                continue
        local_subgraph = local_g.subgraph(max_usable_hood_list)
        minimum_distance_list = []
        minimum_distance_dict = {}
        for v in local_subgraph.vertices():
            v_distance_data = []
            for c in center_list:
                distance = local_g.distance(v, c)
                v_distance_data.append(distance)
            minimum_distance = min(v_distance_data)
            minimum_distance_list.append((v, minimum_distance))
        minimum_distance_dict.update(minimum_distance_list)
        minimum_distance_list = []
        minimum_distance_key = min(minimum_distance_dict,
                                   key=lambda key: minimum_distance_dict[key])
        for v in minimum_distance_dict:
            if minimum_distance_dict[v] \
                    == minimum_distance_dict[minimum_distance_key]:
                minimum_distance_list.append(v)
            else:
                continue
        minimum_distance_subgraph = local_g.subgraph(minimum_distance_list)
        return minimum_distance_subgraph.random_vertex()

    def furthest_from_source_vertex(
            local_g, V_pol_local, V_pro_local, list_thr, v_s):

        # usable_hood_dict = Functions.usable_hood_selector(
        #         local_g, V_pol_local, V_pro_local)
        # minimum_distance_list = []
        # minimum_distance_dict = {}
        max_distance_list = []
        max_distance_dict = {}
        # v_distance_data = []
        for v in list_thr:
            distance = local_g.distance(v, v_s)
            max_distance_list.append((v, distance))
        max_distance_dict.update(max_distance_list)
        max_distance_list = []
        max_distance_key = max(max_distance_dict,
                               key=lambda key: max_distance_dict[key])
        for v in max_distance_dict:
            if max_distance_dict[v] == max_distance_dict[max_distance_key]:
                max_distance_list.append(v)
            else:
                continue
        return local_g.subgraph(max_distance_list)

    def max_weighted_vertex(
            local_g, V_pol_local, V_pro_local,
            list_thr, center_list, v_s):

        max_hood_list = []
        usable_hood_data = []
        # minimum_distance_list = []
        usable_hood_dict = {}
        # minimum_distance_dict = {}

        for v in list_thr:
            hood = list(local_g.neighbors(v))
            hood_list = []
            for h in hood:

                # check to see if vertex is polluted
                if V_pol_local.has_node(h) is True:
                    continue

                # check to see if vertex is green
                if V_pro_local.has_node(h) is True:
                    continue
                else:
                    # add vertex to list usable neighbourhood
                    hood_list.append(h)

            # update vertex choices list
            usable_hood_data.append((v, len(hood_list)))
        usable_hood_dict.update(usable_hood_data)
        max_key = max(usable_hood_dict, key=lambda key: usable_hood_dict[key])
        for v in usable_hood_dict:
            if usable_hood_dict[v] == usable_hood_dict[max_key]:
                max_hood_list.append(v)
                continue
            else:
                continue

        # --- Find vertex furthest from source
        distance_list = []
        for v in max_hood_list:
            distance = nx.shortest_path_length(local_g, v, v_s)
            distance_list.append((v, distance))

        distance_dict = dict(distance_list)
        max_key = max(distance_dict, key=lambda key: distance_dict[key])

        max_distance_list = []
        for v in distance_dict:
            if distance_dict[v] == distance_dict[max_key]:
                max_distance_list.append(v)
            else:
                continue

        # --- Find vertex closest to center
        min_distance_list = []
        min_distance_dict = {}
        for v in max_distance_list:
            v_distance_data = []
            for c in center_list:
                distance = nx.shortest_path_length(local_g, v, c)
                v_distance_data.append(distance)
            min_distance = min(v_distance_data)
            min_distance_list.append((v, min_distance))
        min_distance_dict = dict(min_distance_list)
        min_distance_key = min(min_distance_dict,
                               key=lambda key: min_distance_dict[key])
        return min_distance_key

    def find_avg_distance(v_local, g_local):
        distance_list = []
        for v_g in g_local:
            if nx.algorithms.has_path(g_local, v_local, v_g):
                distance_list.append(
                    nx.algorithms.shortest_path_length(
                        g_local, v_local, v_g))
                continue
            else:
                continue
        return np.mean(distance_list)

    def find_infty_list(v_local, g_local):
        infinity_list = 0
        for nu in g_local.nodes():
            if not nx.algorithms.has_path(g_local, v_local, nu):
                infinity_list = infinity_list + 1
                continue
            else:
                continue
        return infinity_list

    def new_vertex_selector(local_g, V_pol_local, V_pro_local, list_thr, v_s,
                            agg=max):

        # --- Define local subgraph with v_pro removed
        local_vertices = []
        local_vertices = list(local_g.nodes())
        for v_pro in list(V_pro_local.nodes):
            local_vertices.remove(v_pro)

        deleted_subgraph = local_g.subgraph(local_vertices)
        search_subgraph_list = []
        subgraph_list = []
        subgraph_list.extend(list_thr)
        subgraph_list.extend(list(V_pol_local.nodes()))

        # --- Find subgraph for searching use
        for v_thr in list_thr:
            for v_nbr in deleted_subgraph.neighbors(v_thr):
                if v_nbr in subgraph_list:
                    continue
                else:
                    subgraph_list.append(v_nbr)
                    search_subgraph_list.append(v_nbr)

        for rng in range(2):
            search_list_temp = []
            search_list_temp.extend(search_subgraph_list)
            search_subgraph_list = []
            for v_srch in search_list_temp:
                for v_nbr in deleted_subgraph.neighbors(v_srch):
                    if v_nbr in subgraph_list:
                        continue
                    else:
                        subgraph_list.append(v_nbr)
                        search_subgraph_list.append(v_nbr)

        # find out which vertex will increase the average distance the most
        local_vertices_deleted = []
        local_vertices_deleted.extend(subgraph_list)
        local_vertices_deleted.append(v_s)

        # --- Find Articulation Points that are threatened
        art_pts = [x for x in list_thr
                   if x in nx.articulation_points(deleted_subgraph)]

        if len(art_pts) > 0:
            infinity_num_dict = {}
            # --- First pass through articulation points
            for art in art_pts:
                # print('2')
                # Remove articulation point from graph
                local_vertices_deleted.remove(art)
                deleted_subgraph = local_g.subgraph(local_vertices_deleted)

                # Find connected component containing source
                c_gen = deleted_subgraph.subgraph(
                    nx.components.node_connected_component(
                        deleted_subgraph, v_s))

                # Store number of isolated nodes
                infinity_num_dict.update({
                    art: (int(deleted_subgraph.order() - c_gen.order()),
                          c_gen)})

                # Return node to local working graph
                local_vertices_deleted.append(art)

            # Filter infinity_num_dict by maximum
            infinity_num_dict = {
                key: item for key, item in infinity_num_dict.items()
                if item[0] == max(l[0] for l in infinity_num_dict.values())}

            # Find value to return
            if len(infinity_num_dict) > 1:
                # If there are more than one *maximum* cuts, find avg paths
                avg_distance_dict = {
                    key: nx.average_shortest_path_length(item[1].copy())
                    for key, item in infinity_num_dict.items()}

                avg_distance_dict = {
                    key: item for key, item in avg_distance_dict.items()
                    if item == max(avg_distance_dict.values())
                }
                return choice(list(avg_distance_dict.keys()))
            else:
                return choice(list(infinity_num_dict.keys()))

        else:

            avg_distance_list = []
            for l in list_thr:
                local_vertices_deleted.remove(l)
                deleted_subgraph = local_g.subgraph(local_vertices_deleted)
                avg_distance_list.append(
                    (l,
                     nx.average_shortest_path_length(
                         deleted_subgraph.subgraph(
                             nx.components.node_connected_component(
                                 deleted_subgraph, v_s)).copy())))

                local_vertices_deleted.append(l)
            max_avg_distance = max(l[1] for l in avg_distance_list)
            max_avg_distance_dict = dict(filter(
                lambda l: l[1] == max_avg_distance, avg_distance_list))

            return choice(list(max_avg_distance_dict.keys()))

    def random_vertex_selector(local_g, V_pol_local, V_pro_local, list_thr):
        return choice(list(local_g.subgraph(list_thr).nodes()))

    def green_vertex_selector(local_g, V_pol_local, V_pro_local, green_algo,
                              list_thr, center_list, v_s):
        """
        Function to choose which algorithm to use
        """
        if green_algo == 'max_deg_thr_vertex':
            # use maximum degree decision algorithm
            return Functions.max_deg_thr_vertex(local_g,
                                                V_pol_local,
                                                V_pro_local)
        if green_algo == 'closest_to_center_vertex':
            return Functions.closest_to_center_vertex(local_g,
                                                      V_pol_local,
                                                      V_pro_local)
        if green_algo == 'max_weighted_vertex':
            return Functions.max_weighted_vertex(local_g,
                                                 V_pol_local,
                                                 V_pro_local,
                                                 list_thr,
                                                 center_list, v_s)
        if green_algo == 'random_vertex':
            return Functions.random_vertex_selector(local_g,
                                                    V_pol_local,
                                                    V_pro_local, list_thr)
        if green_algo == 'furthest_from_source':
            return Functions.furthest_from_source_vertex(local_g,
                                                         V_pol_local,
                                                         V_pro_local)
        if green_algo == 'new_vertex_selector':
            lp_nvsg = Functions.new_vertex_selector
            return lp_nvsg(local_g, V_pol_local, V_pro_local,
                           list_thr, v_s)
        else:
            # output for invalid algorithm
            print('Invalid green Move algorithm')
            return 0

    def sludge_vertex_selector(
            local_g, V_pol_local, V_pro_local, sludge_algo,
            list_thr, center_list, v_s):
        if sludge_algo == 'max_deg_thr_vertex':
            return Functions.max_deg_thr_vertex(
                local_g, V_pol_local, V_pro_local)
        if sludge_algo == 'closest_to_center_vertex':
            return Functions.closest_to_center_vertex(
                local_g, V_pol_local, V_pro_local,
                list_thr, center_list, v_s)

        if sludge_algo == 'max_weighted_vertex':
            lp_maxwv = lp(Functions.max_weighted_vertex)
            return lp_maxwv(
                local_g, V_pol_local, V_pro_local,
                list_thr, center_list, v_s)
        if sludge_algo == 'random_vertex':
            return Functions.random_vertex_selector(
                local_g, V_pol_local, V_pro_local,
                list_thr)
        if sludge_algo == 'furthest_from_source':
            return Functions.furthest_from_source_vertex(
                local_g, V_pol_local, V_pro_local)
        if sludge_algo == 'new_vertex_selector':
            return Functions.new_vertex_selector(
                local_g, V_pol_local, V_pro_local,
                list_thr, v_s)
        else:
            # output for invalid algorithm
            print('Invalid green Move algorithm')


def seepage_problem(g,
                    range_of_test,
                    repetition_per_vertex,
                    green_move_algorithm,
                    sludge_move_algorithm):
    # --- Preamble
    sludge_algo = sludge_move_algorithm
    green_algo = green_move_algorithm

    start_time = time.clock()
    experiment_start_time = time.ctime()
    lap_time = start_time

    # --- Experiment Initialization
    k = 0
    ell = 10
    num_of_exper = repetition_per_vertex  # Set number of experiments

    # --- create experiment folders
    graph_file_path \
        = './Data/SageGraphs/Sage-Output-Files/Test_Results/'
    file_path = ('./Data/SageGraphs/Sage-Output-Files/Test_Results/'
                 + str(start_time) + '/')
    vertex_file_path = ('./Data/SageGraphs/Sage-Output-Files/' +
                        'Test_Results/' + str(start_time) +
                        '/Vertex-Data/')
    graph_file_path = ('./Data/SageGraphs/Sage-Output-Files/' +
                       'Test_Results/' + str(start_time) + '/Graphs/')

    if not os.path.isdir(graph_file_path):
        os.makedirs(graph_file_path)
    if not os.path.isdir(file_path):
        os.makedirs(file_path)
    if not os.path.isdir(vertex_file_path):
        os.makedirs(vertex_file_path)
    if not os.path.isdir(graph_file_path):
        os.makedirs(graph_file_path)

    start_string = str(
        '\n Experiment started: ' + str(experiment_start_time) + '\n\n' +
        'Testing the seepage problem on the ' + str(g) + ' which has ' +
        str(g.order) + ' vertices.\n' + 'The vertices to be tested are: ' +
        str(range_of_test) + '\n' + 'These vertices will be tested ' +
        str(num_of_exper) + ' time(s) each with Green using the ' +
        str(green_move_algorithm) + ' strategy, and Sludge using the ' +
        str(sludge_move_algorithm) + ' strategy.')
    print(start_string)

    loc_string = (
            """
     The directory for this test can be found here: \n %s \n
     The overall contamination number data for this experiment is in: \n
     combined_experiment_data.txt\n
     The directory containing detailed information for the tests on each
     vertex is: \n %s \n
     The directory containing the graphs of the maximal seepage
     situation is: \n %s \n\n
            """
            % (file_path, vertex_file_path, graph_file_path))

    print(loc_string)

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

    # --- begin testing loop
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

        # --- begin test loop for source vertex
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

            # log test time
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
         The directory for this test can be found here: \n %s \n
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


"""
#
#def perfect_k_tree(k_ary, height):
#    t = Graph()
#    t.add_vertex(0)
#    #t.add_edges([(0, 1), (0, 2)])
#    #t.plot()
#
#    cnt, k = var('cnt', 'k')
#    cnt = 1
#
#    parents = []
#    new_parents = []
#    new_parents.append(0)
#
#    for h in range(height):
#        parents.extend(new_parents)
#        #print parents
#        del(new_parents[:])
#        #print new_parents
#        for p in parents:
#            #print p
#            k=0
#            while k < k_ary:
#                t.add_vertex(cnt)
#                t.add_edge(p, cnt)
#                new_parents.append(cnt)
#                #print 'This is new_parents'+str(new_parents)
#                cnt = cnt + 1
#                k = k+ 1
#        parents = []
#    return t
#


# with open('./Data/Networks/ca-HepTh.txt', 'r') as f:
#    content = f.readlines()
# print(content[4])
# g = Graph()
# content = content[4:]
# content = [x.strip() for x in content]
# content = [x.split('\t') for x in content]
## content = [x.split(' ') for x in content]
# graph_dict = {}
#
# for l in content:
#    # print(l)
#    try:
#        g.add_edge(l[0], l[1])
#    except Exception as e:
#        print(e)
#        print(l[1])
#        sys.exit()
#
# vsg = max(nx.connected_components(g), key=len)
# print(vsg)
# print([len(c) for c in sorted(nx.connected_components(g), key=len,
                                reverse=True)])
"""

# sg = g.subgraph(vsg)

if __name__ == '__main__':
    print('creating graph')
    # lp1 = lp(perfect_k_tree)
    # perfect_k_tree(4, 4)
    # lp.print_stats()
    # g = perfect_k_tree(7, 7)
    with open('./Data/Networks/ca-HepTh.txt', 'r') as f:
        content = f.readlines()
    print(content[4])
    g = Graph()
    content = content[4:]
    content = [x.strip() for x in content]
    content = [x.split('\t') for x in content]
    # content = [x.split(' ') for x in content]
    graph_dict = {}

    for l in content:
        # print(l)
        try:
            g.add_edge(l[0], l[1])
        except Exception as e:
            print(e)
            print(l[1])
            sys.exit()

    vsg = max(nx.connected_components(g), key=len)
    print(vsg)
    print([len(c) for c in sorted(nx.connected_components(g), key=len,
                                  reverse=True)])
    g = g.subgraph(max(nx.connected_components(g), key=len))

    # g = generators.random_graphs.random_powerlaw_tree(n=5000, gamma=3, tries=500000)
    #    print(lp1)
    nx.drawing.nx_pylab.draw_networkx(g)
    #
    #    print('running tests')
    lp2 = lp(seepage_problem)
    lp2(g, range(0, g.order()), 1, 'new_vertex_selector', 'new_vertex_selector')
    lp.print_stats()
