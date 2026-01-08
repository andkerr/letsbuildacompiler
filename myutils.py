import io
import sys

module_start = r"""
(module
  (func (export "main") (result i32)
""".lstrip()

module_end = r"""
  )
)
"""

def slurp_stdin() -> str:
    return "\n".join(line.strip() for line in sys.stdin)


def compile_stdin(Compiler: type, do_prog = lambda c: c.expression()) -> None:
    src = "".join(line.rstrip() for line in sys.stdin)
    print(module_start)
    compiler = Compiler(src)
    do_prog(compiler)
    print(module_end)
