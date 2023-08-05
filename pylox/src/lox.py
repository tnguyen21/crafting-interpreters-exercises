from pathlib import Path
import sys

from scanner import Scanner


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

        for token in tokens:
            print(token)

    def error(self, line: int, msg: str):
        self.report(line, "", msg)

    def report(self, line: int, where: str, msg: str):
        print(f"[line {line}] Error{where}: {msg}")
        self.hadError = True
