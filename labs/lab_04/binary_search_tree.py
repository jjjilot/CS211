'''CS 211 - Josh Jilot - Lab 4
Binary Search Trees'''

class Node:
    '''node'''
    def __init__(self, value: int):
        super().__init__()
        '''nodes have an integer as data'''
        self.node_data = value

    def sum_node_data(self):
        '''add this node and all below it'''
        raise NotImplementedError('each subclass must implement this method')

class Leaf(Node):
    '''nodes with no children'''
    def __init__(self, node_data: int):
        self.node_data = node_data

    def __str__(self):
        return f'{self.node_data}'

    def sum_node_data(self):
        return self.node_data

class Internal(Node):
    '''nodes with children'''
    def __init__(self, node_data: int, left: Node, right: Node):
        self.node_data = node_data
        self.left = left
        self.right = right

    def __str__(self):
        return f'< {self.node_data} , {self.left} , {self.right} >'

    def sum_node_data(self):
        return self.node_data + self.left.sum_node_data() + self.right.sum_node_data()

def main():
    l1 = Leaf(3)
    l2 = Leaf(6)
    l3 = Leaf(9)
    i = Internal(7, l2, l3)
    root = Internal(5, l1, i)
    print(root.sum_node_data())
    print(root)

if __name__ == '__main__':
    main()
