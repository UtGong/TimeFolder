class Node:
    def __init__(self, index, left=None, right=None, distance=0.0, data=None, parent=None):
        self.index = index
        self.left = left
        self.right = right
        self.distance = distance
        self.data = data
        self.parent = parent

    def set_children(self, left=None, right=None):
        self.left = left
        self.right = right
        if left: left.parent = self
        if right: right.parent = self
        
def print_tree_ascii(node, prefix="", isLeft=True):
    if node is not None:
        # print("start printing tree")
        # Determine the line and branch characters based on the position of the node
        if node.left or node.right:  # Not the root node
            # print("if loop")
            line = "├── " if isLeft else "└── "
        else:  # Root node doesn't have a parent
            # print("else loop")
            line = ""
        # Print the current node's details
        print(f"{prefix}{line} Data: {node.data}")
        
        # Prepare the prefix for the children
        if node.parent:  # Adjust prefix based on parent and current node positions
            prefix += "│   " if isLeft else "    "
        # Recursive calls for the children, adjusting the prefix and indicating the position
        if node.left or node.right:
            if node.right:  # Right child exists
                print_tree_ascii(node.right, prefix, False)
            if node.left:  # Left child exists
                print_tree_ascii(node.left, prefix, True)

