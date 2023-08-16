from lox_callable import LoxCallable

class Clock(LoxCallable):
    def arity(self):
        return 0

    def call(self, interpreter, arguments):
        import time
        return time.time()

    def __str__(self):
        return "<native fn clock>"

    def __repr__(self):
        return str(self)