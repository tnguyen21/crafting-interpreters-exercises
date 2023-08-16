from token_type import TokenType
from expr import Assign, Visitor as ExprVisitor
from stmt import Block, Visitor as StmtVisitor
from lox_callable import LoxCallable
from lox_function import LoxFunction
from native import Clock
from runtime_error import RuntimeError
from environment import Environment
from return_exception import Return

class Interpreter(ExprVisitor, StmtVisitor):
    def __init__(self, lox_instance):
        self.lox = lox_instance
        self.globals = Environment()
        self.environment = self.globals
        self.locals = {}

        self.globals.define('clock', Clock())

    def interpret(self, statements):
        try:
            for statement in statements: self.execute(statement)
        except RuntimeError as e:
            self.lox.runtime_error(e)

    def visit_binary(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if expr.operator.type == TokenType.MINUS:
            self.check_number_operands(expr.operator, left, right)
            return left - right
        elif expr.operator.type == TokenType.SLASH:
            self.check_number_operands(expr.operator, left, right)
            return left / right
        elif expr.operator.type == TokenType.STAR:
            self.check_number_operands(expr.operator, left, right)
            return left * right
        elif expr.operator.type == TokenType.PLUS:
            if isinstance(left, (float, str)) and isinstance(right, (float, str)):
                return left + right
            else:
                raise RuntimeError(f'Operands must be two numbers or two strings, not {left.__class__.__name__} and {right.__class__.__name__}')
        elif expr.operator.type == TokenType.GREATER:
            self.check_number_operand(expr.operator, left)
            return left > right
        elif expr.operator.type == TokenType.GREATER_EQUAL:
            self.check_number_operands(expr.operator, left, right)
            return left >= right
        elif expr.operator.type == TokenType.LESS:
            self.check_number_operands(expr.operator, left, right)
            return left < right
        elif expr.operator.type == TokenType.LESS_EQUAL:
            self.check_number_operands(expr.operator, left, right)
            return left <= right
        elif expr.operator.type == TokenType.BANG_EQUAL:
            self.check_number_operands(expr.operator, left, right)
            return not self.is_equal(left, right)
        elif expr.operator.type == TokenType.EQUAL_EQUAL:
            self.check_number_operands(expr.operator, left, right)
            return self.is_equal(left, right)

    def visit_call(self, expr):
        callee = self.evaluate(expr.callee)

        arguments = []
        for argument in expr.arguments:
            arguments.append(self.evaluate(argument))

        if not isinstance(callee, LoxCallable):
            raise RuntimeError(f'Can only call functions and classes.')

        function = callee
        if len(arguments) != function.arity():
            raise RuntimeError(f'Expected {function.arity()} arguments but got {len(arguments)}.')

        return function.call(self, arguments)

    def visit_grouping(self, expr):
        return self.evaluate(expr.expr)

    def visit_literal(self, expr):
        return expr.value
    
    def visit_logical(self, expr):
        left = self.evaluate(expr.left)

        if expr.operator.type == TokenType.OR:
            if self.is_truthy(left): return left
        else:
            if not self.is_truthy(left): return left

        return self.evaluate(expr.right)

    def visit_unary(self, expr):
        right = self.evaluate(expr.right)

        if expr.operator.type == TokenType.MINUS:
            self.check_number_operand(expr.operator, right)
            return -right
        elif expr.operator.type == TokenType.BANG:
            return not self.is_truthy(right)
    
    def visit_variable(self, expr):
        return self.look_up_variable(expr.name, expr)

    def look_up_variable(self, name, expr):
        distance = self.locals.get(expr)
        if distance is not None:
            return self.environment.get_at(distance, name.lexeme)
        else:
            return self.globals.get(name)

    def check_number_operand(self, operator, operand):
        if isinstance(operand, float): return
        raise RuntimeError(f'Operand must be a number, not {operand.__class__.__name__}')

    def check_number_operands(self, operator, left, right):
        if isinstance(left, float) and isinstance(right, float): return
        raise RuntimeError(f'Operands must be numbers, not {left.__class__.__name__} and {right.__class__.__name__}')

    def evaluate(self, expr):
        return expr.accept(self)
    
    def execute(self, stmt):
        stmt.accept(self)
    
    def resolve(self, expr, depth):
        self.locals[expr] = depth
    
    def execute_block(self, statements, environment):
        previous = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous

    def visit_block(self, stmt: Block):
        self.execute_block(stmt.statements, Environment(self.environment))

    def visit_expression(self, stmt):
        self.evaluate(stmt.expr)

    def visit_function(self, stmt):
        function = LoxFunction(stmt, self.environment)
        self.environment.define(stmt.name.lexeme, function)

    def visit_if(self, stmt):
        if self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self.execute(stmt.else_branch)
    
    def visit_print(self, stmt):
        value = self.evaluate(stmt.expr)
        print(self.stringify(value))

    def visit_return(self, stmt):
        value = None
        if stmt.value is not None: value = self.evaluate(stmt.value)
        raise Return(value)

    def visit_var(self, stmt):
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)
        self.environment.define(stmt.name.lexeme, value)

    def visit_while(self, stmt):
        while self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)

    def visit_assign(self, expr: Assign):
        value = self.evaluate(expr.value)
        distance = self.locals.get(expr)
        if distance is not None:
            self.environment.assign_at(distance, expr.name, value)
        else:
            self.globals.assign(expr.name, value)
        return value
    
    def is_truthy(self, obj):
        if obj is None:             return False
        elif isinstance(obj, bool): return obj
        else:                       return True

    def is_equal(self, a, b):
        if a is None and b is None: return True
        elif a is None:             return False
        else:                       return a == b

    def stringify(self, obj):
        if obj is None: return 'nil'

        if isinstance(obj, float):
            text = str(obj)
            if text.endswith('.0'):
                text = text[:-2]
            return text

        return str(obj)