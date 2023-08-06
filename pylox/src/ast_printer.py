from expr import Visitor

class AstPrinter(Visitor):
    def print(self, expr):
        return expr.accept(self)

    def visit_binary(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping(self, expr):
        return self.parenthesize("group", expr.expr)

    def visit_literal(self, expr):
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visit_unary(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def parenthesize(self, name, *exprs):
        builder = "(" + name
        for expr in exprs:
            builder += " "
            builder += expr.accept(self)
        builder += ")"
        return builder
    
if __name__ == "__main__":
    from expr import Binary, Grouping, Literal, Unary
    from my_token import Token, TokenType
    
    expr = Binary(
        Unary(
            Token(TokenType.MINUS, "-", None, 1),
            Literal(123)),
        Token(TokenType.STAR, "*", None, 1),
        Grouping(
            Literal(45.67)))
    
    print(AstPrinter().print(expr))