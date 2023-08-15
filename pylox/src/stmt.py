from expr import Expr
from my_token import Token

class Stmt:
    def accept(self, visitor):
        method_name = 'visit_' + self.__class__.__name__.lower()
        method = getattr(visitor, method_name)
        return method(self)

class Block(Stmt):
    def __init__(self, statements: [Stmt]):
        self.statements = statements

class Expression(Stmt):
    def __init__(self, expr: Expr):
        self.expr = expr

class Print(Stmt):
    def __init__(self, expr: Expr):
        self.expr = expr

class Var(Stmt):
    def __init__(self, name: Token, initializer: Expr):
        self.name = name
        self.initializer = initializer

class Visitor:
    def visit_block(self, stmt: Block): pass
    def visit_expression(self, stmt: Expression): pass
    def visit_print(self, stmt: Print): pass
    def visit_var(self, stmt: Var): pass

