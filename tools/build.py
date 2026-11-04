"""Join the source parts back into one script per folder: src/<name>/ -> dist/<target.txt>.
usage: python3 tools/build.py [name ...]      (no names = all). Also writes src/<name>/MAP.md (function -> line).
Built-in data (the src/<name>/data/ parts) goes to dist/Data/<name>_data.py, which the script reads from
Downloads/Bergama/Data/ (Aras 25 Oct 21:29); src/<name>/INLINE_DATA keeps a script's data inside it instead."""
import os, re, sys, hashlib

LOADER = '''def bergama_data(name, _c={}):
    """Built-in data kept in Downloads/Bergama/Data/%(file)s (Aras 25 Oct 21:29, scripts shortened): runs its
    section `name` here, as if it were written in this place. The file is read once per run; a missing file or one
    from another version of this script stops the script with a message saying which file to copy."""
    import os as _os, hashlib as _hl
    if not _c:
        p_ = _os.path.join(_os.path.expanduser("~"), "Downloads", "Bergama", "Data", "%(file)s")
        if not _os.path.isfile(p_):
            raise RuntimeError("Data file missing: copy %(file)s from the run kit's Data folder into " + _os.path.dirname(p_))
        with open(p_, encoding="utf-8", newline="") as f_:
            for part_ in f_.read().split("\\n#@@ ")[1:]:
                k_, _, b_ = part_.partition("\\n")
                _c[k_] = b_
    b_ = _c.get(name)
    if b_ is None or _hl.md5(b_.encode("utf-8")).hexdigest() != %(md5)r.get(name):
        raise RuntimeError("Data file %(file)s is not the one made with this script version (part " + name +
                           "): copy it again from the same run kit as the script")
    exec(compile(b_, "%(file)s:" + name, "exec"), globals())


'''

def expand(path, depth=0, data=None):
    """The file with its includes put in. With `data` (a dict), data/ parts are collected there and replaced by a
    bergama_data() call instead."""
    out = []
    for ln in open(path, encoding="utf-8", newline="").read().splitlines(keepends=True):
        m = re.match(r"#@include (\S+)\n$", ln)
        if m:
            sub = os.path.normpath(os.path.join(os.path.dirname(path), m.group(1)))
            if data is not None and os.sep + "data" + os.sep in sub:
                nm = os.path.basename(sub)[:-3]
                data[nm] = open(sub, encoding="utf-8", newline="").read()
                out.append("\x00LOADER\x00" if len(data) == 1 else "")
                out.append('bergama_data("%s")\n' % nm)
            else:
                out.append(expand(sub, depth + 1, data))
        else:
            out.append(ln)
    return "".join(out)


def data_file(name, data):
    """dist/Data/<name>_data.py: one section per data part, and the md5 of each section as the loader reads it."""
    txt = "# Built-in data of %s (made by tools/build.py from src/%s/data/; do not edit by hand)\n" % (name, name)
    for nm, body in data.items():
        if "\n#@@ " in body:
            sys.exit("data part %s/%s holds the section marker" % (name, nm))
        txt += "\n#@@ " + nm + "\n" + body
    md5 = {}
    for part in txt.split("\n#@@ ")[1:]:          # exactly as the loader splits it
        k, _, b = part.partition("\n")
        md5[k] = hashlib.md5(b.encode("utf-8")).hexdigest()
    return txt, md5


def build(name):
    d = os.path.join("src", name)
    target = open(os.path.join(d, "target.txt")).read().strip()
    data = None if os.path.isfile(os.path.join(d, "INLINE_DATA")) else {}
    text = expand(os.path.join(d, "code.py"), data=data)
    os.makedirs("dist", exist_ok=True)
    out = os.path.join("dist", target)
    if data:
        fn = name + "_data.py"
        txt, md5 = data_file(name, data)
        os.makedirs(os.path.join("dist", "Data"), exist_ok=True)
        open(os.path.join("dist", "Data", fn), "w", encoding="utf-8", newline="").write(txt)
        text = text.replace("\x00LOADER\x00", LOADER % dict(file=fn, md5=md5))
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
    # the line numbers in the project's SCRIPT_MAP.md (which function draws which drawing) follow the new build
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import script_map
    p = os.environ.get("BERGAMA_SCRIPT_MAP", script_map.DEFAULT)
    if os.path.isfile(p):
        try:
            script_map.refresh(p)
        except Exception as e:
            print("SCRIPT_MAP not refreshed (%s): run python3 tools/script_map.py and fix the map" % e)
    else:
        print("SCRIPT_MAP not found at", p)
