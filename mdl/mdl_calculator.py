"""
Provides functionality to calculate the Minimum Description Length (MDL).
This module is crucial for evaluating the complexity and quality of the model's representation.
"""

def mdl_calculator(frame_list, mdl_condition):
    """
    Calculates the MDL for the given list of frames.

    Args:
        frame_list: A list of frames to be evaluated.
        mdl_condition: A function that returns the MDL condition for a given frame.

    Returns:
        The MDL value for the given list of frames.
    """
    return sum([mdl_condition(frame) for frame in frame_list])