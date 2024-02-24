"""
Module Description:
Responsible for selecting the best tree cut based on the distance calculator.
This module evaluates various cuts of a hierarchical tree to identify the most optimal structure,
minimizing the descriptive length and thus finding a balance between the complexity and goodness of fit.

Dependencies:
- distance_calculator.distance_calculator: Provides functionality to calculate the descriptive length of a node.
- node.node: Defines the Node class used to construct the hierarchical tree.
"""

from distance_calculator.distance_calculator import descriptive_length
from node.node import Node

def find_best_treecut(node):
    """
    Recursively find the best tree cut that minimizes the total descriptive length.
    
    Args:
    - node (Node): The current node being evaluated in the hierarchical tree.
    
    Returns:
    - list[Node]: A list of nodes representing the best cut of the tree.
    """
    
    # Base case: if the node is a leaf (has no children), return a list containing just this node.
    if not node.left and not node.right:
        return [node]
    
    # Recursive case: explore both left and right subtrees to find the best cut.
    combined_results = []
    if node.left:
        combined_results.extend(find_best_treecut(node.left))
    if node.right:
        combined_results.extend(find_best_treecut(node.right))

    # Calculate the descriptive length of the current node as a root of the subtree.
    root_length = descriptive_length(len(node.data), node)
    
    # Calculate the total descriptive length of the children nodes if this node is cut.
    children_length = sum(descriptive_length(len(child.data), child) for child in combined_results)

    # Compare the descriptive length of keeping the current node as a root vs cutting it.
    # Return the current node as a single element list if it's shorter, otherwise return the combined results of children.
    if root_length < children_length:
        return [node]  # More optimal to keep this node as a root.
    else:
        return combined_results  # More optimal to cut this node and use the children nodes.
