from expr import Expr
from my_token import Token

class Stmt:
    def accept(self, visitor):
        method_name = 'visit_' + self.__class__.__name__.lower()
        method = getattr(visitor, method_name)
        return method(self)

class Expression(Stmt):
    def __init__(self, expr: Expr):
        self.expr = expr


class Print(Stmt):
    def __init__(self, expr: Expr):
        self.expr = expr


class Visitor:
    def visit_expression(self, stmt: Expression): pass
    def visit_print(self, stmt: Print): pass

