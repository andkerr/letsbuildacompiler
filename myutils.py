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


def compile_stdin(Compiler: type) -> None:
    src = "".join(line.rstrip() for line in sys.stdin)
    print(module_start)
    compiler = Compiler(src)
    compiler.expression()
    print(module_end)
