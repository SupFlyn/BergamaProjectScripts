"""Top-level functions/classes the script can never reach from its top-level code (references followed transitively).
usage: python3 tools/deadcode.py <script.py>   Names that appear anywhere inside a string (getattr, globals(), embedded engines such as DIAG_SRC) count as used."""
import ast, sys, re
src = open(sys.argv[1], encoding="utf-8").read(); t = ast.parse(src)
defs = {n.name: n for n in t.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
def names(node):
    out = set()
    for x in ast.walk(node):
        if isinstance(x, ast.Name): out.add(x.id)
        elif isinstance(x, ast.Attribute): out.add(x.attr)
        elif isinstance(x, ast.Constant) and isinstance(x.value, str):
            out.update(re.findall(r"[A-Za-z_]\w*", x.value))
    return out
seen = set(); todo = set()
for n in t.body:
    if not isinstance(n, (ast.FunctionDef, ast.ClassDef)): todo |= names(n)
    else:
        for d in getattr(n, "decorator_list", []): todo |= names(d)
while todo:
    k = todo.pop()
    if k in defs and k not in seen:
        seen.add(k); todo |= names(defs[k])
dead = [k for k in defs if k not in seen]
L = src.splitlines()
tot = sum(defs[k].end_lineno - defs[k].lineno + 1 for k in dead)
print("%d of %d top-level defs unreachable, %d lines:" % (len(dead), len(defs), tot), ", ".join(dead))
