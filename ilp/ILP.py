"""
Author: SadeghGhasr
E-mail: sadeghghasr8817@aut.ac.ir
"""

import cvxpy as cp
import numpy as np
from scipy.linalg import block_diag
import itertools
from scipy.sparse import block_diag as sparse_block_diag
from scipy.sparse import csc_matrix, hstack, vstack


# functions:
def find_subsets(s, n):
    all_sub_sets = []
    for i in range(n, len(s) + 1):
        for s_s in list(itertools.combinations(s, i)):
            all_sub_sets.append(s_s)
    return all_sub_sets


n_trees = 2
links = [(1, 2, 200), (1, 3, 130), (2, 3, 210), (2, 5, 120), (3, 4, 250), (4, 5, 75), (4, 6, 100), (5, 6, 140)]
nodes = [1, 2, 3, 4, 5, 6]
hubs = [1, 6]

x_f_l = cp.Variable((n_trees * len(links), 1), boolean=True)  # pos=True
x_f_f_prime_l = cp.Variable((n_trees * n_trees * len(links), 1), boolean=True)

## constraint 1:
b_for_c_1 = np.ones((1, len(links)))
for _ in range(n_trees - 1):
    b_for_c_1 = block_diag(b_for_c_1, np.ones((1, len(links))))

c_1 = b_for_c_1 @ x_f_l == len(nodes) - 1

## constraint 2:
b_b_for_c_2 = np.zeros((0, len(links)))
for n in nodes:
    block = np.zeros((1, len(links)))
    if n in hubs:
        b_b_for_c_2 = np.concatenate((b_b_for_c_2, block), axis=0)
    else:
        for l_idx in range(len(links)):
            if links[l_idx][0] == n or links[l_idx][1] == n:
                block[0][l_idx] = 1

        b_b_for_c_2 = np.concatenate((b_b_for_c_2, block), axis=0)

b_for_c_2 = b_b_for_c_2
for _ in range(n_trees - 1):
    b_for_c_2 = block_diag(b_for_c_2, b_b_for_c_2)

b_for_right_vector_for_c_2 = 2*np.ones((len(nodes), 1))
for i in range(len(nodes)):
    if nodes[i] in hubs:
        b_for_right_vector_for_c_2[i][0] = 0

right_vector_for_c_2 = b_for_right_vector_for_c_2
for _ in range(n_trees - 1):
    right_vector_for_c_2 = np.concatenate((right_vector_for_c_2, b_for_right_vector_for_c_2), axis=0)

c_2 = b_for_c_2@x_f_l == right_vector_for_c_2

## constraint 3:
all_subsets_with_at_least_3_node = find_subsets(nodes, 3)
basic_block = np.array([], dtype='?').reshape(0, len(links))
for ss in range(len(all_subsets_with_at_least_3_node)):
    sub_block = np.zeros((1, len(links)), dtype='?')
    for ll in range(len(links)):
        if (links[ll][0] in all_subsets_with_at_least_3_node[ss]) and (
                links[ll][1] in all_subsets_with_at_least_3_node[ss]):
            sub_block[0, ll] = 1
    if ss == 0:
        basic_block = csc_matrix(sub_block)
    else:
        basic_block = vstack((basic_block, csc_matrix(sub_block)))

A_3_left = csc_matrix(basic_block)
for _ in range(n_trees - 1):
    A_3_left = sparse_block_diag([A_3_left, csc_matrix(basic_block)])

A_3_right = csc_matrix(np.array([len(sss) for sss in all_subsets_with_at_least_3_node], dtype=int).reshape(
                                                                        len(all_subsets_with_at_least_3_node), 1))

for _ in range(n_trees - 1):
    A_3_right = vstack((
        A_3_right, csc_matrix(np.array([len(sss) for sss in all_subsets_with_at_least_3_node], dtype=int).reshape(
            len(all_subsets_with_at_least_3_node), 1))))

c_3 = A_3_left@x_f_l <= (A_3_right - csc_matrix(np.ones([A_3_right.shape[0], A_3_right.shape[1]])))

## constraint 4:
nu = np.zeros((1, len(links)))
for l_idx in range(len(links)):
    nu[0][l_idx] = (l_idx + 1)**3

b_left_4 = np.array([]).reshape(0, 0)
for t_idx in range(n_trees):
    b_b = np.zeros((0, len(links)))
    for t_prime_idx in range(n_trees):
        if t_prime_idx == t_idx:
            b_b = np.concatenate((b_b, np.zeros((1, len(links)))), axis=0)
        else:
            b_b = np.concatenate((b_b, nu), axis=0)

    b_left_4 = block_diag(b_left_4, b_b)


b_right_4 = np.array([]).reshape(0, len(links) * n_trees)
for t_idx in range(n_trees):
    b_b = np.zeros((0, 0))
    for t_prime_idx in range(n_trees):
        b_b = block_diag(b_b, nu)

    b_right_4 = np.concatenate((b_right_4, b_b), axis=0)

print(b_right_4)

c_4_full_right = np.array([]).reshape(0, 0)
for _ in range(n_trees**2):
    c_4_full_right = block_diag(c_4_full_right, nu.reshape(len(links)))

c_4 = b_left_4@x_f_l + b_right_4@x_f_l <= 2*(c_4_full_right@x_f_f_prime_l) - 1

## constraint 5:
b_for_c_5_left = np.array([]).reshape(0, len(links))
for _ in range(n_trees):
    b_for_c_5_left = np.concatenate((b_for_c_5_left, np.eye(len(links))), axis=0)

c_5_left = b_for_c_5_left
for _ in range(n_trees - 1):
    c_5_left = block_diag(c_5_left, b_for_c_5_left)

c_5_right = np.eye(n_trees * len(links))
for _ in range(n_trees - 1):
    c_5_right = np.concatenate((c_5_right, np.eye(n_trees * len(links))), axis=0)

c_5_1 = 0.5 * (c_5_left + c_5_right)@x_f_l <= x_f_f_prime_l
c_5_2 = x_f_f_prime_l <= (c_5_left + c_5_right)@x_f_l
prob = cp.Problem(cp.Minimize(1), [c_1, c_2, c_3, c_4, c_5_1, c_5_2])
prob.solve()
print(x_f_l.value)
