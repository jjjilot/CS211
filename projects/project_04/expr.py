# One global environment (scope) for
# the calculator

# One global environment variable
from typing import Dict
ENV: Dict[str, "IntConst"] = {}

class Expr(object):
    """Abstract base class of all expressions."""

    def eval(self) -> "IntConst":
        """Implementations of eval should return an integer constant."""
        raise NotImplementedError(
            f"'eval' not implemented in {self.__class__.__name__}\n"
            "Each concrete Expr class must define 'eval'")

    def __str__(self) -> str:
        """Implementations of __str__ should return the expression in algebraic notation"""
        raise NotImplementedError(
            f"'__str__' not implemented in {self.__class__.__name__}\n"
            "Each concrete Expr class must define '__str__'")

    def __repr__(self) -> str:
        """Implementations of __repr__ should return a string that looks like
        the constructor, e.g., Plus(IntConst(5), IntConst(4))
        """
        raise NotImplementedError(
            f"'__repr__' not implemented in {self.__class__.__name__}\n"
            "Each concrete Expr class must define '__repr__'")

class IntConst():
    '''Integers/Constants'''
    def __init__(self, const: int):
        self.value = const

    def eval(self) -> 'IntConst':
        return self

    def __str__(self) -> str:
        return f'{self.value}'

    def __repr__(self) -> str:
        return f'IntConst({self.value})'

    def __eq__(self, other: Expr):
        return isinstance(other, IntConst) and self.value == other.value

class BinOp(Expr):
    """Abstract base class for binary operations"""
    def __init__(self, left: Expr, right: Expr, symbol: str="?Operation symbol undefined"):
        self.left = left
        self.right = right
        self.symbol = symbol

    def __str__(self) -> str:
        return f"({self.left} {self.symbol} {self.right})"

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({repr(self.left)}, {repr(self.right)})'

    def _apply(self, left: int, right: int) -> int:
        """Each concrete BinOp subclass provides the appropriate method"""
        raise NotImplementedError(
            f"'_apply' not implemented in {self.__class__.__name__}\n"
            "Each concrete BinOp class must define '_apply'")

    def eval(self) -> "IntConst":
        """Each concrete subclass must define _apply(int, int)->int"""
        left_val = self.left.eval()
        right_val = self.right.eval()
        return IntConst(self._apply(left_val.value, right_val.value))

class Plus(BinOp):
    """Expr + Expr"""
    def __init__(self, left: Expr, right: Expr):
        super().__init__(left, right, symbol="+")

    def _apply(self, left: int, right: int) -> int:
        return left + right

class Minus(BinOp):
    """Expr + Expr"""
    def __init__(self, left: Expr, right: Expr):
        super().__init__(left, right, symbol="-")

    def _apply(self, left: int, right: int) -> int:
        return left - right

class Times(BinOp):
    """left * right"""

    def __init__(self, left: Expr, right: Expr):
        super().__init__(left, right, symbol="*")

    def _apply(self, left: int, right: int) -> int:
        return left * right

class Div(BinOp):
    """left * right"""

    def __init__(self, left: Expr, right: Expr):
        super().__init__(left, right, symbol="//")

    def _apply(self, left: int, right: int) -> int:
        return left // right

class UnOp(Expr):
    """Abstract base class for binary operations"""
    def __init__(self, const: Expr, symbol: str="?Operation symbol undefined"):
        self.const = const
        self.symbol = symbol

    def __str__(self) -> str:
        return f"({self.symbol} {self.const})"

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({repr(self.const)})'

    def _apply(self, const: int) -> int:
        """Each concrete BinOp subclass provides the appropriate method"""
        raise NotImplementedError(
            f"'_apply' not implemented in {self.__class__.__name__}\n"
            "Each concrete BinOp class must define '_apply'")

    def eval(self) -> "IntConst":
        """Each concrete subclass must define _apply(int, int)->int"""
        const_val = self.const.eval()
        return IntConst(self._apply(const_val.value))

class Neg(UnOp):
    '''negation of const'''
    def __init__(self, const: Expr):
        super().__init__(const, symbol='~')

    def _apply(self, const) -> int:
        return const * -1

class Abs(UnOp):
    '''absolute value of const'''
    def __init__(self, const: Expr):
        super().__init__(const, symbol='@')

    def _apply(self, const) -> int:
        return abs(const)

class UndefinedVariable(Exception):
    """Raised when expression tries to use a variable that 
    is not in ENV
    """
    pass

class Var(Expr):

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Var({self.name})"

    def eval(self):
        global ENV
        if self.name in ENV:
            return ENV[self.name]
        else:
            raise UndefinedVariable(f"{self.name} has not been assigned a value")

    def assign(self, value: IntConst):
        global ENV
        ENV[self.name] = value

class Assign(Expr):
    """Assignment:  x = E represented as Assign(x, E)"""

    def __init__(self, left: Var, right: Expr):
        assert isinstance(left, Var)  # Can only assign to variables!
        self.left = left
        self.right = right

    def eval(self) -> IntConst:
        r_val = self.right.eval()
        self.left.assign(r_val)
        return r_val

    def __str__(self) -> str:
        return f'({self.left} = {self.right})'

    def __repr__(self) -> str:
        return f'Assign({repr(self.left)}, {repr(self.right)})'
