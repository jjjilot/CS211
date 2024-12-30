from expr import *

BINOP_DICT = {'+':Plus,
           '-':Minus,
           '*':Times,
           '/':Div}
UNOP_DICT = {'@':Abs,
             '~':Neg}

def calc(text: str):
    """Read and evaluate a single line formula."""
    try:
        stack = rpn_parse(text)
        if len(stack) == 0:
            print("(No expression)")
        else:
            # For a balanced expression there will be one Expr object
            # on the stack, but if there are more we'll just print
            # each of them
            for exp in stack:
                print(f"{exp} => {exp.eval()}")
    except Exception as e: 
        print(e)

def rpn_calc():
    txt = input("Expression (return to quit):")
    while len(txt.strip()) > 0:
        calc(txt)
        txt = input("Expression (return to quit):")
    print("Bye! Thanks for the math!")

def rpn_parse(text: str) -> list:
    """Parse text in reverse Polish notation
    into a list of expressions (exactly one if
    the expression is balanced).
    Example:
        rpn_parse("5 3 + 4 * 7")
          => [ Times(Plus(IntConst(5), IntConst(3)), IntConst(4)))),
               IntConst(7) ]
    May raise:  ValueError for lexical or syntactic error in input 
    """
    vals = text.split()
    stack = []
    for val in vals:
        if val.isnumeric():
            stack.append(IntConst(int(val)))
        elif is_binop(val):
            right = stack.pop()
            left = stack.pop()
            stack.append((binop_class(val)(left,right)))            
        elif is_unop(val):
            left = stack.pop()
            stack.append(unop_class(val)(left))
        elif is_var(val):
            stack.append(Var(val))
        elif val == "=":
            left = stack.pop()
            right = stack.pop()
            stack.append(Assign(left,right))
        else:
            raise KeyError('Error on Parse Eval')
    return stack

def is_binop(op:str)->bool:
    if op in BINOP_DICT: return True
    return False

def is_unop(op:str)->bool:
    if op in UNOP_DICT: return True
    return False

def is_var(op:str)->bool:
    for i in op:
        if i.isalpha(): return True
    return False

def binop_class(op:str)->"BinOp":
    return BINOP_DICT[op](0,0).__class__

def unop_class(op:str)->"UnOp":
    return UNOP_DICT[op](0).__class__

if __name__ == "__main__":
    rpn_calc()
