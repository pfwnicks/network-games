from . import tools as Functions


def green_vertex_selector(local_g, V_pol_local, V_pro_local, green_algo,
                          list_thr, center_list, v_s):
    """
    Function to choose which algorithm to use
    """
    if green_algo == 'max_deg_thr_vertex':
        # use maximum degree decision algorithm
        return Functions.max_deg_thr_vertex(local_g, V_pol_local, V_pro_local)
    if green_algo == 'closest_to_center_vertex':
        return Functions.closest_to_center_vertex(local_g, V_pol_local, V_pro_local)
    if green_algo == 'max_weighted_vertex':
        return Functions.max_weighted_vertex(local_g, V_pol_local, V_pro_local, list_thr, center_list, v_s)
    if green_algo == 'random_vertex':
        return Functions.random_vertex_selector(local_g, V_pol_local, V_pro_local, list_thr)
    if green_algo == 'furthest_from_source':
        return Functions.furthest_from_source_vertex(local_g, V_pol_local, V_pro_local)
    if green_algo == 'new_vertex_selector':
        lp_nvsg = Functions.new_vertex_selector
        return lp_nvsg(local_g, V_pol_local, V_pro_local, list_thr, v_s)
    else:
        # output for invalid algorithm
        print('Invalid green Move algorithm')
        return 0


def sludge_vertex_selector(local_g, V_pol_local, V_pro_local, sludge_algo, list_thr, center_list, v_s):
    if sludge_algo == 'max_deg_thr_vertex':
        return Functions.max_deg_thr_vertex(local_g, V_pol_local, V_pro_local)

    if sludge_algo == 'closest_to_center_vertex':
        return Functions.closest_to_center_vertex(local_g, V_pol_local, V_pro_local, list_thr, center_list, v_s)

    if sludge_algo == 'max_weighted_vertex':
        return Functions.max_weighted_vertex(local_g, V_pol_local, V_pro_local, list_thr, center_list, v_s)

    if sludge_algo == 'random_vertex':
        return Functions.random_vertex_selector(local_g, V_pol_local, V_pro_local, list_thr)

    if sludge_algo == 'furthest_from_source':
        return Functions.furthest_from_source_vertex(local_g, V_pol_local, V_pro_local)

    if sludge_algo == 'new_vertex_selector':
        return Functions.new_vertex_selector(local_g, V_pol_local, V_pro_local, list_thr, v_s)
    else:
        # output for invalid algorithm
        print('Invalid green Move algorithm')
