"""Move the older "NEW IN vN" notes of a script's header docstring into src/<name>/HISTORY.md (newest one stays).
usage: python3 tools/move_history.py src/<name>/<file with the header>   (no effect on what the script does)"""
import sys, re, os
p = sys.argv[1]; name = p.split(os.sep)[1]
L = open(p, encoding="utf-8", newline="").read().split("\n")
import ast
doc = ast.parse("\n".join(L)).body[0]                                   # the header docstring (first statement)
o, end = doc.lineno - 1, doc.end_lineno - 1
head = re.compile(r"^(NEW IN v|[A-Z][A-Z0-9'()/,:+.\- ]{3,}(\s|$|\())")
starts = [i for i in range(o, end) if L[i].startswith("NEW IN v")]
blocks = []
for s in starts[1:]:                                                      # keep the newest note in place
    e = s + 1
    while e < end and e not in starts and not (L[e - 1].strip() == "" and head.match(L[e]) and not L[e].startswith(" ")):
        e += 1
    blocks.append((s, e))
if not blocks: sys.exit("nothing to move in " + p)
moved = []
for s, e in reversed(blocks):
    moved.insert(0, "\n".join(L[s:e]).rstrip() + "\n")
    del L[s:e]
first = starts[1] if len(starts) > 1 else None
note = "OLDER VERSIONS: their notes are in HISTORY.md (repo SupFlyn/BergamaProjectScripts, src/%s/)." % name
L.insert(blocks[0][0], note + "\n")
open(p, "w", encoding="utf-8", newline="").write("\n".join(L))
hp = os.path.join("src", name, "HISTORY.md")
old = open(hp, encoding="utf-8").read() if os.path.isfile(hp) else "# %s: notes of older versions (moved out of the script header)\n\n" % name
open(hp, "w", encoding="utf-8").write(old + "\n".join(moved))
print(p, "moved", len(blocks), "notes,", sum(len(m) for m in moved), "chars")
