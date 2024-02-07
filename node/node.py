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