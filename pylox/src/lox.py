from pathlib import Path
import sys

from scanner import Scanner
from my_parser import Parser
from my_token import Token
from token_type import TokenType
from ast_printer import AstPrinter

class Lox:
    hadError = False

    def main(self, args: list[str]):
        if len(args) > 1:
            print("Usage: lox [script]")
            sys.exit(64)
        elif len(args) == 1:
            self.runFile(args[0])
        else:
            self.runPrompt()

    def runFile(self, path: Path):
        with open(path) as f:
            self.run(f.read())

        if self.hadError:
            sys.exit(65)

    def runPrompt(self):
        try:
            while True:
                line = input("pylox > ")
                self.run(line)
                self.hadError = False
        except KeyboardInterrupt:
            print()
            sys.exit(0)

    def run(self, source: str):
        scanner = Scanner(self, source)
        tokens = scanner.scan_tokens()
        parser = Parser(self, tokens)
        expression = parser.parse()

        if self.hadError: return

        print(AstPrinter().print(expression))

    def error(self, line: int, msg: str, token: Token = None):
        if token is None:               self.report(line, "", msg)
        if token.type == TokenType.EOF: self.report(token.line, " at end", msg)
        else:                           self.report(token.line, f" at '{token.lexeme}'", msg)

    def report(self, line: int, where: str, msg: str):
        print(f"[line {line}] Error{where}: {msg}")
        self.hadError = True
