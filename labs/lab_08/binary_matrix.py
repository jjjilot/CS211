'''Lab_08 - Josh Jilot
Quad Trees auxilary functions'''

from PIL import Image  # pylint: disable=import-error
import numpy as np  # pylint: disable=import-error
import matplotlib.pyplot as plt  # pylint: disable=import-error
import matplotlib  # pylint: disable=import-error
from statistics import mean
    
def read_bin_matrix(file_name):
    """Read a file text and convert its contents to a matrix"""
    matrix = []
    with open(file_name, "r") as text_file:
        while (line := text_file.readline()):
            row = list(map(int, line.split()))
            matrix.append(row)
    return matrix
        
def write_matrix(matrix, file_name):
    """
    Write a matrix to a text file. Using loops for illustration purposes.
    Exercise: eliminate the loops.
    """
    with open(file_name, "w") as text_file:
        for row in matrix:
            for el in row:
                text_file.write(str(el) + " ")
            text_file.write('\n')

def plot_bin_matrix(matrix):
    """
    Plotting a binary matrix using matplotlib. 
    The matrix must be converted to gray levels before plotting.
    """
    gray_matrix = [list(map(gray, x)) for x in matrix]
    plt.matshow(gray_matrix)
    plt.show()

def binarize_number(x):
    """convert a number from gray level [0 - 255] to binary {0, 1}"""
    return 0 if x < 128 else 1

def binarize_RGB(color):
    """convert a number from an RGB triplet to binary {0, 1}"""
    return binarize_number(sum(color)/3)

def gray(n):
    """convert a number from binary {0, 1} to gray level [0 - 255]"""
    return n*255

def binarize_matrix(matrix):
    """Combination of list comprehension and map to properly traverse a matrix"""
    bin_mat = [list(map(binarize_number, row)) for row in matrix]
    return bin_mat

def image_to_matrix(image_file):
    """numpy does all the work"""
    img = Image.open(image_file)
    numpydata = np.asarray(img)
    bin_data = binarize_matrix(numpydata)
    return bin_data

def flatten(a_list):
    """non-rec flatten for nested lists of depth 2"""
    flatlist=[element for sublist in a_list for element in sublist]
    return flatlist

def split_list(data, size):
    """splits a list on chunks of length size"""
    return [data[i:i+size] for i in range(0, len(data), size)]

def submatrix(matrix, r_loc, c_loc):
    """returns the submatrix of matrix delimited by rows in r_loc=(r1, r2) and columns in c_loc=(c1, c2)"""
    row_start, row_end = r_loc
    col_start, col_end = c_loc
    new_matrix = []
    for row in matrix[row_start:row_end]:
        new_row = []
        for elem in row[col_start:col_end]:
            new_row.append(elem)
        new_matrix.append(new_row)
    return new_matrix

def split_4(matrix):
    """
    Splits matrix in 4 submatrices, assumig matrix is square and its size is 
    a power of 2. 
    The result is resturned in order [nw, ne, se, sw] where the original matrix
    is in order
    [[nw ne]
     [sw se]].
    """
    n = len(matrix)
    new_n = n//2
    masks_1d = [(i*new_n, (i+1)*new_n) for i in range(2)] # These tuples define the ranges for indexing the rows and columns of the submatrices.
    masks = [(a, b) for a in masks_1d for b in masks_1d] # creates a list of tuples representing the ranges for indexing all four submatrices. 
    [nw, ne, sw, se] = [submatrix(matrix, m[0], m[1]) for m in masks] # The submatrix function is called with the current mask's row and column ranges, and the resulting submatrix is stored in the respective variable (nw, ne, sw, se).
    return [nw, ne, se, sw]

def same_bits(bin_mat):
    """Returns true if all elements of bin_mat contain the same value"""
    val = bin_mat[0][0]
    for row in bin_mat:
        for elem in row:
            if elem != val:
                return False
    return True

def matrix_mean(matrix):
    """Computes the mean of matrix's elements"""
    flat_mat = flatten(matrix)
    return mean(flat_mat)

def stitch_vertical(top, bottom):
    """stitches the matrices together, according to axis 0"""
    return top + bottom

def stitch_horizontal(left, right):
    """stitches the matrices together, according to axis 1"""
    new_matrix = []
    for i in range(len(left)):
        new_matrix.append(left[i] + right[i])
    return new_matrix

def stitch_matrices(nw, ne, se, sw):
    """Stitches the two matrices together"""
    top = stitch_horizontal(nw, ne)
    bottom = stitch_horizontal(sw, se)
    return stitch_vertical(top, bottom)

if __name__ == "__main__":
    # testing reading, converting, and writing files
    # image_file = 'images/fisherman_m.jpeg'
    # binary_file = 'images/fisherman.txt'
    # binary_file = 'images/square.txt'
    binary_file = 'images/test.txt'
    # matrix = image_to_matrix(image_file)
    # write_matrix(matrix, matrix_file)
    matrix = read_bin_matrix(binary_file)

    # plotting the matrix read from file
    plot_bin_matrix(matrix)
    print(matrix)

    # testing matrix split
    # m_4 = split_4(matrix)
    
    # fig, axs = plt.subplots(2, 2)
    # axs[0, 0].imshow(m_4[0])
    # axs[0, 1].imshow(m_4[1])
    # axs[1, 0].imshow(m_4[2])
    # axs[1, 1].imshow(m_4[3])
    # plt.show()

    # testing same_bits   
    # m = [[1, 1], [0, 1]]
    # all_same = all([all([(lambda x: x == first)(x) for x in row]) for row in m])
    # print(f"all_same = {all_same}")
    # print(same_bits(m))

    # m = [[1, 1], [0, 1]]
    # print(f"mean = {matrix_mean(m)}")

    # print(m_4)

    # [a, b, \
    #  d, c] = m_4    
    # left = stitch_vertical(a, c)
    # right = stitch_vertical(b, d)

    # print(f"l = {left}")
    # print(f"r = {right}")
