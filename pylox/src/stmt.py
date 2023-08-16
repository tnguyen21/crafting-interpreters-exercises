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

class Function(Stmt):
    def __init__(self, name: Token, params: [Token], body: [Stmt]):
        self.name = name
        self.params = params
        self.body = body

class Class(Stmt):
    def __init__(self, name: Token, methods: [Function]):
        self.name = name
        self.methods = methods

class If(Stmt):
    def __init__(self, condition: Expr, then_branch: Stmt, else_branch: Stmt):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

class Print(Stmt):
    def __init__(self, expr: Expr):
        self.expr = expr

class Return(Stmt):
    def __init__(self, keyword: Token, value: Expr):
        self.keyword = keyword
        self.value = value

class Var(Stmt):
    def __init__(self, name: Token, initializer: Expr):
        self.name = name
        self.initializer = initializer

class While(Stmt):
    def __init__(self, condition: Expr, body: Stmt):
        self.condition = condition
        self.body = body

class Visitor:
    def visit_block(self, stmt: Block): pass
    def visit_expression(self, stmt: Expression): pass
    def visit_function(self, stmt: Function): pass
    def visit_class(self, stmt: Class): pass
    def visit_if(self, stmt: If): pass
    def visit_print(self, stmt: Print): pass
    def visit_return(self, stmt: Return): pass
    def visit_var(self, stmt: Var): pass
    def visit_while(self, stmt: While): pass

