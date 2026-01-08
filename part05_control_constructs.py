from typing import TextIO
import sys


class Compiler:
    def __init__(self, src: str, output: TextIO = sys.stdout):
        self.src = src
        self.pos = 0
        self.look = ""
        self.output = output
        self.loopcount = 0

        # 'Init' from the tutorial: prime the parser by calling get_char.
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
        # Note: for part 5, we're back to only supporting single-letter names.
        if not self.look.isalpha():
            self.expected("Name")
        name = self.look.upper()
        self.get_char()
        self.skip_white()
        return name

    def get_num(self) -> str:
        # Note: for part 5, we're back to only supporting single-digit numbers.
        if not self.look.isdigit():
            self.expected("Integer")
        num = self.look
        self.get_char()
        self.skip_white()
        return num

    def emit(self, s: str):
        self.output.write("    " + s)

    def emit_ln(self, s: str):
        self.emit(s + "\n")

    def generate_loop_labels(self) -> dict[str, str]:
        pass

    def condition(self):
        pass

    def expression(self):
        pass

    def other(self):
        self.emit_ln(self.get_name())

    def block(self, breakloop_label: str = ""):
        while self.look != "e":
            self.other()

    def do_if(self, breakloop_label: str = ""):
        pass

    def do_while(self):
        pass

    def do_loop(self):
        pass

    def do_repeat(self):
        pass

    def do_do(self):
        pass

    def do_for(self):
        pass

    def do_break(self, breakloop_label: str):
        pass

    def do_program(self):
        self.block()
        if self.look != "e":
            self.expected("End")
        self.emit_ln("nop")

if __name__ == "__main__":
    import myutils
    myutils.compile_stdin(Compiler, lambda c: c.do_program())
