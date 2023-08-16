from typing import Any
from token_type import TokenType

class Token:
    def __init__(self, type: TokenType, lexeme: str, literal: Any, line: int):
        self.type,self.lexeme,self.literal,self.line = type,lexeme,literal,line

    def __str__(self): return f"{self.type} {self.lexeme} {self.literal}"
