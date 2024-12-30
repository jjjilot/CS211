"""
The game state and logic (model component) of 512, 
a game based on 2048 with a few changes. 
This is the 'model' part of the model-view-controller
construction plan.  It must NOT depend on any
particular view component, but it produces event 
notifications to trigger view updates. 
"""

import random
from game_element import GameElement, GameEvent, EventKind
from typing import List, Tuple, Optional

# Configuration constants
GRID_SIZE = 4

class Vec():
    """A Vec is an (x,y) or (row, column) pair that
    represents distance along two orthogonal axes.
    Interpreted as a position, a Vec represents
    distance from (0,0).  Interpreted as movement,
    it represents distance from another position.
    Thus we can add two Vecs to get a Vec.
    """
    def __init__(self, x_dist, y_dist) -> None:
        self.x_dist = x_dist
        self.y_dist = y_dist

    def __add__(self, other: 'Vec') -> 'Vec':
        return Vec(self.x_dist + other.x_dist, self.y_dist + other.y_dist)

    def __eq__(self, other: 'Vec') -> bool:
        return self.x_dist == other.x_dist and self.y_dist == other.y_dist

class Tile(GameElement):
    """A slidy numbered thing."""

    def __init__(self, pos: Vec, value: int):
        super().__init__()
        self.row = pos.x_dist
        self.col = pos.y_dist
        self.value = value

    def __repr__(self):
        """Not like constructor --- more useful for debugging"""
        return f"Tile[{self.row},{self.col}]:{self.value}"

    def __str__(self):
        return str(self.value)

    def __eq__(self, other: "Tile"):
        return self.value == other.value

    def move_to(self, new_pos: Vec):
        self.row = new_pos.x_dist
        self.col = new_pos.y_dist
        self.notify_all(GameEvent(EventKind.tile_updated, self))

    def merge(self, other: "Tile"):
        # This tile incorporates the value of the other tile
        self.value = self.value + other.value
        self.notify_all(GameEvent(EventKind.tile_updated, self))
        # The other tile has been absorbed.  Resistance was futile.
        other.notify_all(GameEvent(EventKind.tile_removed, other))

class Board(GameElement):
    """The game grid.  Inherits 'add_listener' and 'notify_all'
    methods from game_element.GameElement so that the game
    can be displayed graphically.
    """

    def __init__(self, rows=GRID_SIZE, cols=GRID_SIZE):
        super().__init__()
        self.rows = rows
        self.cols = cols
        self.tiles = []
        for i in range(rows):
            row_tiles = []
            for i in range(cols):
                row_tiles.append(None)
            self.tiles.append(row_tiles)

    def has_empty(self) -> bool:
        """Is there at least one grid element without a tile?"""
        for row in self.tiles:
            for tile in row:
                if tile is None:
                    return True
        return False

    def _empty_positions(self) -> List[Vec]:
        """Return a list of positions of None values,
        i.e., unoccupied spaces.
        """
        empties = []
        for row_i, row in enumerate(self.tiles):
            for col_i, col in enumerate(row):
                if col is None:
                    empties.append(Vec(row_i, col_i))
        return empties

    def in_bounds(self, pos: Vec) -> bool:
        """Is position (pos.x, pos.y) a legal position on the board?"""
        return 0 <= pos.x_dist < len(self.tiles) and \
                0 <= pos.y_dist < len(self.tiles[0])

    def to_list(self) -> List[List[int]]:
        """Test scaffolding: represent each Tile by its
        integer value and empty positions as 0
        """
        result = [ ]
        for row in self.tiles:
            row_values = []
            for col in row:
                if col is None:
                    row_values.append(0)
                else:
                    row_values.append(col.value)
            result.append(row_values)
        return result

    def from_list(self, values: List[List[int]]):
        """Test scaffolding: set board tiles to the
        given values, where 0 represents an empty space."""
        for row_i, row in enumerate(values):
            for val_i, val in enumerate(row):
                if val == 0:
                    self.tiles[row_i][val_i] = None
                else:
                    self.tiles[row_i][val_i] = Tile(Vec(row_i, val_i), val)

    def place_tile(self, value=None):
        """Place a tile on a randomly chosen empty square."""
        empties = self._empty_positions()
        assert len(empties) > 0
        choice = random.choice(empties)
        row, col = choice.x_dist, choice.y_dist
        if value is None:
            # 0.1 probability of 4
            if random.random() > 0.1:
                value = 2
            else:
                value = 4
        new_tile = Tile(Vec(row, col), value)
        self.tiles[row][col] = new_tile
        self.notify_all(GameEvent(EventKind.tile_created, new_tile))

    def slide(self, pos: Vec,  direc: Vec):
        """Slide tile at row,col (if any)
        in direction (dx,dy) until it bumps into
        another tile or the edge of the board.
        """
        if self[pos] is None:
            return
        while True:
            new_pos = pos + direc
            if not self.in_bounds(new_pos):
                break
            if self[new_pos] is None:
                self._move_tile(pos, new_pos)
            elif self[pos] == self[new_pos]:
                self[pos].merge(self[new_pos])
                self._move_tile(pos, new_pos)
                break  # Stop moving when we merge with another tile
            else:
                # Stuck against another tile
                break
            pos = new_pos

    def _move_tile(self, old_pos: Vec, new_pos: Vec):
        self[old_pos].move_to(new_pos)
        self[new_pos] = self[old_pos]
        self[old_pos] = None

    def __getitem__(self, pos: Vec) -> Tile:
        return self.tiles[pos.x_dist][pos.y_dist]

    def __setitem__(self, pos: Vec, tile: Tile):
        self.tiles[pos.x_dist][pos.y_dist] = tile

    def _move(self, starting_pos: Vec, slide_dir: Vec, row_dir: Vec, col_dir: Vec):
        '''the repeatable code to call slide'''
        current_pos = starting_pos
        col_pos = starting_pos
        for i in range(1, GRID_SIZE + 1):
            for i in range(1, GRID_SIZE + 1):
                self.slide(current_pos, slide_dir)
                current_pos += row_dir
            col_pos += col_dir
            current_pos = col_pos

    def right(self):
        '''move all tiles right'''
        self._move(Vec(0,3), Vec(0,1), Vec(0,-1), Vec(1,0))

    def left(self):
        '''move all tiles left'''
        self._move(Vec(0,0), Vec(0,-1), Vec(0,1), Vec(1,0))

    def up(self):
        '''move all tiles up'''
        self._move(Vec(0,0), Vec(-1,0), Vec(0,1), Vec(1,0))

    def down(self):
        '''move all tiles down'''
        self._move(Vec(3,0), Vec(1,0), Vec(0,1), Vec(-1,0))

    def score(self) -> int:
        """Calculate a score from the board.
        (Differs from classic 1024, which calculates score
        based on sequence of moves rather than state of
        board.
        """
        score = 0
        for row in self.tiles:
            for col in row:
                if col is not None:
                    score += col.value
        return score
