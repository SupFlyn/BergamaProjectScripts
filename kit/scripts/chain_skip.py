# chain_skip.py v1 (Aras 15 Nov 2026 19:48 UTC: "optimize the scripts to be much much faster"; items 1 + 3)
# A helper for the chain runner, run OUTSIDE Rhino with the normal Python (py -3 chain_skip.py ...), from
# Downloads/Bergama/scripts. It never runs or changes a drawing script; it only says whether a step can be left out.
#
#   py -3 chain_skip.py check <script.py>      prints "SKIP ..." (inputs unchanged since its last good run) or "RUN ..."
#   py -3 chain_skip.py mark <script.py>       after a good run: stores the key (refused if the log starts with ERROR / RUNNING)
#   py -3 chain_skip.py alongside <script.py>  prints "YES ..." when it may run in Rhino while AcBuild's Archicad part runs
#   py -3 chain_skip.py forget [<script.py>]   deletes the stored key(s): the next check says RUN
#
# The key = sha1 of: the script file itself; every library script it loads (newest bergama_<family>_v*.py), every
# Data file / folder and every cached/<folder> whose name appears in its code or in the code it loads (size + time of
# each file); its kit/scripts/script_reads.txt lines; the 3dm. The key is taken AFTER the run, so a script's own
# outputs are in it. Scripts that talk to Archicad (Tapir) or capture views always RUN. Any doubt -> RUN.
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                        # Downloads/Bergama
KEYS = os.path.join(ROOT, "cached", "_chain")
ALWAYS = ("bergama_acbuild", "bergama_perspectives", "bergama_sections_ac")   # Archicad / view state is not in files
AC_READS = ("bergama_mapbase", "bergama_masterplanbase", "bergama_sections", "bergama_perspectives",
            "bergama_basemap", "bergama_archicad")  # AcBuild reads these (or writes bergama_archicad) while it runs


def family(name):
    return re.sub(r"_v\d+(_\d+)*\.py$", "", os.path.basename(name))


def newest(fam):
    fs = [f for f in os.listdir(HERE) if f.startswith(fam + "_v") and f.endswith(".py") and family(f) == fam]
    return os.path.join(HERE, max(fs, key=lambda p: [int(n) for n in re.findall(r"\d+", p)])) if fs else None


def text(p):
    try:
        with open(p, encoding="utf-8", errors="replace") as f:
            return f.read()
    except Exception:
        return u""


def deps(script):
    """(code files, Data entries, cached folders) the script may read, found by name in its code and the code it loads"""
    data = os.listdir(os.path.join(ROOT, "Data")) if os.path.isdir(os.path.join(ROOT, "Data")) else []
    cached = os.listdir(os.path.join(ROOT, "cached")) if os.path.isdir(os.path.join(ROOT, "cached")) else []
    code, todo, dset, cset = [], [script], set(), set()
    while todo:
        p = todo.pop()
        if p in code:
            continue
        code.append(p)
        t = text(p)
        for fam in set(re.findall(r"(bergama_[a-z0-9_]+?)_v\*", t)):
            q = newest(fam)
            if q and q not in code:
                todo.append(q)
        for d in data:
            if re.search(r"(?<![A-Za-z0-9_])%s(?![A-Za-z0-9_])" % re.escape(d), t):
                dset.add(d)
                if d.endswith(".py"):
                    todo.append(os.path.join(ROOT, "Data", d))
        for c in cached:
            if c != "_chain" and re.search(r"(?<![A-Za-z0-9_])%s(?![A-Za-z0-9_])" % re.escape(c), t):
                cset.add(c)
    return code, sorted(dset), sorted(cset)


def stamp(path, out):
    if os.path.isfile(path):
        st = os.stat(path)
        out.append([os.path.relpath(path, ROOT), st.st_size, st.st_mtime_ns])
    elif os.path.isdir(path):
        for dp, dn, fn in os.walk(path):
            dn.sort()
            for f in sorted(fn):
                stamp(os.path.join(dp, f), out)
    else:
        out.append([os.path.relpath(path, ROOT), None, None])


def reads(fam):
    out = []
    for ln in text(os.path.join(HERE, "script_reads.txt")).splitlines():
        if ln.startswith(fam + ":"):
            out.append(ln.split(":", 1)[1].split("#")[0].strip())
    return out


def key(script):
    code, dset, cset = deps(script)
    h = hashlib.sha1()
    for p in code:
        with open(p, "rb") as f:
            h.update(os.path.basename(p).encode("utf-8") + b"\0" + f.read())
    st = []
    for d in dset:
        stamp(os.path.join(ROOT, "Data", d), st)
    for c in cset:
        stamp(os.path.join(ROOT, "cached", c), st)
    for r in reads(family(script)):
        if r == "rhino":
            for f in os.listdir(ROOT):
                if f.lower().endswith(".3dm"):
                    stamp(os.path.join(ROOT, f), st)
        elif r:
            stamp(os.path.join(ROOT, r.rstrip("/")), st)
    h.update(json.dumps(st, sort_keys=True).encode("utf-8"))
    return h.hexdigest(), code, dset, cset


def log_of(script):
    m = re.search(r'^LOG_NAME\s*=\s*"([^"]+)"', text(script), re.M)
    return os.path.join(ROOT, "logs", m.group(1)) if m else None


def kpath(script):
    return os.path.join(KEYS, family(script) + ".key")


def main(a):
    if len(a) < 1 or a[0] not in ("check", "mark", "alongside", "forget"):
        print(__doc__ or "usage: check | mark | alongside | forget <script.py>")
        return 2
    if a[0] == "forget":
        fs = [kpath(a[1])] if len(a) > 1 else [os.path.join(KEYS, f) for f in os.listdir(KEYS)] if os.path.isdir(KEYS) else []
        for f in fs:
            if os.path.isfile(f):
                os.remove(f)
        print("forgot %d key(s)" % len(fs))
        return 0
    s = a[1] if os.path.isabs(a[1]) else os.path.join(HERE, a[1])
    if not os.path.isfile(s):
        print("RUN: %s not found" % s)
        return 1
    fam = family(s)
    t = text(s)
    if a[0] == "alongside":
        code, dset, cset = deps(s)
        bad = [c for c in cset if c in AC_READS]
        out_ = re.search(r'^OUT_FOLDER\s*=\s*"([^"]+)"', t, re.M)
        if fam in ALWAYS or "19723" in t or "Tapir" in t:
            print("NO: %s talks to Archicad" % fam)
        elif out_ and out_.group(1) in AC_READS:
            print("NO: %s writes cached/%s, which AcBuild reads" % (fam, out_.group(1)))
        elif "bergama_archicad" in cset:
            print("NO: %s reads cached/bergama_archicad (AcBuild writes it)" % fam)
        elif any(family(p) in ("bergama_mapbase", "bergama_masterplanbase", "bergama_basemap") and family(p) == fam
                 for p in code):
            print("NO: %s rebuilds a cache AcBuild reads" % fam)
        else:
            print("YES: %s reads %s; none is written by AcBuild" % (fam, ", ".join(cset) or "no cache"))
        return 0
    lg = log_of(s)
    if a[0] == "mark":
        if fam in ALWAYS:
            print("not marked: %s always runs" % fam)
            return 0
        head = text(lg)[:200] if lg else u""
        if not lg or not head or head.startswith(("ERROR", "RUNNING")):
            print("not marked: log %s missing, ERROR or RUNNING" % lg)
            return 1
        k = key(s)[0]
        os.makedirs(KEYS, exist_ok=True)
        with open(kpath(s), "w", encoding="utf-8") as f:
            json.dump({"key": k, "script": os.path.basename(s)}, f)
        print("marked %s" % os.path.basename(s))
        return 0
    # check
    if fam in ALWAYS or "19723" in t or "Tapir" in t:
        print("RUN: %s talks to Archicad or captures views (state outside files)" % fam)
        return 1
    if not lg or not os.path.isfile(lg) or text(lg)[:200].startswith(("ERROR", "RUNNING")):
        print("RUN: no good log from the last run")
        return 1
    try:
        with open(kpath(s), encoding="utf-8") as f:
            old = json.load(f)
    except Exception:
        print("RUN: no stored key (first run with chain_skip)")
        return 1
    out_ = re.search(r'^OUT_FOLDER\s*=\s*"([^"]+)"', t, re.M)
    if out_ and not any(os.path.isdir(os.path.join(ROOT, w, out_.group(1))) for w in ("output", "cached")):
        print("RUN: its output folder %s is gone" % out_.group(1))
        return 1
    k, code, dset, cset = key(s)
    if old.get("key") == k and old.get("script") == os.path.basename(s):
        print("SKIP: %s inputs unchanged since its last good run (code %d file(s), Data %d, cached %d)" % (
            os.path.basename(s), len(code), len(dset), len(cset)))
        return 0
    print("RUN: %s or one of its inputs changed" % os.path.basename(s))
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
