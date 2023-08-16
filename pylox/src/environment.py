from my_token import Token
from runtime_error import RuntimeError

class Environment:
    def __init__(self, enclosing = None):
        self.enclosing: Environment = enclosing
        self.values: dict[str, object] = {}

    def get(self, name: Token) -> object:
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        
        if self.enclosing is not None:
            return self.enclosing.get(name)

        raise RuntimeError(name, f"Undefined variable '{name.lexeme}'.")

    def assign(self, name: Token, value: object):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
        
        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return

        raise RuntimeError(name, f"Undefined variable '{name.lexeme}'.")

    def define(self, name: str, value: object):
        self.values[name] = value
    
    def ancestor(self, distance: int):
        environment = self
        for _ in range(distance):
            environment = environment.enclosing
        return environment

    def get_at(self, distance: int, name: str) -> object:
        return self.ancestor(distance).values[name]

    def assign_at(self, distance: int, name: Token, value: object):
        self.ancestor(distance).values[name.lexeme] = value