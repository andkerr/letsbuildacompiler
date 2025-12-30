from typing import TextIO
import sys


class Compiler:
    def __init__(self, src: str, output: TextIO = sys.stdout):
        self.src = src
        self.pos = 0
        self.look = ""
        self.output = output

        # 'Init' from the tutorial: prime the parser by calling get_char.
        self.get_char()
        self.skip_white()

    def get_char(self):
        if self.pos < len(self.src):
            self.look = self.src[self.pos]
            self.pos += 1
        else:
            self.look = ""  # End of input

    def is_whitespace(self, c: str) -> bool:
        return c in (" ", "\t")

    def skip_white(self):
        while self.is_whitespace(self.look):
            self.get_char()

    def abort(self, msg: str):
        raise Exception(f"Error: {msg}")

    def expected(self, s: str):
        self.abort(f"{s} expected")

    def match(self, x: str):
        if self.look == x:
            self.get_char()
            self.skip_white()
        else:
            self.expected(f"'{x}'")

    def get_name(self) -> str:
        token = ""
        if not self.look.isalpha():
            self.expected("Name")
        while self.look.isalnum():
            token += self.look.upper()
            self.get_char()
        self.skip_white()
        return token

    def get_num(self) -> str:
        value = ""
        if not self.look.isdigit():
            self.expected("Integer")
        while self.look.isdigit():
            value += self.look
            self.get_char()
        self.skip_white()
        return value

    def is_addop(self, c: str) -> bool:
        return c in ("+", "-")

    def is_mulop(self, c: str) -> bool:
        return c in ("*", "/")

    def emit(self, s: str):
        self.output.write("    " + s)

    def emit_ln(self, s: str):
        self.emit(s + "\n")

    def ident(self):
        name = self.get_name()
        if self.look == "(":
            self.match("(")
            self.match(")")
            self.emit_ln(f"call ${name}")
        else:
            self.emit_ln(f"local.get ${name}")

    def assignment(self):
        name = self.get_name()
        self.match("=")
        self.emit_ln(f"(local ${name} i32)")
        self._expression()
        self.emit_ln(f"local.set ${name}")

    def factor(self):
        if self.look == "(":
            self.match("(")
            self._expression()
            self.match(")")
        elif self.look.isalpha():
            self.ident()
        else:
            self.emit_ln(f"i32.const {self.get_num()}")

    def multiply(self):
        self.match("*")
        self.factor()
        self.emit_ln("i32.mul")

    def divide(self):
        self.match("/")
        self.factor()
        self.emit_ln("i32.div_s")

    def term(self):
        self.factor()
        while self.is_mulop(self.look):
            if self.look == "*":
                self.multiply()
            elif self.look == "/":
                self.divide()

    def add(self):
        self.match("+")
        self.term()
        self.emit_ln("i32.add")

    def subtract(self):
        self.match("-")
        self.term()
        self.emit_ln("i32.sub")

    def _expression(self):
        if self.is_addop(self.look): # handle unary +,-
            self.emit_ln("i32.const 0")
        else:
            self.term()
        while self.is_addop(self.look):
            if self.look == "+":
                self.add()
            elif self.look == "-":
                self.subtract()

    def expression(self):
        self._expression()
        if self.look not in ("\n", ""):
            self.expected("EOF or newline")


if __name__ == "__main__":
    import myutils
    myutils.compile_stdin(Compiler)
