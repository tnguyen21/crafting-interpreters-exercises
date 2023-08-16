from expr import Visitor as ExprVisitor
from stmt import Visitor as StmtVisitor
from expr import Expr
from stmt import Stmt
from enum import Enum
from runtime_error import RuntimeError

class FunctionType(Enum):
    NONE = 0
    FUNCTION = 1


class Resolver(ExprVisitor, StmtVisitor):
    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.scopes = []
        self.current_function = FunctionType.NONE
    
    def visit_block(self, stmt):
        self.begin_scope()
        self.resolve(stmt.statements)
        self.end_scope()
    
    def visit_class(self, stmt):
        self.declare(stmt.name)
        self.define(stmt.name)

    def visit_expression(self, stmt): self.resolve(stmt.expr)
    
    def visit_function(self, stmt):
        self.declare(stmt.name)
        self.define(stmt.name)
        self.resolve_function(stmt, FunctionType.FUNCTION)
    
    def visit_if(self, stmt):
        self.resolve(stmt.condition)
        self.resolve(stmt.then_branch)
        if stmt.else_branch != None: self.resolve(stmt.else_branch)

    def visit_print(self, stmt): self.resolve(stmt.expr)

    def visit_return(self, stmt):
        if self.current_function == FunctionType.NONE:
            raise RuntimeError(stmt.keyword, "Cannot return from top-level code.")
        if stmt.value is not None: self.resolve(stmt.value)

    def visit_var(self, stmt):
        self.declare(stmt.name)
        if stmt.initializer != None: self.resolve(stmt.initializer)
        self.define(stmt.name)
    
    def visit_while(self, stmt):
        self.resolve(stmt.condition)
        self.resolve(stmt.body)
    
    def visit_assign(self, expr):
        self.resolve(expr.value)
        self.resolve_local(expr, expr.name)
    
    def visit_binary(self, expr):
        self.resolve(expr.left)
        self.resolve(expr.right)
    
    def visit_call(self, expr):
        self.resolve(expr.callee)
        for argument in expr.arguments:
            self.resolve(argument)

    def visit_grouping(self, expr): self.resolve(expr.expr)
    # omit visit literal -- no vars or exprs to resolve

    def visit_logical(self, expr):
        self.resolve(expr.left)
        self.resolve(expr.right)
    
    def visit_unary(self, expr): self.resolve(expr.right)

    def visit_variable(self, expr):
        if len(self.scopes) != 0 and self.scopes[-1].get(expr.name.lexeme) == False:
            raise RuntimeError(expr.name, "Cannot read local variable in its own initializer.")
        self.resolve_local(expr, expr.name)

    def resolve(self, line):
        if isinstance(line, list):
            for statement in line:
                self.resolve(statement)
        
        elif isinstance(line, (Stmt, Expr)):
            line.accept(self)
        
        else:
            raise RuntimeError(line, "Unknown type of line passed to resolve function.")
    
    def resolve_function(self, function, type):
        enclosing_function = self.current_function
        self.current_function = type
        self.begin_scope()
        for param in function.params:
            self.declare(param)
            self.define(param)
        self.resolve(function.body)
        self.end_scope()
        self.current_function = enclosing_function

    def begin_scope(self): self.scopes.append({})
    def end_scope(self):   self.scopes.pop()

    def declare(self, name):
        if len(self.scopes) == 0: return
        scope = self.scopes[-1]
        if name.lexeme in scope:
            raise RuntimeError(name, "Variable with this name already declared in this scope.")
        scope[name.lexeme] = False
    
    def define(self, name):
        if len(self.scopes) == 0: return
        self.scopes[-1][name.lexeme] = True
    
    def resolve_local(self, expr, name):
        for i in range(len(self.scopes) - 1, -1, -1):
            if name.lexeme in self.scopes[i]:
                self.interpreter.resolve(expr, len(self.scopes) - 1 - i)
                return