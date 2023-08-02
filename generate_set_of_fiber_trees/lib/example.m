%--------------------------------------------------------------------------
%   Authors:
%     Sadegh Ghasr <sadeghghasr8817@aut.ac.ir>
%
%--------------------------------------------------------------------------
link_src =  [1  , 1  , 1  , 1  , 2  , 2  , 2  , 3  , 4  , 4  , 5  , 6  , 7  , 7  , 8];
% data1=xlsread('Reference_Network_TID_RegionalA.xlsx');
% link_src = data1(:, 1)';
% link_dst = data1(:, 2)';
% links = [(1, 2, 100), (1, 6, 200)
link_dst =  [2  , 5  , 6  , 8  , 3  , 4  , 6  , 4  , 5  , 6  , 7  , 8  , 8  , 9  , 9];
link_length=[100, 200, 300, 250, 140, 133, 465, 465, 432, 132, 234, 123, 186, 532, 123];
num_nodes = max(link_dst);
nodes = 1:num_nodes;
A = sparse(link_src, link_dst, ones(size(link_dst, 2), 1), num_nodes, num_nodes)';  % Adjacency matrix
fprintf('\nNumber of spanning trees: %d\n', getNumberSpanningTrees(A));
hub1 = 1;
hub2 = 2;
[idx, src, dst] = generateSpanningTrees(A, link_src, link_dst, nodes, hub1, hub2);

set_of_feasible_trees = [];
previous_tree_length = sum(link_length);
set_of_tree_length = [];
for i = 1:size(idx, 2)
    fprintf('\n%4i:', i);
    local_tree = [];
    for j = 1:size(idx, 1)
        fprintf('  (%i,%i)', src(idx(j, i)), dst(idx(j, i)));
        local_tree = [local_tree, [src(idx(j, i)); dst(idx(j, i))]];
    end
    set_of_feasible_trees = [set_of_feasible_trees local_tree];
%     num_of_2 = getNumberValueInMatrix(local_tree, 2);
%     for k = 1:num_nodes
       
%        if k == hub1
%            continue;
%        elseif k == hub2
%            continue;
%        end
%        number_of_this_node_in_local_tree = getNumberValueInMatrix(local_tree, k);
%        if number_of_this_node_in_local_tree == 1
%            break;
%        else
%            new_local_tree = local_tree;
%            length_of_this_tree = 0;
%            for local_idx = 1:size(new_local_tree, 2)
%                for index = 1:size(link_dst, 2)
%                    if new_local_tree(1, local_idx) == link_src(index)
%                       if new_local_tree(2, local_idx) == link_dst(index)
%                           length_of_this_tree = length_of_this_tree + link_length(index);
%                       end
%                    end
%                end
%            end
%            new_local_tree = [new_local_tree; (length_of_this_tree)*ones(size(new_local_tree, 2))];
           % sort length of trees in ascending order:
%            if length_of_this_tree < previous_tree_length
%                set_of_feasible_trees = [new_local_tree, set_of_feasible_trees];
%                set_of_tree_length = [length_of_this_tree, set_of_tree_length];
%                previous_tree_length = length_of_this_tree;
%            else
%                set_of_feasible_trees = [set_of_feasible_trees, new_local_tree];
%                set_of_tree_length = [set_of_tree_length, length_of_this_tree];
%            end
%             
%            set_of_tree_length = [set_of_tree_length, length_of_this_tree];
           
           % print feasible trees:
%        end
end
% end
xlswrite('trees.xlsx',set_of_feasible_trees);
fprintf('\n\n');
