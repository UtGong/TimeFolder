import math
from node.node import Node
"""
Provides functionality to calculate the Minimum Description Length (MDL).
This module is crucial for evaluating the complexity and quality of the model's representation.
"""

def mock_distance_condition(point1, point2):
    if isinstance(point1, Node):
        point1 = point1.data
        point2 = point2.data
    return abs(point2 - point1)   

# TODO: Implement MDL calculation.
def distance_calculator(frame_list, dist_condition=mock_distance_condition):
    """
    Calculates the distance for the given list of frames.

    Args:
        frame_list: A list of frames to be evaluated.
        mdl_condition: A function that returns the distance condition for a given frame.

    Returns:
        The distance value for the given list of frames.
    """
    # TODO: this if statement is only used for testing purposes, remove it when the distance_condition is implemented
    if len(frame_list) == 1:
        return 999
    return sum([dist_condition(frame_list[i], frame_list[i+1]) for i in range(len(frame_list) - 1)])