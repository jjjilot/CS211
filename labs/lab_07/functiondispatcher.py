'''Lab 07 - Josh Jilot
Functions as Arguments'''
import math
from typing import List, Callable

def total_sum(vals: list):
    tot = 0
    for val in vals:
        tot += val
    return tot

def apply(func, vals: list):
    func_out = []
    for val in vals:
        func_out.append(func(val))
    return func_out

def square(vals: list):
    return apply(lambda val:val**2, vals)

def magnitude(vector: list):
    sum_sq = 0
    for val in square(vector):
        sum_sq += val
    return math.sqrt(sum_sq)

dispatch_table = {1: total_sum, 2: square, 3: magnitude}

class FunctionDispatcher:

    def __init__(self, dispatch_table: dict):
        self.dispatch_table = dispatch_table

    def process_command(self, key: int, list1: List[int]):
        return dispatch_table[key](list1)
