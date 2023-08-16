from my_token import Token

class Expr:
    def accept(self, visitor):
        method_name = 'visit_' + self.__class__.__name__.lower()
        method = getattr(visitor, method_name)
        return method(self)

class Assign(Expr):
    def __init__(self, name: Token, value: Expr):
        self.name,self.value = name,value

class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left,self.operator,self.right = left,operator,right

class Call(Expr):
    def __init__(self, callee: Expr, paren: Token, arguments: [Expr]):
        self.callee,self.paren,self.arguments = callee,paren,arguments

class Get(Expr):
    def __init__(self, object: Expr, name: Token):
        self.object,self.name = object,name

class Set(Expr):
    def __init__(self, object: Expr, name: Token, value: Expr):
        self.object,self.name,self.value = object,name,value

class Grouping(Expr):
    def __init__(self, expr: Expr):
        self.expr = expr

class Literal(Expr):
    def __init__(self, value: object):
        self.value = value

class Logical(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left,self.operator,self.right = left,operator,right

class Unary(Expr):
    def __init__(self, operator: Token, right: Expr):
        self.operator,self.right = operator,right

class This(Expr):
    def __init__(self, keyword: Token):
        self.keyword = keyword

class Variable(Expr):
    def __init__(self, name: Token):
        self.name = name

class Visitor:
    def visit_assign(self, expr: Assign): pass
    def visit_binary(self, expr: Binary): pass
    def visit_call(self, expr: Call): pass
    def visit_get(self, expr: Get): pass
    def visit_set(self, expr: Set): pass
    def visit_grouping(self, expr: Grouping): pass
    def visit_literal(self, expr: Literal): pass
    def visit_logical(self, expr: Logical): pass
    def visit_unary(self, expr: Unary): pass
    def visit_this(self, expr: This): pass
    def visit_variable(self, expr: Variable): pass

