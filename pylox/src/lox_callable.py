class LoxCallable:
    def __init__(self, declaration=None):
        self.declaration = declaration

    def call(self, interpreter, arguments):
        raise NotImplementedError()

    def arity(self):
        raise NotImplementedError()