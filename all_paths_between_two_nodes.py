"""
Author : Mohammad Sadegh Ghasrizadeh Dezfouli
Project: Point to multipoint optical network communication
"""
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt


## functions definition
def get_length_of_link(src, dst, all_links):
    length = 0
    for lin in all_links:
        if lin[0] == src and lin[1] == dst:
            length = lin[2]
            break
    return length

def draw_trees(nodes, link_of_tree):
    '''
        This function draw input tree in the network
        INPUTS: nodes        = list of nodes
                link_of_tree = [(src1, dst1), (src2, dst2), ...]
                
    '''
    local_graph = nx.Graph()
    local_graph.add_nodes_from(nodes)
    local_graph.add_weighted_edges_from(link_of_tree)
    # random_pos = nx.random_layout(local_graph, seed=10)
    # pos = nx.spring_layout(local_graph, pos=random_pos)
    nx.draw(local_graph, with_labels = True)
    plt.show()

## network topology
list_of_nodes = [1, 2, 3, 4, 5]
list_of_links = [(1, 2), (1, 3), (1, 5), (2, 4), (2, 5), (3, 4), (3, 5)]

    # read topology from excel file

# src_list = [i[0] for i in pd.read_excel('Reference_Network_TID_RegionalA.xlsx', usecols='A').values.tolist()]
# dst_list = [i[0] for i in pd.read_excel('Reference_Network_TID_RegionalA.xlsx', usecols='B').values.tolist()]
# len_list = [i[0] for i in pd.read_excel('Reference_Network_TID_RegionalA.xlsx', usecols='C').values.tolist()]
# att_list = [i[0] for i in pd.read_excel('Reference_Network_TID_RegionalA.xlsx', usecols='D').values.tolist()]

src_list = [1, 1, 2, 2, 3, 4, 4, 5]
dst_list = [2, 3, 3, 5, 4, 5, 6, 6]
len_list = [1, 1, 1, 1, 1, 1, 1, 1]
att_list = [1, 1, 1, 1, 1, 1, 1, 1]

list_of_nodes = [*set(src_list + dst_list)]
list_of_links = [(src_list[i], dst_list[i], att_list[i]) for i in range(len(src_list))]
## generate graph
network = nx.Graph()

network.add_nodes_from(list_of_nodes)
network.add_weighted_edges_from(list_of_links, weight='weight')
nx.draw(network, with_labels = True)

## find all paths between two hubs
paths = nx.all_simple_paths(network, source=1, target=6)  # 8, 22 were previous hubs

number_of_all_paths = 0
number_of_all_feasible_trees = 0
set_of_all_feasible_trees = {}
for path in paths:
    local_nodes = path
    local_links = [(path[i], path[i + 1], get_length_of_link(path[i], path[i + 1], list_of_links)) for i in range(len(path) - 1)]
    local_graph = nx.Graph()
    local_graph.add_nodes_from(local_nodes)
    local_graph.add_weighted_edges_from(local_links)

    if len(path) == len(list_of_nodes):
        print(path)
        number_of_all_feasible_trees += 1
        set_of_all_feasible_trees[str(path)] = local_graph.size(weight='weight')
        
    number_of_all_paths += 1


trees_Sorted = dict(sorted(set_of_all_feasible_trees.items(), key=lambda item: item[1]))


# print(list(paths))


