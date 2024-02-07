"""
Responsible for selecting the best tree cut using the distance calculator. 
This module evaluates different cuts of the tree to identify the most optimal structure.
"""

from ..distance_calculator.distance_calculator import distance_calculator

def find_best_treecut(node_list, best_cut={'score': float('inf'), 'nodes':[]}):
    if node_list is None:
        return best_cut
    
    curr_dist = distance_calculator(node_list)
    
    if curr_dist < best_cut['score']:
        best_cut = {'score': curr_dist, 'nodes': list(node_list)}
        
    for index, node in enumerate(node_list):
        if node.left is not None and node.right is not None:
            # Create a new list that includes the children instead of the current node
            testing_node_list = node_list[:index] + [node.left, node.right] + node_list[index+1:]
            best_cut = find_best_treecut(testing_node_list, best_cut)
            
    return best_cut

        