"""
Implements hierarchical clustering algorithms. 
This module is responsible for grouping data points into clusters based on their similarities.
"""
from ..mdl.mdl_calculator import mdl_calculator

# literate over first level of time frames and select the group that has the smalleset MDL
# TODO: What if there are two distances in the distList that are equally the smallest?
def compute_init_dist_list(data):
    distList = []
    for i in range(len(data) - 1):
        group = [data[i], data[i+1]]
        dist = mdl_calculator(group)
        distList.append(dist)
    return distList

def find_smallest_distance_group(data, distList):
    minDist = min(distList)
    index = distList.index(minDist)
    return index, data[index], data[index+1]

# find the smallest distance index using find_smallest_distance_group and then combine the two timeframe in data
def update_data(data, distList):
    """
    Updates the data and distance list by merging the closest groups.

    Args:
        data: A list of data groups.
        distList: A list of distances between adjacent groups.

    Returns:
        Tuple of updated data and distance list.
    """
    min_index, group1, group2 = find_smallest_distance_group(data, distList)

    # Merge the closest groups
    data[min_index] = group1 + group2

    # Remove the merged group
    if min_index + 1 < len(data):
        del data[min_index + 1]

    # Update distance list
    if min_index < len(distList):
        del distList[min_index]

    # Recalculate distances for the adjacent groups
    if min_index > 0:
        prevGroup = [data[min_index - 1], data[min_index]]
        distList[min_index - 1] = mdl_calculator(prevGroup)
    
    if min_index < len(data) - 1:
        nextGroup = [data[min_index], data[min_index + 1]]
        distList[min_index] = mdl_calculator(nextGroup)

    return data, distList

# take the initial data, use compute_init_dist_list to compute the distances between adjacent groups
# then use update_data to update the data and distance list until the distance list's length = 1
# form the hcluster process into a tree structure (level 0(highest) length=1, level 1 length = 2, etc) and return it as result

def hcluster(data):
    """
    Performs hierarchical clustering on the given data.
    
    Args:
        data: A list of data groups.
        
    Returns:
        A list of data groups in hierarchical order.
        
    """
    distList = compute_init_dist_list(data)
    treeList = [data]
    while len(distList) > 1:
        data, distList = update_data(data, distList)
        treeList.append(data)
    treeList.reverse()
    return treeList

    
    


        

