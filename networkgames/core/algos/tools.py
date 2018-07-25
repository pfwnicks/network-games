def usable_hood_selector(local_g, v_pol_local, v_pro_local, list_thr):
    usable_hood_data = []
    for v_thr in list_thr:
        hood = []
        hood_list = []
        hood.extend(local_g.neighbors(v_thr))
        for v_h in hood:
            if (v_pol_local.has_vertex(v_h) is True
                    or v_pro_local.has_vertex(v_h) is True):
                continue
            else:
                hood_list.append(v_h)
        length = len(hood_list)
        usable_hood_data.append((v_thr, length))
    return dict(usable_hood_data)


def max_deg_thr_vertex(local_g, v_pol_local, v_pro_local, list_thr):
    usable_hood_dict = {}
    usable_hood_data = []
    for v_thr in list_thr:
        hood = []
        hood_list = []
        hood.extend(local_g.neighbors(v_thr))
        for v_h in hood:
            if (v_pol_local.has_vertex(v_h) is True
                    or v_pro_local.has_vertex(v_h) is True):
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
        local_g, v_pol_local, v_pro_local, center_list):
    usable_hood_dict = Functions.usable_hood_selector(
        local_g, v_pol_local, v_pro_local)
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
        local_g, v_pol_local, v_pro_local, list_thr, v_s):
    # usable_hood_dict = Functions.usable_hood_selector(
    #         local_g, v_pol_local, v_pro_local)
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
        local_g, v_pol_local, v_pro_local,
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
            if v_pol_local.has_node(h) is True:
                continue

            # check to see if vertex is green
            if v_pro_local.has_node(h) is True:
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


def new_vertex_selector(local_g, v_pol_local, v_pro_local, list_thr, v_s,
                        agg=max):
    # --- Define local subgraph with v_pro removed
    local_vertices = []
    local_vertices = list(local_g.nodes())
    for v_pro in list(v_pro_local.nodes):
        local_vertices.remove(v_pro)

    deleted_subgraph = local_g.subgraph(local_vertices)
    search_subgraph_list = []
    subgraph_list = []
    subgraph_list.extend(list_thr)
    subgraph_list.extend(list(v_pol_local.nodes()))

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


def random_vertex_selector(local_g, v_pol_local, v_pro_local, list_thr):
    return choice(list(local_g.subgraph(list_thr).nodes()))