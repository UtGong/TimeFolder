"""
Module for Hierarchical Clustering
This module is designed to organize data points into clusters based on their similarity.
"""

from distance_calculator.distance_calculator import descriptive_length
from node.node import Node


def build_time_series_pairs(data, date_column, value_column):
    """
    Constructs pairs of consecutive data points from the given data set, combining their dates and values.

    Parameters:
    - data: A list of dictionaries, each containing 'date' and 'value'.

    Returns:
    - A list of dictionaries, each representing a pair of consecutive data points with combined dates and values.
    """
    pairs = []
    for i in range(len(data) - 1):
        start_date = data.iloc[i][date_column]
        end_date = data.iloc[i + 1][date_column]
        values = [data.iloc[i][value_column], data.iloc[i + 1][value_column]]
        pairs.append({'date': f'{start_date} | {end_date}', 'value': values})
    return pairs


def calculate_initial_pairwise_distances(data):
    """
    Computes the initial distances between consecutive data point pairs using the Minimum Description Length (MDL).

    Parameters:
    - data: A list of data points.

    Returns:
    - A list of distances between consecutive data point pairs.
    """
    distances = []
    for i in range(len(data) - 1):
        pair = [data[i]['value'][0], data[i+1]
                ['value'][len(data[i+1]['value']) - 1]]
        pair_length = len(data[i]['value']) + len(data[i+1]['value'])
        distance = descriptive_length(pair_length, pair)
        distances.append(distance)
    return distances


def find_pair_with_minimum_distance(data, distances):
    """
    Identifies the pair of data points with the minimum distance.

    Parameters:
    - data: A list of data points.
    - distances: A list of distances between consecutive data point pairs.

    Returns:
    - The index of the pair with the minimum distance, and the data points forming that pair.
    """
    min_distance = min(distances)
    pair_index = distances.index(min_distance)
    return pair_index, data[pair_index], data[pair_index+1]


def merge_nearest_neighbors(data, distances):
    """
    Merges the closest pair of data points and updates the distances accordingly.

    Parameters:
    - data: A list of data points.
    - distances: A list of distances between consecutive data point pairs.

    Returns:
    - Updated data and distances after merging the closest pair of data points, along with the merge record.
    """
    index, group1, group2 = find_pair_with_minimum_distance(data, distances)
    new_group = {'date': group1['date'].split(' | ')[
        0] + ' | ' + group2['date'].split(' | ')[1], 'value': group1['value'] + group2['value'][1:]}
    new_value = group1['value'] + group2['value'][1:]
    new_date = group1['date'].split(
        ' | ')[0] + ' | ' + group2['date'].split(' | ')[1]
    merge_record = {'indexes': (index, index + 1), 'value': new_value,
                    'date': new_date, 'distance': distances[index]}
    
    # Perform the merge operation on the data
    data[index] = new_group
    del data[index + 1]

    # Update the pairwise distances
    del distances[index]

    if index > 0:
        pair_length = len(data[index - 1]['value']) + len(data[index]['value'])
        distances[index - 1] = descriptive_length(pair_length,
                                                  [data[index - 1]['value'][0], data[index]['value'][len(data[index]['value']) - 1]])
    if index < len(data) - 1:
        pair_length = len(data[index]['value']) + len(data[index + 1]['value'])
        distances[index] = descriptive_length(pair_length,
                                              [data[index]['value'][0], data[index + 1]['value'][len(data[index + 1]['value']) - 1]])

    return data, distances, merge_record


def perform_hierarchical_clustering(initial_data, date_column, value_column):
    """
    Executes the hierarchical clustering algorithm on the given data set.

    Parameters:
    - initial_data: A list of initial data points.

    Returns:
    - The root node of the constructed hierarchical clustering tree.
    """
    data = build_time_series_pairs(initial_data, date_column, value_column)
    distances = calculate_initial_pairwise_distances(data)
    merges = []  # Keeps a record of all merges performed
    nodes = [Node(index=i, data=d['value'], date=d['date'])
             for i, d in enumerate(data)]  # Initialize leaf nodes

    while len(data) > 1:
        data, distances, merge_record = merge_nearest_neighbors(
            data, distances)
        merges.append(merge_record)

    # Construct the hierarchical clustering tree from merge records
    for merge in merges:
        index1, index2 = merge['indexes']
        new_node = Node(index=None, data=merge['value'], date=merge['date'])
        new_node.set_children(left=nodes[index1], right=nodes[index2])
        # Replace one of the merged nodes with the new node
        nodes[index1] = new_node
        nodes.pop(index2)  # Remove the other node

    return nodes[0]  # The final node is the root of the tree
