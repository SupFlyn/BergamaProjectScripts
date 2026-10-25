"""Join the source parts back into one self-contained script per folder: src/<name>/ -> dist/<target.txt>.
usage: python3 tools/build.py [name ...]      (no names = all). Also writes src/<name>/MAP.md (function -> line)."""
import os, re, sys

def expand(path, depth=0):
    out = []
    for ln in open(path, encoding="utf-8", newline="").read().splitlines(keepends=True):
        m = re.match(r"#@include (\S+)\n$", ln)
        if m:
            out.append(expand(os.path.normpath(os.path.join(os.path.dirname(path), m.group(1))), depth + 1))
        else:
            out.append(ln)
    return "".join(out)

def build(name):
    d = os.path.join("src", name)
    target = open(os.path.join(d, "target.txt")).read().strip()
    text = expand(os.path.join(d, "code.py"))
    os.makedirs("dist", exist_ok=True)
    out = os.path.join("dist", target)
    open(out, "w", encoding="utf-8", newline="").write(text)
    compile(text, out, "exec")   # syntax check
    # map: where each function is (code.py or the part that holds it)
    rows = ["# %s map (made by tools/build.py; edit the file named here)\n" % name, "| function / data | file | line |", "|---|---|---|"]
    def walk(path):
        for i, ln in enumerate(open(path, encoding="utf-8").read().splitlines(), 1):
            rel = os.path.relpath(path, d)
            m = re.match(r"(?:def|class) (\w+)", ln)
            if m: rows.append("| %s | %s | %d |" % (m.group(1), rel, i))
            m = re.match(r"#@include (\S+)", ln)
            if m:
                sub = os.path.normpath(os.path.join(os.path.dirname(path), m.group(1)))
                if "/parts/" in sub: walk(sub)
                else: rows.append("| %s | %s | - |" % (os.path.basename(sub)[:-3], os.path.relpath(sub, d)))
    walk(os.path.join(d, "code.py"))
    open(os.path.join(d, "MAP.md"), "w").write("\n".join(rows) + "\n")
    print("built", out, "(%d lines)" % text.count("\n"))
    return out

if __name__ == "__main__":
    names = sys.argv[1:] or sorted(n for n in os.listdir("src") if os.path.isfile(os.path.join("src", n, "target.txt")))
    for n in names: build(n)
