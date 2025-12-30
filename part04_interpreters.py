from typing import TextIO
import sys


# The interpreter doesn't emit code, it executes it directly. Here, output
# refers to the stdout used for the ! (output) command. inp refers to stdin
# used for the ? (input) command.
class Interpreter:
    def __init__(
        self, src: str, input: TextIO = sys.stdin, output: TextIO = sys.stdout
    ):
        self.src = src
        self.pos = 0
        self.look = ""
        self.input = input
        self.output = output

        # Table for holding variable values. Unassigned variables default to 0.
        self.table = {}

        self.get_char()
        self.skip_white()

    def get_char(self):
        if self.pos < len(self.src):
            self.look = self.src[self.pos]
            self.pos += 1
        else:
            self.look = ""  # End of input

    def abort(self, msg: str):
        raise Exception(f"Error: {msg}")

    def expected(self, s: str):
        self.abort(f"{s} expected")

    def skip_white(self):
        while self.look.isspace():
            self.get_char()

    def match(self, x: str):
        if self.look == x:
            self.get_char()
            self.skip_white()
        else:
            self.expected(f"'{x}'")

    def get_name(self) -> str:
        if not self.look.isalpha():
            self.expected("Name")
        name = ""
        while self.look.isalnum():
            name += self.look.upper()
            self.get_char()
        self.skip_white()
        return name

    def get_num(self) -> int:
        pass

    def is_addop(self, c: str) -> bool:
        return c in ("+", "-")

    def is_mulop(self, c: str) -> bool:
        return c in ("*", "/")

    def ident(self):
        pass

    def factor(self) -> int:
        pass

    def term(self) -> int:
        pass

    def expression(self) -> int:
        pass

    def assignment(self):
        pass

    def interpret(self):
        pass
