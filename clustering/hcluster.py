"""
Implements hierarchical clustering algorithms. 
This module is responsible for grouping data points into clusters based on their similarities.
"""
from ..distance_calculator.distance_calculator import distance_calculator
from ..node.node import Node

# # literate over first level of time frames and select the group that has the smalleset MDL
# # TODO: What if there are two distances in the distList that are equally the smallest?
def compute_initial_distances(data):
    distances = []
    for i in range(len(data) - 1):
        pair = [data[i], data[i+1]]
        distance = distance_calculator(pair)
        distances.append(distance)
    return distances

def identify_min_distance_pair(data, distances):
    min_distance = min(distances)
    # returns the first index of the minimum distance
    pair_index = distances.index(min_distance)
    return pair_index, data[pair_index], data[pair_index+1]

def merge_closest_groups(data, distances):
    """
    Finds and merges the two closest groups, updates data and distances.

    Args:
        data: List of data groups.
        distances: List of distances between adjacent groups.

    Returns:
        Updated data, distances, and merge record.
    """
    index, group1, group2 = identify_min_distance_pair(data, distances)
    new_group = group1 + group2
    merge_record = {'indexes': (index, index + 1), 'data': new_group, 'distance': distances[index]}
    
    # Perform the merge in data
    data[index] = new_group
    del data[index + 1]

    # Update distances
    del distances[index]
    if index > 0:
        distances[index - 1] = distance_calculator([data[index - 1], data[index]])
    if index < len(data) - 1:
        distances[index] = distance_calculator([data[index], data[index + 1]])

    return data, distances, merge_record

def hierarchical_clustering(data):
    """
    Performs hierarchical clustering on data, building a tree structure from recorded merges.

    Args:
        data: List of initial data groups.

    Returns:
        Root node of the hierarchical clustering tree.
    """
    distances = compute_initial_distances(data)
    merges = []  # Record of merges
    nodes = [Node(index=i, data=d) for i, d in enumerate(data)]  # Initial leaf nodes

    while len(distances) > 1:
        data, distances, merge_record = merge_closest_groups(data, distances)
        merges.append(merge_record)

    # Build the tree from recorded merges
    for merge in merges:
        index1, index2 = merge['indexes']
        new_node = Node(index=None, left=nodes[index1], right=nodes[index2], distance=merge['distance'], data=merge['data'])
        nodes[index1] = new_node  # Replace one of the merged nodes with the new node
        nodes.pop(index2)  # Remove the other node

    return nodes[0]  # The last node is the root of the tree
