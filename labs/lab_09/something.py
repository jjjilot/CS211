def flatten(a_list):
    """non-rec flatten for nested lists of depth 2"""
    flatlist = [flatten(element) for element in a_list]
    return flatlist

print(flatten([1, [2, 3], [4, 5]]))