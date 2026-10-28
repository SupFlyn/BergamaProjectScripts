"""Refresh the line numbers in the project's SCRIPT_MAP.md (library/SCRIPT_MAP.md: which script draws which drawing).
usage: python3 tools/script_map.py [path to SCRIPT_MAP.md]     (default: /mnt/project-files/library/SCRIPT_MAP.md)
tools/build.py calls it after every build, so the line numbers follow every new version.
It only reads text (no script is run). In each section that starts with a line `<!-- script: <src folder> -->`, every
`name()` in backticks is looked up as a top-level def/class of that script, and the block between
`<!-- lines: <src folder> -->` and `<!-- /lines -->` is rewritten: src part file + lines, delivered file + lines.
Everything else in the file is left as written."""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT = "/mnt/project-files/library/SCRIPT_MAP.md"


def defs(path):
    """{name: [(start, end), ...]} of the top-level defs/classes in a file (end = last line of its body)."""
    L = open(path, encoding="utf-8").read().split("\n")
    out, cur = {}, None
    for i, ln in enumerate(L, 1):
        top = ln[:1] not in ("", " ", "\t", "#", ")", "]", "}", "@")
        if top and cur:
            j = i - 1
            while j > cur[1] and (not L[j - 1].strip() or L[j - 1].startswith("#")):
                j -= 1
            out.setdefault(cur[0], []).append((cur[1], j))
            cur = None
        m = re.match(r"(?:def|class) (\w+)", ln)
        if m:
            cur = (m.group(1), i)
    if cur:
        out.setdefault(cur[0], []).append((cur[1], len(L)))
    return out


def src_files(name):
    """code.py, its parts and the common helpers it includes, as (path relative to src/<name>/, absolute path)."""
    d = os.path.join(ROOT, "src", name)
    seen = []

    def walk(p):
        seen.append(p)
        for ln in open(p, encoding="utf-8").read().splitlines():
            m = re.match(r"#@include (\S+)", ln)
            if m:
                sub = os.path.normpath(os.path.join(os.path.dirname(p), m.group(1)))
                if os.sep + "data" + os.sep not in sub and sub not in seen:
                    walk(sub)
    walk(os.path.join(d, "code.py"))
    return [(os.path.relpath(p, d), p) for p in seen]


def table(name, wanted):
    target = open(os.path.join(ROOT, "src", name, "target.txt")).read().strip()
    dist = defs(os.path.join(ROOT, "dist", target))
    src = {}
    for rel, p in src_files(name):
        for k, v in defs(p).items():
            src.setdefault(k, []).extend((rel, a, b) for a, b in v)
    rows = ["| function | src/%s/ part : lines | %s : lines |" % (name, target), "|---|---|---|"]
    for fn in wanted:
        s, t = src.get(fn), dist.get(fn)
        if not s and not t:
            rows.append("| %s | NOT FOUND (renamed or removed: fix this map) | - |" % fn)
            continue
        sx = "%s : %d-%d" % s[-1] if s else "-"
        tx = "%d-%d" % t[-1] if t else "-"
        if t and len(t) > 1:
            tx += " (defined %dx, the last one counts)" % len(t)
        rows.append("| %s | %s | %s |" % (fn, sx, tx))
    return "\n".join(rows)


def refresh(path=DEFAULT):
    txt = open(path, encoding="utf-8").read()
    parts = re.split(r"(?m)^(?=<!-- script: )", txt)
    out = [parts[0]]
    for sec in parts[1:]:
        name = re.match(r"<!-- script: (\S+) -->", sec).group(1)
        body = re.sub(r"<!-- lines: \S+ -->.*?<!-- /lines -->", "", sec, flags=re.S)
        wanted = []
        for fn in re.findall(r"`(\w+)\(\)`", body):
            if fn not in wanted:
                wanted.append(fn)
        sec = re.sub(r"(<!-- lines: \S+ -->).*?(<!-- /lines -->)",
                     lambda m: m.group(1) + "\n" + table(name, wanted) + "\n" + m.group(2), sec, flags=re.S)
        out.append(sec)
    new = "".join(out)
    if new != txt:
        open(path, "w", encoding="utf-8").write(new)
    print("SCRIPT_MAP line numbers", "refreshed:" if new != txt else "unchanged:", path)


if __name__ == "__main__":
    refresh(sys.argv[1] if len(sys.argv) > 1 else DEFAULT)
