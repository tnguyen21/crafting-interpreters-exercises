from my_token import Token

class Expr:
    def accept(self, visitor):
        method_name = 'visit_' + self.__class__.__name__.lower()
        method = getattr(visitor, method_name)
        return method(self)

class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

class Grouping(Expr):
    def __init__(self, expr: Expr):
        self.expr = expr

class Literal(Expr):
    def __init__(self, value: object):
        self.value = value

class Unary(Expr):
    def __init__(self, operator: Token, right: Expr):
        self.operator = operator
        self.right = right

class Visitor:
    def visit_binary(self, expr: Binary): pass
    def visit_grouping(self, expr: Grouping): pass
    def visit_literal(self, expr: Literal): pass
    def visit_unary(self, expr: Unary): pass

