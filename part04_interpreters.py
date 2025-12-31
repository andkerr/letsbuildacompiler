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
        num = ""
        if not self.look.isdigit():
            self.expected("Digit")
        while self.look.isdigit():
            num += self.look
            self.get_char()
        self.skip_white()
        return int(num)

    def is_addop(self, c: str) -> bool:
        return c in ("+", "-")

    def is_mulop(self, c: str) -> bool:
        return c in ("*", "/")

    def ident(self):
        name = self.get_name()
        return int(self.table.get(name, 0))

    # <factor> ::= <number>
    #              "(" <expression> ")"
    def factor(self) -> int:
        if self.look == "(":
            self.match("(")
            value = self.expression()
            self.match(")")
        elif self.look.isalpha():
            value = self.ident()
        else:
            value = self.get_num()
        return value

    # <term> ::= <factor> [ <mulop> <factor> ]*
    def term(self) -> int:
        value = self.factor()
        while self.is_mulop(self.look):
            if self.look == "*":
                self.match("*")
                value *= self.factor()
            elif self.look == "/":
                self.match("/")
                value //= self.factor()
        return value

    # <expression> ::= [ <addop> ] <term> [ <addop> <term> ]*
    def expression(self) -> int:
        if self.is_addop(self.look):
            value = 0
        else:
            value = self.term()
        while self.is_addop(self.look):
            if self.look == "+":
                self.match("+")
                value += self.term()
            elif self.look == "-":
                self.match("-")
                value -= self.term()
        return value

    def assignment(self):
        name = self.get_name()
        self.match("=")
        self.table[name] = self.expression()

    def interpret(self):
        while self.look != ".":
            if self.look == "?":
                self.match("?")
                self.table[self.get_name()] = self.input.readline()
            elif self.look == "!":
                self.match("!")
                value = self.ident()
                self.output.write(f"{value}")
            else:
                self.assignment()


if __name__ == "__main__":
    import myutils
    interp = Interpreter(myutils.slurp_stdin())
    print(interp.expression())
