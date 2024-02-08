# Assuming the import issue is resolved
from clustering.hcluster import hierarchical_clustering
from treecut_selection.treecut_selector import find_best_treecut
from node.node import print_tree_ascii

# Test data: A list of 2D points
test_data = [17, 37, 23, 20, 54, 14, 31, 27, 71, 3]

# Perform hierarchical clustering on the test data
tree_root = hierarchical_clustering(test_data)

print_tree_ascii(tree_root)
# Find the best tree cut from the clustered data
best_cut = find_best_treecut([tree_root])

print(f"Best tree cut: {best_cut}")
