"""Edit check: what changed between two versions of one script, and the usual breakages.
usage: python3 tools/check.py <old.py> <new.py>
Reports: syntax, functions removed / added / changed, a function defined twice (the later one wins silently),
new undefined names (pyflakes), and whether VERSION changed. Exit code 1 if something is broken."""
import ast, sys, hashlib, subprocess

def inv(path):
    src = open(path, encoding="utf-8").read()
    t = ast.parse(src)                     # raises on a syntax error
    L = src.splitlines(); fns = {}; dups = []; version = None
    for n in t.body:
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
            txt = "\n".join(L[n.lineno - 1 - len(n.decorator_list):n.end_lineno])
            if n.name in fns: dups.append(n.name)
            fns[n.name] = hashlib.md5(txt.encode()).hexdigest()
        if isinstance(n, ast.Assign) and any(isinstance(x, ast.Name) and x.id == "VERSION" for x in n.targets):
            try: version = ast.literal_eval(n.value)
            except Exception: pass
    return fns, dups, version

def data_names(path):
    """Names the script's Data file defines (Data/<name>_data.py beside the script, read by bergama_data())."""
    import os, re
    m = re.search(r'"Data", "(\w+_data\.py)"', open(path, encoding="utf-8").read())
    if not m: return set()
    f = os.path.join(os.path.dirname(os.path.abspath(path)), "Data", m.group(1))
    if not os.path.isfile(f):
        print("BROKEN? its data file is not beside it:", f); return set()
    t = ast.parse(open(f, encoding="utf-8").read())
    return {x.id for n in t.body if isinstance(n, ast.Assign) for x in n.targets if isinstance(x, ast.Name)}

def undefined(path):
    r = subprocess.run([sys.executable, "-m", "pyflakes", path], capture_output=True, text=True)
    skip = {"'ghenv'"} | {"'%s'" % n for n in data_names(path)}
    return {ln.split(": ", 1)[1] for ln in r.stdout.splitlines() if "undefined name" in ln and ln.rsplit(" ", 1)[-1] not in skip}

old, new = sys.argv[1], sys.argv[2]
bad = False
try:
    fo, do, vo = inv(old); fn, dn, vn = inv(new)
except SyntaxError as e:
    print("BROKEN: syntax error", e); sys.exit(1)
rem = sorted(set(fo) - set(fn)); add = sorted(set(fn) - set(fo))
chg = sorted(k for k in set(fo) & set(fn) if fo[k] != fn[k])
print("functions: %d -> %d" % (len(fo), len(fn)))
print("removed :", ", ".join(rem) or "-")
print("added   :", ", ".join(add) or "-")
print("changed :", ", ".join(chg) or "-")
if dn:
    print("BROKEN? defined twice (later wins):", ", ".join(dn)); bad = True
u = undefined(new) - undefined(old)
if u:
    print("BROKEN? new undefined names:", "; ".join(sorted(u))); bad = True
print("VERSION :", vo, "->", vn, "" if vo != vn else "(UNCHANGED: bump it for a new version)")
sys.exit(1 if bad else 0)
