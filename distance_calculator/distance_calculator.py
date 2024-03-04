import math
from typing import Union, List
from node.node import Node
import numpy as np

def info_length(node_length: int) -> float:
    """
    Calculate the information length of a node.
    
    Args:
    - node_length (int): The length of the node.
    
    Returns:
    - float: The calculated information length.
    """
    return (node_length * math.log2(node_length + 1)) / 2

def loss_function(node: Union[List[float], Node], method, direction: str = 'rising') -> float:
    """
    Calculates a loss function for the node based on the probability of change.
    
    Args:
    - node (Union[List, Node]): The node data as a list or a Node object.
    - direction (str, optional): The direction of change ('rising' or 'falling'). Defaults to 'rising'.
    
    Returns:
    - float: The calculated loss.
    """
    data = node if isinstance(node, list) else node.data
    diff = data[0] - data[1]
    exponent = -diff if direction == 'rising' else diff
    pr_t = 1 / (1 + math.exp(exponent))
    if method == 'tanh':
        pr_t = (np.tanh(exponent) + 1) / 2
    elif method == 'softmax':
        logits = np.array([0, exponent])  # Assuming 0 represents no change, difference represents change
        probabilities = np.exp(logits) / np.sum(np.exp(logits))
        pr_t = probabilities[1]
    else:
        exponent = -diff if direction == 'rising' else diff
        pr_t = 1 / (1 + math.exp(exponent))
        
    if method == 'entropy':
        return pr_t * math.log2(pr_t) if pr_t > 0 else 0
    return -pr_t

def descriptive_length(node_length: int, node: Union[List[float], Node], method, direction: str = 'rising') -> float:

    return info_length(node_length) + loss_function(node, method, direction)
