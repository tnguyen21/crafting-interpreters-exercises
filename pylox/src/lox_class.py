from lox_callable import LoxCallable
from lox_instance import LoxInstance

class LoxClass(LoxCallable):
    def __init__(self, name, superclass, methods):
        self.name,self.superclass,self.methods = name,superclass,methods
    
    def __str__(self): return self.name

    def find_method(self, name):
        if name in self.methods:          return self.methods[name]
        elif self.superclass is not None: return self.superclass.find_method(name)
        else:                             return None

    def arity(self):
        initializer = self.find_method("init")
        if initializer is None: return 0
        return initializer.arity()

    def call(self, interpreter, arguments):
        instance = LoxInstance(self)
        initializer = self.find_method("init")
        if initializer is not None:
            initializer.bind(instance).call(interpreter, arguments)
        return instance