"""Unreachable defs inside an embedded source string (e.g. DETAIL_SRC), with every name the host script uses as roots.
usage: python3 tools/deadcode_embedded.py <host.py> <VARNAME>"""
import ast, sys, re
host = open(sys.argv[1], encoding="utf-8").read(); var = sys.argv[2]
ht = ast.parse(host); emb = None
for n in ht.body:
    if isinstance(n, ast.Assign) and any(getattr(x, "id", None) == var for x in n.targets): emb = ast.literal_eval(n.value)
def names(node, strings=True):
    out = set()
    for x in ast.walk(node):
        if isinstance(x, ast.Name): out.add(x.id)
        elif isinstance(x, ast.Attribute): out.add(x.attr)
        elif strings and isinstance(x, ast.Constant) and isinstance(x.value, str):
            out.update(re.findall(r"[A-Za-z_]\w*", x.value))
    return out
roots = set()
for n in ht.body:
    if not (isinstance(n, ast.Assign) and any(getattr(x, "id", None) == var for x in n.targets)): roots |= names(n)
et = ast.parse(emb); defs = {n.name: n for n in et.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
todo = set(roots)
for n in et.body:
    if not isinstance(n, (ast.FunctionDef, ast.ClassDef)): todo |= names(n)
seen = set()
while todo:
    k = todo.pop()
    if k in defs and k not in seen: seen.add(k); todo |= names(defs[k])
dead = [k for k in defs if k not in seen]
print("%s: %d of %d defs unreachable, %d lines: %s" % (var, len(dead), len(defs), sum(defs[k].end_lineno - defs[k].lineno + 1 for k in dead), ", ".join(dead)))
