from lox_callable import LoxCallable
from environment import Environment
from return_exception import Return

class LoxFunction(LoxCallable):
    def __init__(self, declaration, closure, is_initializer):
        self.declaration = declaration
        self.closure = closure
        self.is_initializer = is_initializer

    def __str__(self):
        return f"<fn {self.declaration.name.lexeme}>"

    def bind(self, instance):
        environment = Environment(self.closure)
        environment.define("this", instance)
        return LoxFunction(self.declaration, environment, self.is_initializer)

    def arity(self):
        return len(self.declaration.params)

    def call(self, interpreter, arguments):
        environment = Environment(self.closure)
        for i in range(len(self.declaration.params)):
            environment.define(self.declaration.params[i].lexeme, arguments[i])
        
        try:
            interpreter.execute_block(self.declaration.body, environment)
        except Return as ret:
            if self.is_initializer: return self.closure.get_at(0, "this")
            return ret.value

        if self.is_initializer: return self.closure.get_at(0, "this")
