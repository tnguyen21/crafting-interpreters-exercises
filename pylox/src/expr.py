from my_token import Token

class Expr:
    def accept(self, visitor):
        method_name = 'visit_' + self.__class__.__name__.lower()
        method = getattr(visitor, method_name)
        return method(self)

class Assign(Expr):
    def __init__(self, name: Token, value: Expr):
        self.name = name
        self.value = value

class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

class Call(Expr):
    def __init__(self, callee: Expr, paren: Token, arguments: [Expr]):
        self.callee = callee
        self.paren = paren
        self.arguments = arguments

class Grouping(Expr):
    def __init__(self, expr: Expr):
        self.expr = expr

class Literal(Expr):
    def __init__(self, value: object):
        self.value = value

class Logical(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

class Unary(Expr):
    def __init__(self, operator: Token, right: Expr):
        self.operator = operator
        self.right = right

class Variable(Expr):
    def __init__(self, name: Token):
        self.name = name

class Visitor:
    def visit_assign(self, expr: Assign): pass
    def visit_binary(self, expr: Binary): pass
    def visit_call(self, expr: Call): pass
    def visit_grouping(self, expr: Grouping): pass
    def visit_literal(self, expr: Literal): pass
    def visit_logical(self, expr: Logical): pass
    def visit_unary(self, expr: Unary): pass
    def visit_variable(self, expr: Variable): pass

