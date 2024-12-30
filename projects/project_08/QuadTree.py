"""
class designed to represent an image as a Quad Tree.

Josh Jilot
5/28/2023
"""
from binary_matrix import *
from math import inf as infinity

class QuadTree:

    def __init__(self) -> None:
        self.depth = 0
        self.mean = 0
        self.size = 0,0
        self.nw = None
        self.ne = None
        self.se = None
        self.sw = None

    def insert(self, bin_mat, depth = 0):
        self.size = len(bin_mat[0]), len(bin_mat)
        self.mean = matrix_mean(bin_mat)
        self.depth = depth
        if same_bits(bin_mat): return
        bin_mat_split = split_4(bin_mat)
        self.nw, self.ne, self.se, self.sw = QuadTree(), QuadTree(), QuadTree(), QuadTree()
        i = 0
        for elem in self.nw, self.ne, self.se, self.sw:
            elem.insert(bin_mat_split[i], depth + 1)
            i += 1

    def reconstruct_image(self, depth):
        if not self.nw or self.depth == depth:
            mat = [[]]*self.size[0]
            for i in range(self.size[1]):
                mat[i].append(self.mean)
            return mat
        else:
            cards = []
            for elem in self.nw, self.ne, self.se, self.sw:
                cards.append(elem.reconstruct_image(depth))
            return stitch_matrices(cards[0],cards[1],cards[2],cards[3])

    def __str__(self):
        if not self.nw:
            return f'{"+"*self.depth} (({self.depth}, {self.mean}, {self.size}))'
        return f'{"+"*self.depth} (({self.depth}, {self.mean}, {self.size}))' + \
                self.nw.__str__() + self.ne.__str__() + self.se.__str__() + self.sw.__str__()

if __name__ == "__main__":
    binary_file = 'images/fisherman.txt'
    matrix = read_bin_matrix(binary_file)
    q_t = QuadTree()
    q_t.insert(matrix)
    # print(q_t)

    depth = infinity # why infinity?
    rec_mat = q_t.reconstruct_image(depth) 
    plot_bin_matrix(rec_mat)
