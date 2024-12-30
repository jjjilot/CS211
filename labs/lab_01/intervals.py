"""Closed intervals of integers
Josh Jilot, 4/4/2023, CS 211"""

class Interval:
    """An interval [m..n] represents the set of integers from m to n."""

    def __init__(self, low: int, high: int):
        """Interval(low,high) represents the interval [low..high]"""
        self.low = low
        self.high = high
        assert low < high

    def contains(self, i: int) -> bool:
        """Integer i is within the closed interval"""
        if self.low <= i <= self.high:
            return True
        else:
            return False

    def overlaps(self, other: "Interval") -> bool:
        """i.overlaps(j) iff i and j have some elements in common"""
        if self.low > other.high or other.low > self.high:
            return False
        else:
            return True

    def __eq__(self, other: "Interval") -> bool:
        """Intervals are equal if they have the same low and high bounds"""
        return (self.low == other.low and self.high == other.high)

    def join(self, other: "Interval") -> "Interval":
        """Create a new Interval that contains the union of elements in self and other.
        Precondition: self and other must overlap."""
        assert self.overlaps(other)
        return (Interval(min(self.low, other.low), max(self.high, other.high)))
