import io
import sys

module_template = r"""
(module
  (func (export "main") (result i32)
{instrs}
  )
)
""".lstrip()


def compile_stdin(Compiler: type) -> None:
    src = "".join(line.rstrip() for line in sys.stdin)
    output = io.StringIO()
    compiler = Compiler(src, output=output)
    compiler.expression()
    instrs = output.getvalue()
    full_code = module_template.format(instrs=instrs)
    print(full_code)
