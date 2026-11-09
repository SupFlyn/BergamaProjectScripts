# ---- Bergama folders (Aras 24 Oct 08:28 + 27 Oct 11:07; SCRIPT_STANDARD §9). Every script uses ONLY these. ----
#   Downloads/Bergama/output/<name>/          final PDFs only
#   Downloads/Bergama/logs/                    every log file and log folder
#   Downloads/Bergama/cached/<name>/           caches, results other scripts read, any other working file
#   Downloads/Bergama/cached/booklet/<name>/   the script's booklet assets (blocks.json, results, images);
#                                              the booklet's own leftovers in cached/booklet/
BERGAMA_ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")


def bg_output(name):
    return os.path.join(BERGAMA_ROOT, "output", name)


def bg_cache(name):
    return os.path.join(BERGAMA_ROOT, "cached", name)


def bg_booklet(name):
    return os.path.join(BERGAMA_ROOT, "cached", "booklet", name)


def bg_logs(*sub):
    return os.path.join(BERGAMA_ROOT, "logs", *sub)


def bg_first(paths):
    """The first path that exists (new place first, then where older versions wrote it), else the first."""
    for p in paths:
        if os.path.exists(p):
            return p
    return paths[0]


def bg_out_dir(name):
    """round 5 (C2): output/<name>/ made only now, just before a file is written into it (a run that stops early, or a
    solve that never runs, leaves no empty folder). Returns the path."""
    p = bg_output(name)
    os.makedirs(p, exist_ok=True)
    return p


def bg_result(script, fn):
    """round 5 (C10): where another script's result file `fn` is: cached/<script>/fn, then cached/<script>/from_output/
    fn (moved there by bg_tidy_output), then output/<script>/fn (older versions); the first that exists, else the
    first path (shade_july.json was looked for in output/ after the site board had moved it to cached/)."""
    return bg_first([os.path.join(bg_cache(script), fn), os.path.join(bg_cache(script), "from_output", fn),
                     os.path.join(bg_output(script), fn)])


def bg_this_run(path):
    """round 5 (C10): (fresh, note) for a result file another script wrote: fresh = written at or after the start of
    this chain run (the Button press that started the chain, sticky "bergama_chain_t0" from trigger.py); note = a short
    log text ("this run 23:01" / "from an earlier run 22:40" / "missing" / "no chain start known"). A reader logs the
    note and, when not fresh, a WARNING (the value is from the run before: one press must give one answer)."""
    import time as _t
    if not os.path.isfile(path):
        return False, u"missing"
    m = os.path.getmtime(path)
    hm = _t.strftime("%d %b %H:%M", _t.localtime(m))
    try:
        import scriptcontext as _scx
        t0 = _scx.sticky.get("bergama_chain_t0")
    except Exception:
        t0 = None
    if t0 is None:
        return True, u"no chain start known (file of %s)" % hm
    if m + 1.0 >= t0:
        return True, u"this run %s" % hm
    return False, u"from an earlier run %s" % hm


def bg_tidy_output(name, cache_dir=None):
    """output/<name>/ keeps PDFs only: log files and anything in a log folder move to logs/<name>/, every other
    non-PDF file to cached/<name>/from_output/ (or cache_dir: the booklet uses cached/booklet/; moved, never deleted;
    same sub-folders). Empty folders go.
    Returns short log lines (counts, not one line per file)."""
    import shutil as _sh
    root, moved, fail = bg_output(name), {}, []
    if not os.path.isdir(root):
        return []
    for d, subs, files in os.walk(root, topdown=False):
        rel = os.path.relpath(d, root)
        rel = "" if rel == "." else rel
        for fn in files:
            if fn.lower().endswith(".pdf"):
                continue
            is_log = "log" in fn.lower() or any("log" in p.lower() for p in rel.split(os.sep) if p)
            dst = os.path.join(bg_logs(name) if is_log else (cache_dir or os.path.join(bg_cache(name), "from_output")), rel, fn)
            try:
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                if os.path.exists(dst):
                    os.remove(dst)
                _sh.move(os.path.join(d, fn), dst)
                top = bg_logs(name) if is_log else (cache_dir or os.path.join(bg_cache(name), "from_output"))
                moved[top] = moved.get(top, 0) + 1
            except Exception as ex:
                fail.append(u"%s (%s)" % (os.path.join(rel, fn), type(ex).__name__))
        if d != root:
            try:
                os.rmdir(d)                       # only when empty
            except Exception:
                pass
    return ([u"output/%s: %d non-PDF file(s) moved to %s" % (name, n, d) for d, n in sorted(moved.items())] +
            ([u"output/%s: could not move %s" % (name, ", ".join(fail[:5]))] if fail else []))
