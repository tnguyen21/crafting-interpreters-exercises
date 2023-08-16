from lox_callable import LoxCallable
from lox_instance import LoxInstance

class LoxClass(LoxCallable):
    def __init__(self, name, methods):
        self.name = name
        self.methods = methods
    
    def __str__(self): return self.name

    def find_method(self, name): return self.methods.get(name, None)

    def arity(self):
        # initializer = self.find_method("init")
        # if initializer is None: return 0
        # return initializer.arity()
        return 0

    def call(self, interpreter, arguments):
        instance = LoxInstance(self)
        # initializer = self.find_method("init")
        # if initializer is not None:
        #     initializer.bind(instance).call(interpreter, arguments)
        return instance