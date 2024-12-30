'''Point Class
Josh Jilot, 4/6/2023, CS 211'''

class Point:
    '''An (x,y) position is represented as a point'''
    def __init__(self, x: int, y: int):
        '''Point(x,y) represents the x and y coordinates of the position'''
        self.x = x
        self.y = y

    def move(self, dx: int, dy: int):
        '''Change x and y by dx and dy respectively'''
        self.x += dx
        self.y += dy

    def __eq__(self, other: 'Point'):
        '''Equal points have the same x and y values'''
        return(self.x == other.x and self.y == other.y)

    def __str__(self):
        '''Strings are represented as (x,y) pairs'''
        return f'({self.x}, {self.y})'
