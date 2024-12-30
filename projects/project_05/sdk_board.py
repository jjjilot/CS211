

"""
A Sudoku board holds a matrix of tiles.
Each row and column and also sub-blocks
are treated as a group (sometimes called
a 'nonet'); when solved, each group must contain
exactly one occurrence of each of the
symbol choices.
M Young, Feb 2019.
"""
import enum
from typing import Sequence, List, Set
from sdk_config import NCOLS, NROWS, ROOT
from sdk_config import UNKNOWN, CHOICES

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# --------------------------------
#  The events for MVC
# --------------------------------

class Event(object):
    """Abstract base class of all events, both for MVC
    and for other purposes.
    """
    pass

# ---------------
# Listeners (base class)
# ---------------

class Listener(object):
    """Abstract base class for listeners.
    Subclass this to make the notification do
    something useful.
    """

    def __init__(self):
        """Default constructor for simple listeners without state"""
        pass

    def notify(self, event: Event):
        """The 'notify' method of the base class must be
        overridden in concrete classes.
        """
        raise NotImplementedError("You must override Listener.notify")


# --------------------------------------
# Events and listeners for Tile objects
# --------------------------------------

class EventKind(enum.Enum):
    TileChanged = 1
    TileGuessed = 2


class TileEvent(Event):
    """Abstract base class for things that happen
    to tiles. We always indicate the tile.  Concrete
    subclasses indicate the nature of the event.
    """

    def __init__(self, tile: 'Tile', kind: EventKind):
        self.tile = tile
        self.kind = kind
        # Note 'Tile' type is a forward reference;
        # Tile class is defined below

    def __str__(self):
        """Printed representation includes name of concrete subclass"""
        return f"{repr(self.tile)}"

class TileListener(Listener):
    def notify(self, event: TileEvent):
        raise NotImplementedError(
            "TileListener subclass needs to override notify(TileEvent)")


class Listenable:
    """Objects to which listeners (like a view component) can be attached"""

    def __init__(self):
        self.listeners = []

    def add_listener(self, listener: Listener):
        self.listeners.append(listener)

    def notify_all(self, event: Event):
        for listener in self.listeners:
            listener.notify(event)

# ----------------------------------------------
#      Tile class
# ----------------------------------------------

class Tile(Listenable):
    """One tile on the Sudoku grid.
    Public attributes (read-only): value, which will be either
    UNKNOWN or an element of CHOICES; candidates, which will
    be a set drawn from CHOICES.  If value is an element of
    CHOICES,then candidates will be the singleton containing
    value.  If candidates is empty, then no tile value can
    be consistent with other tile values in the grid.
    value is a public read-only attribute; change it
    only through the access method set_value or indirectly
    through method remove_candidates.
    """
    def __init__(self, row: int, col: int, value=UNKNOWN):
        super().__init__()
        assert value == UNKNOWN or value in CHOICES
        self.row = row
        self.col = col
        self.set_value(value)

    def set_value(self, value: str):
        if value in CHOICES:
            self.value = value
            self.candidates = {value}
        else:
            self.value = UNKNOWN
            self.candidates = set(CHOICES)
        self.notify_all(TileEvent(self, EventKind.TileChanged))

    def could_be(self, value: str) -> bool:
        """True iff value is a candidate value for this tile"""
        return value in self.candidates

    def remove_candidates(self, used_values: Set[str]):
        """The used values cannot be a value of this unknown tile.
        We remove those possibilities from the list of candidates.
        If there is exactly one candidate left, we set the
        value of the tile.
        Returns:  True means we eliminated at least one candidate,
        False means nothing changed (none of the 'used_values' was
        in our candidates set).
        """
        new_candidates = self.candidates.difference(used_values)
        if new_candidates == self.candidates:
            # Didn't remove any candidates
            return False
        self.candidates = new_candidates
        if len(self.candidates) == 1:
            self.set_value(new_candidates.pop())
        self.notify_all(TileEvent(self, EventKind.TileChanged))
        return True

    def __str__(self) -> str:
        if self.value == UNKNOWN: return UNKNOWN
        return self.value

    def __repr__(self) -> str:
        return f"Tile({self.row}, {self.col}, '{self.value}')"

# ------------------------------
#  Board class
# ------------------------------

class Board(object):
    """A board has a matrix of tiles"""

    def __init__(self):
        """The empty board"""
        # Row/Column structure: Each row contains columns
        self.tiles: List[List[Tile]] = [ ]
        for row in range(NROWS):
            cols = [ ]
            for col in range(NCOLS):
                cols.append(Tile(row, col))
            self.tiles.append(cols)
        self._form_groups()

    def _form_groups(self):
        self.groups = []
        # Rows
        for row in self.tiles:
            self.groups.append(row)

        # Columns
        # Adding groups for columns is not too difficult. 
        for i in range(len(self.tiles)):
            new_group = []
            for j in range(len(self.tiles[i])):
                new_group.append(self.tiles[j][i])
            self.groups.append(new_group)

        # Blocks
        for block_row in range(ROOT):
            for block_col in range(ROOT):
                group = [ ]
                for row in range(ROOT):
                    for col in range(ROOT):
                        row_addr = (ROOT * block_row) + row
                        col_addr = (ROOT * block_col) + col
                        group.append(self.tiles[row_addr][col_addr])
                self.groups.append(group)

    def set_tiles(self, tile_values: Sequence[Sequence[str]] ):
        """Set the tile values a list of lists or a list of strings"""
        for row_num in range(NROWS):
            for col_num in range(NCOLS):
                tile = self.tiles[row_num][col_num]
                tile.set_value(tile_values[row_num][col_num])


    def is_consistent(self) -> bool:
        """No duplicates in any group"""
        for group in self.groups:
            used_symbols = set()
            for tile in group:
                if tile.value in CHOICES:
                    if tile.value in used_symbols:
                        return False
                    else:
                        used_symbols.add(tile.value)
        return True


    def naked_single(self) -> bool:
        """Eliminate candidates and check for sole remaining possibilities.
        Return value True means we crossed off at least one candidate.
        Return value False means we made no progress.
        """
        success = False
        for group in self.groups:
            used_symbols = set()
            for tile in group:
                if tile.value in CHOICES:
                    used_symbols.add(tile.value)
            for tile in group:
                if tile.remove_candidates(used_symbols):
                    success = True
        return success

    def hidden_single(self) -> bool:
        """Sets a tile value if it is the only tile in a group that can
        take a value.  Returns True if any tiles have been determined this way.
        """
        success = False
        for group in self.groups:
            leftovers = set(CHOICES)
            for tile in group:
                if tile.value in CHOICES:
                    leftovers.discard(tile.value)
            for val in leftovers:
                occurences = []
                for tile in group:
                    if val in tile.candidates:
                        occurences.append(tile)
                if len(occurences) == 1:
                    occurences[0].set_value(val)
                    occurences[0].notify_all(TileEvent(tile, EventKind.TileChanged))
                    success = True
        return success

    def is_complete(self) -> bool:
        """All tiles are filled?"""
        for group in self.groups:
            for tile in group:
                if tile.value == UNKNOWN: return False
        return self.is_consistent()

    def min_tile(self) -> Tile:
        """Find tile with minimum choices"""
        current = [0, 'abcdefghi']
        for group in self.groups:
            for tile in group:
                if tile.value == UNKNOWN and len(tile.candidates) < len(current[1]):
                    current[0] = tile
                    current[1] = tile.candidates
        return current[0]

    def solve(self) -> bool:
        """Recursive guess-and-check between
        constraint propagation phases.
        """
        self.propagate()
        if not self.is_consistent():
            return False
        if self.is_complete():
            return True
        focus = self.min_tile()
        log.debug(f"Focusing on {repr(focus)} with candidates {focus.candidates}")
        saved = self.as_list()
        for choice in list(focus.candidates):
            log.debug(f"Guessing {choice}")
            focus.set_value(choice)
            if self.solve():
                log.debug("Yaha, yes")
                return True
            log.debug(f"Nope, {choice} didn't work")
            self.set_tiles(saved)
        # None of those choices worked
        return False
        
    def propagate(self):
        """Repeat solution tactics until we
        don't make any progress, whether or not
        the board is solved.
        """
        progress = True
        while progress:
            progress = self.naked_single()
            self.hidden_single()
        return

    def __str__(self) -> str:
        """In Sadman Sudoku format"""
        return "\n".join(self.as_list())

    def as_list(self) -> List[str]:
        """Inverse of set_tiles"""
        row_syms = [ ]
        for row in self.tiles:
            values = [tile.value for tile in row]
            row_syms.append("".join(values))
        return row_syms
