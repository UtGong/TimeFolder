"""
This module contains functions to filter valid time frames from the input data. 
It's used to preprocess data to ensure it meets the criteria for further processing.
"""

# todo: decide type of condition
def time_frame_filter(data, condition):
    """
    Filters and returns items from 'data' that meet the 'condition'.

    Args:
        data: An iterable dataset to be filtered.
        condition: A function that returns True for items to include.

    Returns:
        A list of items from 'data' that satisfy the 'condition'.
    """
    return [item for item in data if condition(item)]
    