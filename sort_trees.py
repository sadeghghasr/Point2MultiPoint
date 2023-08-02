# -*- coding: utf-8 -*-
"""
Created on Thu May  4 12:33:58 2023

@author: SadeghGhasr

This script tries to extract feasible trees from set of all trees based on
only hub nodes can be degree 1.
Also, sorts the feasible trees in acsending order based on tree length.

"""


import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# functions definition:
def find_length_of_a_spanning_tree(sp_tree, all_links):
    '''
        This function returns length of a spanning tree.
        INPUTS: sp_tree=[(src1, dst1), (src2, dst2), ...]
                all_links = [(s_l1, d_l1, l_l1), (s_l2, d_l2, l_l2), ...]
        OUTPUT: length of the tree (integer)
    '''
    tree_length = 0
    for tre in sp_tree:
        for lin in all_links:
            if (lin[0] == tre[0] and lin[1] == tre[1]) or (lin[1] == tre[0] and lin[0] == tre[1]):
                tree_length += lin[2]
    
    return tree_length

def draw_trees(nodes, link_of_tree, idx_of_tree):
    '''
        This function draw input tree in the network
        INPUTS: nodes        = list of nodes
                link_of_tree = [(src1, dst1), (src2, dst2), ...]
                
    '''
    local_graph = nx.Graph()
    local_graph.add_nodes_from(nodes)
    local_graph.add_edges_from(link_of_tree)
    # random_pos = nx.random_layout(local_graph, seed=10)
    # pos = nx.spring_layout(local_graph, pos=random_pos)
    nx.draw(local_graph, with_labels = True)
    plt.show()
    
    


################################################################

# load trees:
CSVData = open("./generate_set_of_fiber_trees/lib/trees.csv")
all_trees = np.loadtxt(CSVData, delimiter=",")

# network topology:
links = [(1, 2, 100), (1, 5, 200), (1, 6, 300), (1, 8, 250), (2, 3, 140),
         (2, 4, 133), (2, 6, 465), (3, 4, 456), (4, 5, 432), (4, 6, 132),
         (5, 7, 234), (6, 8, 123), (7, 8, 186), (7, 9, 532), (8, 9, 123)] # node number 
                                                # should start from 1

# find number of nodes in network
number_of_nodes = max(max([i[0] for i in links]), max([j[1] for j in links]))

all_nodes = [i + 1 for i in range(number_of_nodes)]

# all of the tree are spaning tree; 
# so their number of links are number of nodes -1

number_of_links_in_a_tree = number_of_nodes - 1

# create set of sets where each set make up a tree.
link_distinct_tree = []
for i in range(0, all_trees.shape[1], number_of_links_in_a_tree):
    local_tree = []
    for j in range(number_of_links_in_a_tree):
        local_tree.append((int(all_trees[0, i + j]), int(all_trees[1, i + j])))
    link_distinct_tree.append(local_tree)
    
# determine hub nodes and extract feasible trees:
hub_node_1 = 1
hub_node_2 = 2

all_feasible_trees = []
for tr in link_distinct_tree:
    list_of_num_nodes = []
    for node in all_nodes:
        if node == hub_node_1 or node == hub_node_2:
            continue
        else:
            number_of_this_node = [i[0] for i in tr].count(node) + [i[1] for i in tr].count(node)
            list_of_num_nodes.append(number_of_this_node)
            
    if all(i >= 2 for i in list_of_num_nodes):
        all_feasible_trees.append(tr)
                
all_feasible_trees.sort(key=lambda x: find_length_of_a_spanning_tree(x, links))
for f_t in all_feasible_trees:
    draw_trees(all_nodes, f_t, 0)
tree_lengths = [find_length_of_a_spanning_tree(x, links) for x in 
                all_feasible_trees]

















