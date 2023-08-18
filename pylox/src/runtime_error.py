class RuntimeError(Exception):
    def __init__(self, token, message): self.token,self.message = token, message
    def __str__(self): return f'[line {self.token.line}] Error: {self.message}'