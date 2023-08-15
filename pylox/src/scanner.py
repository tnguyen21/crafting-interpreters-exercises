from my_token import Token
from token_type import TokenType

class Scanner:
    keywords = {
        "and":    TokenType.AND,
        "class":  TokenType.CLASS,
        "else":   TokenType.ELSE,
        "false":  TokenType.FALSE,
        "for":    TokenType.FOR,
        "fun":    TokenType.FUN,
        "if":     TokenType.IF,
        "nil":    TokenType.NIL,
        "or":     TokenType.OR,
        "print":  TokenType.PRINT,
        "return": TokenType.RETURN,
        "super":  TokenType.SUPER,
        "this":   TokenType.THIS,
        "true":   TokenType.TRUE,
        "var":    TokenType.VAR,
        "while":  TokenType.WHILE
    }

    def __init__(self, lox_instance, source: str):
        self.lox = lox_instance
        self.source = source
        self.tokens: list[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1

    def scan_tokens(self) -> list[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scan_token(self):
        c = self.advance()
        if   c == "(": self.add_token(TokenType.LEFT_PAREN)
        elif c == ")": self.add_token(TokenType.RIGHT_PAREN)
        elif c == "{": self.add_token(TokenType.LEFT_BRACE)
        elif c == "}": self.add_token(TokenType.RIGHT_BRACE)
        elif c == ",": self.add_token(TokenType.COMMA)
        elif c == ".": self.add_token(TokenType.DOT)
        elif c == "-": self.add_token(TokenType.MINUS)
        elif c == "+": self.add_token(TokenType.PLUS)
        elif c == ";": self.add_token(TokenType.SEMICOLON)
        elif c == "*": self.add_token(TokenType.STAR)
        elif c == "!": self.add_token(TokenType.BANG_EQUAL    if self.match("=") else TokenType.BANG)
        elif c == "=": self.add_token(TokenType.EQUAL_EQUAL   if self.match("=") else TokenType.EQUAL)
        elif c == "<": self.add_token(TokenType.LESS_EQUAL    if self.match("=") else TokenType.LESS)
        elif c == ">": self.add_token(TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER)
        elif c == "/":
            if self.match("/"):
                # A comment goes until the end of the line.
                while self.peek() != "\n" and not self.is_at_end():
                    self.advance()
            else:
                self.add_token(TokenType.SLASH)
        
        elif  c == " " or c == "\r" or c == "\t":
            # Ignore whitespace.
            pass
        elif c == "\n":
            self.line += 1
        
        elif c == '"': self.string()

        else:
            if    self.is_digit(c): self.number()
            elif  self.is_alpha(c): self.identifier()
            else: self.lox.error(self.line, "Unexpected character.")

    def identifier(self):
        while self.is_alpha_numeric(self.peek()): self.advance()

        # See if the identifier is a reserved word.
        text = self.source[self.start:self.current]
        token_type = Scanner.keywords.get(text, TokenType.IDENTIFIER)
        self.add_token(token_type)

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n": self.line += 1
            self.advance()

        # Unterminated string.
        if self.is_at_end():
            self.lox.error(self.line, "Unterminated string.")
            return

        # The closing "
        self.advance()

        # Trim the surrounding quotes.
        value = self.source[self.start + 1:self.current - 1]
        self.add_token(TokenType.STRING, value)

    def number(self):
        while self.is_digit(self.peek()): self.advance()

        # Look for a fractional part.
        if self.peek() == "." and self.is_digit(self.peek_next()):
            # Consume the "."
            self.advance()

            while self.is_digit(self.peek()): self.advance()

        self.add_token(TokenType.NUMBER, float(self.source[self.start:self.current]))

    def match(self, expected: str) -> bool:
        if self.is_at_end():                      return False
        if self.source[self.current] != expected: return False

        self.current += 1
        return True
    
    def is_at_end(self) -> bool:
        return self.current >= len(self.source)
    
    def peek(self) -> str:
        if self.is_at_end(): return "\0"
        return self.source[self.current]

    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source): return "\0"
        return self.source[self.current + 1]

    def advance(self) -> str:
        self.current += 1
        return self.source[self.current - 1]
    
    def is_digit(self, c: str) -> bool:
        return c >= "0" and c <= "9"

    def is_alpha(self, c: str) -> bool:
        return (c >= "a" and c <= "z") or \
               (c >= "A" and c <= "Z") or \
                c == "_"

    def is_alpha_numeric(self, c: str) -> bool:
        return self.is_alpha(c) or self.is_digit(c)

    def add_token(self, token_type: TokenType, literal: object = None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))