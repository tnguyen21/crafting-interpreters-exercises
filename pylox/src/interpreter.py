from token_type import TokenType
from expr import Visitor as ExprVisitor
from stmt import Visitor as StmtVisitor
from runtime_error import RuntimeError

class Interpreter(ExprVisitor, StmtVisitor):
    def __init__(self, lox_instance):
        self.lox = lox_instance

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

    def visit_grouping(self, expr):
        return self.evaluate(expr.expr)

    def visit_literal(self, expr):
        return expr.value

    def visit_unary(self, expr):
        right = self.evaluate(expr.right)

        if expr.operator.type == TokenType.MINUS:
            self.check_number_operand(expr.operator, right)
            return -right
        elif expr.operator.type == TokenType.BANG:
            return not self.is_truthy(right)

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
    
    def visit_expression(self, stmt):
        self.evaluate(stmt.expr)
    
    def visit_print(self, stmt):
        value = self.evaluate(stmt.expr)
        print(self.stringify(value))
    
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