"""
Tests for model.py.

Note that the unittest module predates PEP-8 guidelines, which
is why we have a bunch of names that don't comply with the
standard.
"""
import model
from model import Vec, Board, Tile
import unittest
import sys

class TestMove(unittest.TestCase):
    """The moves are 'right', 'left', 'up', 'down'.
    These methods are normally called from the 'keypress.py' module.
    """

    def test_move_all_right(self):
        """Simple slide with no merges"""
        board = model.Board()
        board.from_list([[2, 0, 0, 0],
                          [0, 2, 0, 0],
                          [0, 0, 2, 0],
                          [0, 0, 0, 2]])
        board.right();
        self.assertEqual(board.to_list(),
                          [[0, 0, 0, 2],
                           [0, 0, 0, 2],
                           [0, 0, 0, 2],
                           [0, 0, 0, 2]])

    def test_move_all_left(self):
        """Simple slide with no merges"""
        board = model.Board()
        board.from_list([[2, 0, 0, 0],
                          [0, 2, 0, 0],
                          [0, 0, 2, 0],
                          [0, 0, 0, 2]])
        board.left();
        self.assertEqual(board.to_list(),
                          [[2, 0, 0, 0],
                           [2, 0, 0, 0],
                           [2, 0, 0, 0],
                           [2, 0, 0, 0]])

    def test_move_all_up(self):
        """Simple slide with no merges"""
        board = model.Board()
        board.from_list([[2, 0, 0, 0],
                         [0, 2, 0, 0],
                         [0, 0, 2, 0],
                         [0, 0, 0, 2]])
        board.up();
        self.assertEqual(board.to_list(),
                          [[2, 2, 2, 2],
                           [0, 0, 0, 0],
                           [0, 0, 0, 0],
                           [0, 0, 0, 0]])

    def test_move_merge_right(self):
        board = model.Board()
        board.from_list([[2, 0, 2, 0],
                         [2, 2, 2, 0],
                         [2, 2, 0, 0],
                         [2, 2, 2, 2]])
        board.right()
        self.assertEqual(board.to_list(),
                          [[0, 0, 0, 4],
                           [0, 0, 2, 4],  # Must work from right to left
                           [0, 0, 0, 4],
                           [0, 0, 4, 4]]) # Tile stops sliding when it merges

    def test_move_merge_up(self):
        board = model.Board()
        board.from_list([[4, 0, 2, 2],
                         [2, 0, 2, 2],
                         [2, 2, 4, 0],
                         [2, 2, 2, 2]])
        board.up()
        expected = [[4, 4, 8, 4],
                    [4, 0, 2, 2],
                    [2, 0, 0, 0],
                    [0, 0, 0, 0]]
        actual = board.to_list()
        # board_diff(actual, expected)
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()
