from tests import wasm_util
import sys

code = "".join(line.rstrip() for line in sys.stdin)
if code == "":
    print("Error: empty input", file=sys.stderr)
    sys.exit(1)
print(wasm_util.run_wasm(code))
