import math
from typing import Union, List
from node.node import Node

def info_length(node_length: int) -> float:
    """
    Calculate the information length of a node.
    
    Args:
    - node_length (int): The length of the node.
    
    Returns:
    - float: The calculated information length.
    """
    return (node_length * math.log2(node_length + 1)) / 2

def probability_of_change(timeframe: List[float], direction: str = 'rising') -> float:
    """
    Calculates the probability of a change (either rising or falling) between two points in time.
    
    Args:
    - timeframe (List[float]): A list containing two points in time.
    - direction (str, optional): The direction of change ('rising' or 'falling'). Defaults to 'rising'.
    
    Returns:
    - float: The probability of the specified change occurring.
    """
    diff = timeframe[1] - timeframe[0]
    exponent = -diff if direction == 'rising' else diff
    return 1 / (1 + math.exp(exponent))

def info_entropy(node: Union[List[float], Node], direction: str = 'rising') -> float:
    """
    Calculate the information entropy of a node, measuring the uncertainty or disorder.
    
    Args:
    - node (Union[List, Node]): The node data as a list or a Node object.
    - direction (str, optional): The direction of change ('rising' or 'falling'). Defaults to 'rising'.
    
    Returns:
    - float: The calculated information entropy.
    """
    data = node if isinstance(node, list) else node.data
    pr_t = probability_of_change([data[0], data[-1]], direction)
    entropy = pr_t * math.log2(pr_t) if pr_t > 0 else 0
    return -entropy

def loss_function(node: Union[List[float], Node], direction: str = 'rising') -> float:
    """
    Calculates a loss function for the node based on the probability of change.
    
    Args:
    - node (Union[List, Node]): The node data as a list or a Node object.
    - direction (str, optional): The direction of change ('rising' or 'falling'). Defaults to 'rising'.
    
    Returns:
    - float: The calculated loss.
    """
    data = node if isinstance(node, list) else node.data
    pr_t = probability_of_change([data[0], data[-1]], direction)
    return -pr_t

def descriptive_length(node_length: int, node: Union[List[float], Node], direction: str = 'rising') -> float:
    """
    Compute the descriptive length of a node by summing its information length and loss function.
    This represents a balance between the structure's complexity and the data's diversity.
    
    Args:
    - node_length (int): The length of the node.
    - node (Union[List, Node]): The node data as a list or a Node object.
    - direction (str, optional): The direction of change ('rising' or 'falling'). Defaults to 'rising'.
    
    Returns:
    - float: The calculated descriptive length.
    """
    return info_length(node_length) + loss_function(node, direction)

# def descriptive_length(node_length: int, node: Union[List[float], Node], direction: str = 'rising') -> float:
#     """
#     Compute the descriptive length of a node by summing its information length and loss function.
#     This represents a balance between the structure's complexity and the data's diversity.
    
#     Args:
#     - node_length (int): The length of the node.
#     - node (Union[List, Node]): The node data as a list or a Node object.
#     - direction (str, optional): The direction of change ('rising' or 'falling'). Defaults to 'rising'.
    
#     Returns:
#     - float: The calculated descriptive length.
#     """
#     return info_length(node_length) + loss_function(node, direction)

def descriptive_length(node_length, node: Union[List, Node]) -> float:
    """
    Compute the descriptive length of a node by summing its information length and loss function.
    This represents a balance between the structure's complexity and the data's diversity.
    
    Args:
    - node_length (int): The length of the node.
    - node (Union[List, Node]): The node data as a list or a Node object.
    - direction (str, optional): The direction of change ('rising' or 'falling'). Defaults to 'rising'.
    
    Returns:
    - float: The calculated descriptive length.
    """
    return info_length(node_length) + info_entropy(node)
