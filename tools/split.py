"""Split delivered scripts into small source parts (code + data + common), so edits touch only small files.
usage: python3 tools/split.py <script.py> [<script.py> ...]     (run from the repo root)
Writes src/<name>/code.py, src/<name>/data/*.py, src/common/*.py, src/<name>/target.txt.
Round trip is checked: tools/build.py must give back the input byte for byte, or nothing is written."""
import ast, os, re, sys, hashlib, collections, shutil
DATA_MIN = 2000      # a top-level assignment this many characters or longer goes to data/
ROOT = os.getcwd()

def name_of(path):
    return re.sub(r"_v\d+(_\d+)*$", "", os.path.basename(path)[:-3])

def blocks(src):
    """top-level functions (with decorators) and big assignments: (kind, name, first line idx, last line idx)"""
    t = ast.parse(src); out = []
    for n in t.body:
        a = n.lineno - 1 - len(getattr(n, "decorator_list", []))
        if isinstance(n, ast.FunctionDef):
            out.append(("fn", n.name, a, n.end_lineno - 1))
        elif isinstance(n, (ast.Assign, ast.AnnAssign)):
            tg = n.targets[0] if isinstance(n, ast.Assign) else n.target
            nm = tg.id if isinstance(tg, ast.Name) else "assign_%d" % n.lineno
            out.append(("data", nm, a, n.end_lineno - 1))
    return out

def fn_text(lines, a, b):
    return "".join(lines[a:b + 1])

def main(paths):
    srcs = {p: open(p, encoding="utf-8", newline="").read() for p in paths}
    # functions with the exact same text in 2+ scripts -> common/
    seen = collections.defaultdict(collections.Counter)
    for p, s in srcs.items():
        L = s.splitlines(keepends=True)
        for k, nm, a, b in blocks(s):
            if k == "fn":
                seen[nm][hashlib.md5(fn_text(L, a, b).encode()).hexdigest()] += 1
    # the most used exact text of a function shared by 2+ scripts; scripts with another variant keep theirs inline
    common = {nm: c.most_common(1)[0][0] for nm, c in seen.items() if c.most_common(1)[0][1] >= 2}
    for p, s in srcs.items():
        name = name_of(p); d = os.path.join("src", name)
        L = s.splitlines(keepends=True); repl = {}
        parts = {}
        for k, nm, a, b in blocks(s):
            txt = fn_text(L, a, b)
            if k == "fn" and common.get(nm) == hashlib.md5(txt.encode()).hexdigest():
                parts[a] = (b, "#@include ../common/%s.py\n" % nm, os.path.join("src", "common", nm + ".py"), txt)
            elif k == "data" and len(txt) >= DATA_MIN and txt.endswith("\n"):
                parts[a] = (b, "#@include data/%s.py\n" % nm, os.path.join(d, "data", nm + ".py"), txt)
        code = []; i = 0; files = {}
        while i < len(L):
            if i in parts:
                b, inc, fp, txt = parts[i]
                if fp in files and files[fp] != txt:
                    sys.exit("two different blocks named %s in %s" % (fp, p))
                files[fp] = txt; code.append(inc); i = b + 1
            else:
                code.append(L[i]); i += 1
        # round trip in memory before writing anything
        back = []
        for ln in code:
            m = re.match(r"#@include (\S+)\n$", ln)
            back.append(files[os.path.normpath(os.path.join(d, m.group(1)))] if m else ln)
        if "".join(back) != s:
            sys.exit("round trip failed for " + p)
        if os.path.isdir(os.path.join(d, "data")):
            shutil.rmtree(os.path.join(d, "data"))
        for fp, txt in files.items():
            os.makedirs(os.path.dirname(fp), exist_ok=True)
            open(fp, "w", encoding="utf-8", newline="").write(txt)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "code.py"), "w", encoding="utf-8", newline="").write("".join(code))
        open(os.path.join(d, "target.txt"), "w").write(os.path.basename(p) + "\n")
        print("%-38s %6d lines -> code.py %5d lines, %d data parts, %d common" % (
            os.path.basename(p), len(L), len(code), sum(1 for f in files if "/data/" in f), sum(1 for f in files if "/common/" in f)))

if __name__ == "__main__":
    main(sys.argv[1:])
