class LoxClass:
    def __init__(self, name):
        self.name = name
        self.methods = {}
    
    def __str__(self): return self.name