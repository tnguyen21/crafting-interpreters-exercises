class LoxInstance:
    def __init__(self, klass):
        self.klass,self.fields = klass, {}
    
    def __str__(self): return self.klass.name + " instance"

    def get(self, name):
        if name.lexeme in self.fields:
            return self.fields[name.lexeme]
        
        method = self.klass.find_method(name.lexeme)
        if method is not None: return method.bind(self)
        
        raise RuntimeError(name, "Undefined property '" + name.lexeme + "'.")

    def set(self, name, value): self.fields[name.lexeme] = value