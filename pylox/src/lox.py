from pathlib import Path
import sys

from scanner import Scanner
from my_parser import Parser
from resolver import Resolver
from interpreter import Interpreter
from my_token import Token
from token_type import TokenType
from runtime_error import RuntimeError

class Lox:
    def __init__(self):
        self.interpreter = Interpreter(self)
        self.had_error = False
        self.had_runtime_error = False

    def main(self, args: list[str]):
        if len(args) > 1:
            print("Usage: lox [script]")
            sys.exit(64)
        elif len(args) == 1:
            self.runFile(args[0])
        else:
            self.runPrompt()

    def runFile(self, path: Path):
        with open(path) as f: self.run(f.read())
        
        if self.had_error:         sys.exit(65)
        if self.had_runtime_error: sys.exit(70)

    def runPrompt(self):
        while True:
            try:
                line = input("pylox > ")
                self.run(line)
                self.had_error = False
            except KeyboardInterrupt:
                print()
                sys.exit(0)
            except RuntimeError as e:
                self.runtime_error(e)

    def run(self, source: str):
        scanner = Scanner(self, source)
        tokens = scanner.scan_tokens()
        parser = Parser(self, tokens)
        statements = parser.parse()

        if self.had_error: return

        resolver = Resolver(self.interpreter)
        resolver.resolve(statements)

        if self.had_error: return

        self.interpreter.interpret(statements)

    def error(self, line: int, msg: str, token: Token = None):
        if token is None:               self.report(line, "", msg)
        if token.type == TokenType.EOF: self.report(token.line, " at end", msg)
        else:                           self.report(token.line, f" at '{token.lexeme}'", msg)

    def runtime_error(self, error: RuntimeError):
        print(error)
        self.had_runtime_error = True

    def report(self, line: int, where: str, msg: str):
        print(f"[line {line}] Error{where}: {msg}")
        self.had_error = True
