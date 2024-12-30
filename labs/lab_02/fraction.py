'''Josh Jilot - 4/11/2023
CS 211 Lab 2: classes, objects, and methods'''
class Fraction:
    '''a fraction n/d is composed of a numerator and a denominator'''

    def __init__(self, numerator: int, denominator: int):
        '''the numerator and denominator of a fraction must be positive
        integers but the numerator can be 0'''
        assert numerator >= 0 and denominator > 0
        self.numerator = numerator
        self.denominator = denominator
        self.simplify()

    def __str__(self) -> str:
        '''fractions are represented as numerator/denominator'''
        return f'{self.numerator}/{self.denominator}'

    def __repr__(self) -> str:
        return f'Fraction({self.numerator},{self.denominator})'

    def __add__(self, other: 'Fraction') -> 'Fraction':
        '''fractions can be added to form other fractions'''
        self.simplify()
        return Fraction(self.numerator * other.denominator + self.denominator *\
                        other.numerator, self.denominator * other.denominator)

    def __mul__(self, other: 'Fraction') -> 'Fraction':
        '''fractions can be multiplied to form other fraction'''
        self.simplify()
        return Fraction(self.numerator * other.numerator,\
                        self.denominator * other.denominator)

    def simplify(self) -> 'Fraction':
        '''simplifies fractions to their reduced form'''
        gcd = 1
        for i in range(1, min(self.numerator, self.denominator) + 1):
            if self.numerator % i == 0 and self.denominator % i == 0:
                gcd = i
        self.numerator = int(self.numerator / gcd)
        self.denominator = int(self.denominator / gcd)
        return self
