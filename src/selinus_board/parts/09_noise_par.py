def noise_par(NM, tasks, mode, label):
    """NM.column(*t) (mode "col") or NM.column_multi(*t) (mode "multi") for every task, in order, on the worker
    processes when that is possible and checked; in Rhino otherwise. The results are the same either way."""
    return noise_par_collect(noise_par_start(NM, tasks, mode, label))


# ------------------------------------------------------------ v18: worker processes for the one-core stages
# Rhino's Python runs one Python thread at a time, so stages written in plain Python (terrain heights, the section
# drawings) used one core in v17 however many the computer has. v18 hands them to worker processes: Rhino 8's own
# Python running THIS script's own code (everything above the main block, read from the component), so every number
# is made by the same code on the same Python and numpy. Each worker must report the same bytecode for every
# function, the same maths fingerprint and the same numpy as Rhino before it gets any work, and Rhino computes the
# first piece of every job itself and compares it bit for bit with the worker's. On any difference, error or missing
# piece the job is computed in Rhino as in v17 and the workers are not used again in that run (LOG says why).
PAR_POOL = True            # v18: worker processes for the one-core stages (False: in Rhino, as v17)
POOL_MIN_PTS = 60000       # v18: terrain heights of at least this many points go to the workers
POOL_START_S = 120.0       # v18: a worker that has not started within this many seconds: none are used
POOL_KEY = "\nLAYOUT = str(inp(\"layout\""        # the start of the main block: the workers run everything above it
_POOL = {}                 # this run's workers (filled by pool_start, emptied by pool_stop)
_POOL_DATA = {}            # data handed to the workers once per run (pool_share); in Rhino the same objects
_POOL_SHARE = {}           # key -> (version, the message that hands it over)
_NS_MOD = "selinus_ns"     # the module name the script's classes and functions are pickled under
_POOL_LOCK = _threading.Lock()

POOL_LAUNCHER = r'''
import sys, pickle, traceback


def _main():
    inp, out = sys.stdin.buffer, sys.stdout.buffer
    sys.stdout = sys.stderr                                # a print() in the code must not reach Rhino's pipe
    hdr = pickle.load(inp)
    for p in hdr["path"]:                                  # v44.1: Rhino's folders after this Python's own
        if p and p not in sys.path:
            sys.path.append(p)
    try:
        with open(hdr["src"], "r", encoding="utf-8") as fh:
            src = fh.read()
        ns = {"__name__": "selinus_worker"}
        exec(compile(src[:src.index(hdr["key"])], hdr["label"], "exec"), ns)
        b = pickle.dumps(("ok", ns["_pool_hello"]()), 4)
    except BaseException:
        b = pickle.dumps(("err", traceback.format_exc()), 4)
        out.write(b)
        out.flush()
        return
    out.write(b)
    out.flush()
    while True:
        try:
            msg = pickle.load(inp)
        except EOFError:
            return
        if msg[0] == "quit":
            return
        try:
            if msg[0] == "set":
                ns["_POOL_DATA"][msg[1]] = msg[2]
                r = None
            else:
                r = ns[msg[1]](*msg[2])
            b = pickle.dumps(("ok", r), 4)
        except BaseException:
            b = pickle.dumps(("err", traceback.format_exc()), 4)
        out.write(b)
        out.flush()


_main()
'''


def _ns_register(g=None):
    """Make the script's classes and functions picklable by name (module selinus_ns), in Rhino and in a worker alike.
    Only their __module__ label changes; what they do does not."""
    import sys, types
    g = globals() if g is None else g
    m = sys.modules.get(_NS_MOD)
    if m is None:
        m = sys.modules[_NS_MOD] = types.ModuleType(_NS_MOD)
    me = g.get("__name__")
    for k, v in list(g.items()):
        if isinstance(v, type) or type(v).__name__ == "function":
            if getattr(v, "__module__", None) in (me, _NS_MOD):
                try:
                    v.__module__ = _NS_MOD
                except Exception:
                    pass
                setattr(m, k, v)


def _code_print(g=None):
    """name -> fingerprint of the bytecode of every function and method of the script (the workers must match)."""
    import hashlib
    g = globals() if g is None else g
    out = {}

    def const_repr(k_):                                  # sets in sorted order (their order varies per process)
        if isinstance(k_, (frozenset, set)):
            return "{" + ",".join(sorted(const_repr(x) for x in k_)) + "}"
        if isinstance(k_, tuple):
            return "(" + ",".join(const_repr(x) for x in k_) + ")"
        return repr(k_)

    def code_fp(c, h):
        h.update(c.co_code)
        h.update(repr(c.co_names).encode("utf-8"))
        for k_ in c.co_consts:
            if hasattr(k_, "co_code"):
                code_fp(k_, h)
            else:
                h.update(const_repr(k_).encode("utf-8", "replace"))
    for k, v in list(g.items()):
        fs = []
        if type(v).__name__ == "function" and getattr(v, "__module__", None) in (g.get("__name__"), _NS_MOD):
            fs = [(k, v)]
        elif isinstance(v, type) and getattr(v, "__module__", None) in (g.get("__name__"), _NS_MOD):
            fs = [(k + "." + a, f) for a, f in sorted(vars(v).items()) if type(f).__name__ == "function"]
        for nm, f in fs:
            h = hashlib.sha1()
            code_fp(f.__code__, h)
            out[nm] = h.hexdigest()
    return out


def _pool_hello():
    """In a worker, once its code ran: what Rhino checks before handing it any work."""
    import sys
    _ns_register()
    return dict(code=_code_print(), probe=_math_probe(), py=sys.version,
                np=getattr(np, "__version__", None) if HAVE_NP else None)


def _component_text(obj):
    """The script text of a Grasshopper script component (as the render script reads it), or None."""
    f_ = getattr(obj, "TryGetSource", None)
    if callable(f_):
        try:
            r_ = f_()
            if isinstance(r_, tuple) and len(r_) == 2 and r_[0] and isinstance(r_[1], str):
                return r_[1]
            if isinstance(r_, str):
                return r_
        except Exception:
            pass
    for nm in ("Text", "Code", "ScriptSource", "SourceCode", "Script"):
        try:
            v_ = getattr(obj, nm, None)
        except Exception:
            v_ = None
        if isinstance(v_, str) and v_:
            return v_
        if v_ is not None and not isinstance(v_, str):
            for nm2 in ("Text", "Code"):
                t_ = getattr(v_, nm2, None)
                if isinstance(t_, str) and t_:
                    return t_
    for nm in dir(obj):                                  # any other text property that holds this script
        if nm.startswith("_") or not any(w in nm for w in ("Text", "Code", "Script", "Source", "Content")):
            continue
        try:
            v_ = getattr(obj, nm, None)
            if isinstance(v_, str) and POOL_KEY in v_:
                return v_
            for nm2 in dir(v_) if v_ is not None and not isinstance(v_, (str, bytes, int, float)) else ():
                if nm2.startswith("_") or not any(w in nm2 for w in ("Text", "Code", "Source")):
                    continue
                t_ = getattr(v_, nm2, None)
                if isinstance(t_, str) and POOL_KEY in t_:
                    return t_
        except Exception:
            pass
    return None


def _self_source():
    """This script's own text, for the workers: from the component, the file Rhino runs it from or the line cache."""
    cands = []
    s_ = globals().get("_SELINUS_SRC")
    if isinstance(s_, str):
        cands.append(s_)
    try:
        cands.append(_component_text(ghenv.Component))                 # noqa: F821
    except Exception:
        pass
    fn = _self_source.__code__.co_filename
    try:
        if fn and os.path.isfile(fn):
            with open(fn, "r", encoding="utf-8") as fh:
                cands.append(fh.read())
    except Exception:
        pass
    try:
        import linecache
        cands.append("".join(linecache.getlines(fn)))
    except Exception:
        pass
    for t in cands:
        if isinstance(t, str) and POOL_KEY in t and "def _pool_hello" in t:
            return t
    return None


def pool_allow(on=True):
    """Only selinus_board's own pipeline uses the workers (the render script, which runs this code, does not)."""
    _POOL["allow"] = bool(on)


def pool_start():
    """Start the workers (once per run). Returns the list of live workers ([] when they cannot be used)."""
    with _POOL_LOCK:
        if "w" not in _POOL:
            _pool_start()
    return _POOL["w"]


def _pool_start():
    import pickle, subprocess, sys, tempfile, hashlib, threading
    _POOL["w"], _POOL["why"], _POOL["n_jobs"] = [], "", 0
    if not _POOL.get("allow"):
        _POOL["why"] = "not used outside selinus_board's own run"
        return
    if not PAR_POOL:
        _POOL["why"] = "switched off (PAR_POOL = False)"
        return
    n = _cores() if PAR_PROCS <= 0 else int(PAR_PROCS)
    if n < 2:
        _POOL["why"] = "one core only (PAR_PROCS = 1 or a single-core computer)"
        return
    src = _self_source()
    if src is None:
        _POOL["why"] = "this component's code could not be read from Python here"
        return
    # v49.2 (Aras 28 Oct log: "SyntaxError ... line 630", the "+ \" line 315): the component's text has Windows line
    # ends; written in text mode each "\r\n" became "\r\r\n", read back as two lines, so every line doubled and a
    # line ending in "\" met an empty line. One "\n" per line now.
    src = src.replace("\r\n", "\n").replace("\r", "\n")
    py = noise_worker_python()
    if py is None:
        _POOL["why"] = _NOISE_PY.get("why", "") or "no python executable found beside Rhino"
        return
    procs = []
    try:
        d = os.path.join(tempfile.gettempdir(), "selinus_workers")
        if not os.path.isdir(d):
            os.makedirs(d)
        sf = os.path.join(d, "selinus_src_%s.py" % hashlib.sha1(src.encode("utf-8")).hexdigest()[:16])
        lf = os.path.join(d, "selinus_pool_%s.py" % hashlib.sha1(POOL_LAUNCHER.encode("utf-8")).hexdigest()[:12])
        for f_, t_ in ((sf, src), (lf, POOL_LAUNCHER)):
            if not os.path.isfile(f_):
                with open(f_ + ".tmp", "w", encoding="utf-8") as fh:
                    fh.write(t_)
                os.replace(f_ + ".tmp", f_)
        hdr = pickle.dumps(dict(path=[p for p in sys.path if isinstance(p, str)], src=sf, key=POOL_KEY,
                                label="selinus_board"), 4)
        for _ in range(n):
            pr = subprocess.Popen([py, "-I", lf], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=subprocess.DEVNULL, **_popen_kw())
            procs.append(pr)
            pr.stdin.write(hdr)
            pr.stdin.flush()
        _ns_register()
        mine = _code_print()
        want = dict(probe=_math_probe(), np=getattr(np, "__version__", None) if HAVE_NP else None)
        hello = [None] * len(procs)

        def read_hello(k, pr):
            try:
                hello[k] = pickle.load(pr.stdout)
            except Exception as ex_:
                hello[k] = ("err", "{}: {}".format(type(ex_).__name__, ex_))
        rd = [threading.Thread(target=read_hello, args=(k, pr), daemon=True) for k, pr in enumerate(procs)]
        for t_ in rd:
            t_.start()
        import time as _tm
        t_end = _tm.time() + POOL_START_S
        for t_ in rd:
            t_.join(max(0.1, t_end - _tm.time()))
        if any(h_ is None for h_ in hello):
            raise RuntimeError("a worker did not start within {:.0f} s".format(POOL_START_S))
        for st, info in hello:
            if st != "ok":
                tb_ = [l_.strip() for l_ in str(info).strip().splitlines() if l_.strip()]
                raise RuntimeError("a worker could not run the code: " + " | ".join(tb_[-4:])[:400])   # v44.1: file + line
            if info["probe"] != want["probe"] or info["np"] != want["np"]:
                raise RuntimeError("a worker's Python or numpy does not compute exactly like Rhino's")
            bad = [k for k, v in info["code"].items() if mine.get(k) != v]
            if bad or not info["code"]:
                raise RuntimeError("a worker's code differs from this component's ({} functions)".format(len(bad)))
    except Exception as ex:
        for pr in procs:
            try:
                pr.kill()
            except Exception:
                pass
        _POOL["why"] = "{}: {}".format(type(ex).__name__, ex)
        return
    import queue
    _POOL["q"] = queue.PriorityQueue()
    _POOL["seq"] = 0
    _POOL["lock"] = threading.Lock()
    for pr in procs:
        w = dict(proc=pr, sent={}, alive=True)
        w["thread"] = threading.Thread(target=_pool_io, args=(w,), daemon=True)
        w["thread"].start()
        _POOL["w"].append(w)


def _pool_io(w):
    """One thread per worker: takes the next piece of any job, sends it, waits for the result."""
    import pickle
    q = _POOL["q"]
    while True:
        item = q.get()
        if item[2] is None:
            return
        job, i = item[2], item[3]
        if job["dead"]:
            _pool_done(job, i, None)
            continue
        try:
            pr = w["proc"]
            for k in job["share"]:
                ver, msg = _POOL_SHARE[k]
                if w["sent"].get(k) != ver:
                    pr.stdin.write(msg)
                    pr.stdin.flush()
                    st, r = pickle.load(pr.stdout)
                    if st != "ok":
                        raise RuntimeError(str(r).strip().splitlines()[-1][:200])
                    w["sent"][k] = ver
            pr.stdin.write(pickle.dumps(("call", job["fn"], job["args"][i]), 4))
            pr.stdin.flush()
            st, r = pickle.load(pr.stdout)
            if st != "ok":
                raise RuntimeError(str(r).strip().splitlines()[-1][:200])
            _pool_done(job, i, r)
        except Exception as ex:
            job["dead"] = True
            job["err"] = job.get("err") or "{}: {}".format(type(ex).__name__, ex)
            w["alive"] = False
            _pool_done(job, i, None)
            try:
                w["proc"].kill()
            except Exception:
                pass
            return


def _pool_done(job, i, r):
    with job["cv"]:
        job["res"][i] = r
        job["left"] -= 1
        job["cv"].notify_all()


def pool_share(key, obj, ver):
    """Hand obj to every worker once (before the first piece of a job that needs it); ver tells when it changed.
    Rhino keeps the same object under the same key, so its own check computes from the same data."""
    import pickle
    if _POOL_SHARE.get(key, (None,))[0] != ver:
        _POOL_SHARE[key] = (ver, pickle.dumps(("set", key, obj), 4))
        _POOL_DATA[key] = obj
        _POOL_DATA.pop("_obj_" + key, None)


def pool_live():
    """The live workers when this run may use them (started on first use)."""
    if not _POOL.get("allow") or _POOL.get("broken"):
        return []
    return [w for w in pool_start() if w["alive"]]


def pool_submit(fn, args, share=(), prio=5, label=""):
    """Start fn(*a) for every a in args on the workers; returns at once. pool_wait gives the results in order.
    Without workers nothing starts here and pool_wait computes in Rhino."""
    import threading
    job = dict(fn=fn, args=list(args), share=tuple(share), res=[None] * len(args), left=len(args), dead=False,
               err=None, cv=threading.Condition(), label=label, local=True)
    if len(job["args"]) >= 1 and pool_live():
        job["local"] = False
        _POOL.setdefault("jobs", []).append(job)
        with _POOL["lock"]:
            for i in range(len(job["args"])):
                _POOL["seq"] += 1
                _POOL["q"].put((prio, _POOL["seq"], job, i))
    return job


def pool_wait(job):
    f = globals()[job["fn"]]
    if job["local"]:
        return [f(*a) for a in job["args"]]
    first = f(*job["args"][0])                         # Rhino computes the first piece itself: the check
    with job["cv"]:
        while job["left"] > 0:
            job["cv"].wait(1.0)
            if job["left"] > 0 and not any(w["alive"] for w in _POOL.get("w") or []):
                job["err"] = job["err"] or "no worker left running"
                break
    why = job["err"]
    if why is None and not _same(first, job["res"][0]):
        why = "the checked piece differs from Rhino's own result"
    if why is not None:
        _POOL["broken"] = True
        LOG.append("Worker processes ({}): not used from here on ({}); computed in Rhino.".format(job["label"], why))
        return [first] + [f(*a) for a in job["args"][1:]]
    _POOL["n_jobs"] = _POOL.get("n_jobs", 0) + 1
    _POOL.setdefault("labels", [])
    if job["label"] and job["label"] not in _POOL["labels"]:
        _POOL["labels"].append(job["label"])
    return job["res"]


def pool_map(fn, args, share=(), label=""):
    return pool_wait(pool_submit(fn, args, share, label=label))


def pool_result(job):
    """pool_wait once; the same list on every later call (for jobs whose pieces are taken one by one)."""
    if "out" not in job:
        job["out"] = pool_wait(job)
    return job["out"]


def _same(a, b):
    """Bit for bit the same result (numbers, NaN, arrays, bytes, nested lists, tuples and dicts)."""
    import struct
    if type(a) is not type(b):
        return False
    if HAVE_NP and isinstance(a, np.ndarray):
        return a.dtype == b.dtype and a.shape == b.shape and a.tobytes() == b.tobytes()
    if isinstance(a, float):
        return struct.pack("<d", a) == struct.pack("<d", b)
    if isinstance(a, (list, tuple)):
        return len(a) == len(b) and all(_same(x, y) for x, y in zip(a, b))
    if isinstance(a, dict):
        return list(a.keys()) == list(b.keys()) and all(_same(a[k], b[k]) for k in a)
    if HAVE_NP and isinstance(a, np.generic):
        return a.dtype == b.dtype and a.tobytes() == b.tobytes()
    return a == b


def pool_stop():
    """End the workers of this run (also after an error). A job still waited for is then computed in Rhino."""
    for job in _POOL.get("jobs") or []:
        with job["cv"]:
            if job["left"] > 0:
                job["dead"] = True
                job["err"] = job["err"] or "the workers were stopped"
                job["left"] = 0
                job["cv"].notify_all()
    ws = _POOL.get("w") or []
    q = _POOL.get("q")
    for w in ws:
        if q is not None:
            q.put((-1, -1, None, None))
    for w in ws:
        try:
            w["proc"].stdin.close()
        except Exception:
            pass
    for w in ws:
        try:
            w["proc"].wait(timeout=3)
        except Exception:
            try:
                w["proc"].kill()
            except Exception:
                pass
    allow = _POOL.get("allow")
    _POOL.clear()
    _POOL_SHARE.clear()
    _POOL_DATA.clear()
    if allow is not None:
        _POOL["allow"] = allow


def pool_report():
    """One LOG line: how many workers took part, or why none did."""
    if "w" not in _POOL:
        return
    n = len(_POOL["w"])
    if n and _POOL.get("n_jobs"):
        LOG.append("Worker processes: {} for {} ({} jobs, each checked against Rhino).".format(
            n, ", ".join(_POOL.get("labels", [])), _POOL["n_jobs"]))
    elif not n and _POOL.get("why"):
        LOG.append("Worker processes for terrain heights and section drawings: not used ({}); computed in Rhino as "
                   "in v17.".format(_POOL["why"]))


# ---- the pieces of work the workers take (plain data in, plain data out; Rhino runs the same functions to check)
class _TerrainOnly(object):
    """The terrain part of a site (the samples and their z_at), as a worker rebuilds it from the shared samples."""
    _no_pool = True


def _pool_terrain():
    d = _POOL_DATA["terrain"]
    T = _POOL_DATA.get("_obj_terrain")
    if T is None or T._d is not d:
        T = _TerrainOnly()
        T._d = d
        T.terrain_ok, T.terrain_smp = d
        T.z_at = terrain_z_at(T, T.terrain_smp)
        _POOL_DATA["_obj_terrain"] = T
    return T


def pool_terrain(S):
    """Hand the site's terrain samples to the workers (once per site)."""
    pool_share("terrain", (S.terrain_ok, S.terrain_smp), S.terrain_fp)
    return ("terrain",)


def _pool_z_np(X, Y):
    return z_np(_pool_terrain(), X, Y)


def _pool_z_at(pts):
    z = _pool_terrain().z_at
    return [z(x, y) for x, y in pts]


def _pool_chunks(n_items, n_min=1):
    """Contiguous pieces [a, b) for the workers: about three per worker, at least n_min items each."""
    nw = max(1, len(pool_live()))
    k = max(1, min(3 * nw, n_items // max(1, n_min)))
    return [(n_items * j // k, n_items * (j + 1) // k) for j in range(k)]


def z_at_many(S, pts, label="terrain heights"):
    """[S.z_at(x, y) for (x, y) in pts], on the workers when there are many points (the same function there)."""
    pts = list(pts)
    if len(pts) < 2000 or getattr(S, "_no_pool", False) or not pool_live():
        return [S.z_at(x, y) for x, y in pts]
    sh = pool_terrain(S)
    out = []
    for r in pool_map("_pool_z_at", [(pts[a:b],) for a, b in _pool_chunks(len(pts), 500)], sh, label):
        out += r
    return out


def noise_map_start(S, solids, cell=20.0, R=300.0, h_rec=4.0, h_src=0.5, nbin=36, model=None):
    """v17: the map's receivers handed to the worker processes (they run on while Rhino goes on)."""
    F = S.F
    NM = model or NoiseModel(S, solids, R, h_src, nbin)
    nx, ny = int(math.ceil(F.w / cell)) + 1, int(math.ceil(F.h / cell)) + 1
    where, pts = [], []
    for j in range(ny):
        for i in range(nx):
            x, y = F.world(F.u0 + i * cell, F.v0 + j * cell)
            if NM.inside(x, y):
                continue
            where.append((j, i))
            pts.append((x, y))
    tasks = [(x, y, z, (h_rec,)) for (x, y), z in zip(pts, z_at_many(S, pts, "sound receivers"))]   # v18
    return dict(h=noise_par_start(NM, tasks, "col", "map"), where=where, nx=nx, ny=ny, cell=cell, R=R, NM=NM)


def noise_map_collect(m):
    nx, ny, cell, R, NM = m["nx"], m["ny"], m["cell"], m["R"], m["NM"]
    grid = [[None] * nx for _ in range(ny)]
    for (j, i), rr in zip(m["where"], noise_par_collect(m["h"])):     # v17: on every core
        r = rr[0]
        if r is None:                                     # no counted road within R: not computed (not "quiet")
            grid[j][i] = dict(day=None, evening=None, night=None, lden=None, out=True)
            continue
        grid[j][i] = dict(day=r[0], evening=r[1], night=r[2], lden=r[3])
    return dict(grid=grid, cell=cell, nx=nx, ny=ny, n_src=len(NM.src), R=R)


# ------------------------------------------------------------ raster to vector: class regions with holes
def class_regions(cls, nx, ny):
    """Connected patches of equal class as polygons with holes, in cell-corner coordinates."""
    regions = []
    classes = set(v for row in cls for v in row if v is not None)
    for c in classes:
        nxt = {}

        def add(p, q):
            nxt.setdefault(p, []).append(q)
        for j in range(ny):
            row = cls[j]
            for i in range(nx):
                if row[i] != c:
                    continue
                if j == 0 or cls[j - 1][i] != c:
                    add((i, j), (i + 1, j))
                if i == nx - 1 or row[i + 1] != c:
                    add((i + 1, j), (i + 1, j + 1))
                if j == ny - 1 or cls[j + 1][i] != c:
                    add((i + 1, j + 1), (i, j + 1))
                if i == 0 or row[i - 1] != c:
                    add((i, j + 1), (i, j))
        loops = []
        while nxt:
            start = next(iter(nxt))
            loop = [start]
            prev, cur = None, start
            guard = 0
            while guard < 10 ** 6:
                guard += 1
                outs = nxt.get(cur)
                if not outs:
                    break
                if len(outs) == 1 or prev is None:
                    q = outs[0]
                else:
                    din = (cur[0] - prev[0], cur[1] - prev[1])
                    q = min(outs, key=lambda o: (din[0] * (o[1] - cur[1]) - din[1] * (o[0] - cur[0])))
                outs.remove(q)
                if not outs:
                    del nxt[cur]
                prev, cur = cur, q
                if cur == start:
                    break
                loop.append(cur)
            simp = []
            n_ = len(loop)
            for k in range(n_):
                a, b, d = loop[k - 1], loop[k], loop[(k + 1) % n_]
                if (b[0] - a[0]) * (d[1] - b[1]) - (b[1] - a[1]) * (d[0] - b[0]) != 0:
                    simp.append(b)
            if len(simp) >= 3:
                loops.append(simp)
        outers = [L_ for L_ in loops if signed_area(L_) > 0]      # the class on the left: outers anticlockwise
        holes = [L_ for L_ in loops if signed_area(L_) < 0]
        outers.sort(key=lambda L_: shoelace(L_)[0])
        groups = [(o, []) for o in outers]
        for h in holes:
            (x0, y0), (x1, y1) = h[0], h[1]                       # just on the class side of the hole's first edge
            L_ = math.hypot(x1 - x0, y1 - y0) or 1.0
            px, py = (x0 + x1) / 2.0 - (y1 - y0) / L_ * 0.25, (y0 + y1) / 2.0 + (x1 - x0) / L_ * 0.25
            for o, hl in groups:
                if pip(px, py, o):
                    hl.append(h)
                    break
        for o, hl in groups:
            regions.append((c, o, hl))
    return regions

# ============================================================ ENVIRONMENT · drawings and pages
NOISE_PALS = {
    # NoiseModelling style files: "Coloring Noise" (Tomio, for the DIN 45682 revision) and DIN 18005-2 / UNI 9884
    "coloring": ["82a7ac", "a0bbbf", "b8d6d1", "cfe4cc", "e3f2bf", "f4c683", "e87d4d", "cd463f", "a11a4d", "75095d", "430a4a"],
    "din": ["B7CE8E", "1D8435", "0E4C3C", "ECD721", "9F6F2C", "EF7926", "C71932", "8D1A27", "88497B", "18558C", "134367"]}


def ramp(hexes, n):
    cols = [C(h) for h in hexes]
    if n <= 1:
        return [cols[len(cols) // 2]]
    out = []
    for k in range(n):
        t = k * (len(cols) - 1) / float(n - 1)
        i = min(len(cols) - 2, int(t))
        out.append(mix(cols[i], cols[i + 1], t - i))
    return out


def nice_step(span, n):
    raw = span / float(max(1, n))
    mag = 10 ** math.floor(math.log10(raw)) if raw > 0 else 1.0
    for m in (1, 2, 2.5, 5, 10):
        if m * mag >= raw:
            return m * mag
    return 10 * mag


def fmt_h(h):
    m = int(round(h * 60))
    return "%d:%02d" % (m // 60, m % 60)


# ------------------------------------------------------------ grids -> classed regions -> board
def building_blocks(S, cell=2.0):
    """All footprints merged into blocks (2 m raster, traced back to outlines): one shape per block."""
    if S.env.get("blocks") is not None:
        return S.env["blocks"]
    F = S.F
    nx, ny = int(math.ceil(F.w / cell)), int(math.ceil(F.h / cell))
    grid = [[None] * nx for _ in range(ny)]
    for b in S.env["solids"][0]:
        for Q in convex_parts(b["P"]):
            for j, a0, a1 in raster_rows([F.local(x, y) for x, y in Q], F, cell, nx, ny):
                row = grid[j]
                for i in range(a0, a1):
                    row[i] = 1
    loops = []
    for c, outer, holes in class_regions(grid, nx, ny):
        loops.append([[F.world(F.u0 + i * cell, F.v0 + j * cell) for i, j in lp] for lp in [outer] + holes])
    S.env["blocks"] = loops
    return loops


# ------------------------------------------------------------ the four analyses as map panels
def lst_grid(S, season, cell=10.0):
    L_ = S.env["lst"].get(season)
    if not L_:
        return None
    memo = env_memo(S)
    mk = ("lst_grid", season, cell)
    r = memo.get(mk)
    if r is not None:
        return r
    F = S.F
    nx, ny = int(math.ceil(F.w / cell)), int(math.ceil(F.h / cell))
    g = [[lst_sample(L_, *F.world(F.u0 + (i + 0.5) * cell, F.v0 + (j + 0.5) * cell)) for i in range(nx)] for j in range(ny)]
    r = memo[mk] = (g, nx, ny, cell)
    return r


# ------------------------------------------------------------ solar radiation in 3D (axonometric)
# ------------------------------------------------------------ legends and key figures
def canopy_note(S, short=False):
    """The crowns of this bake, their leaf types (with the evidence) and the leaf season (for the sheets)."""
    tr = S.env["solids"][2] if getattr(S, "env", None) else []
    k = dict((nm, sum(1 for t in tr if t["kind"] == nm)) for nm in ("olive", "pine", "tree"))
    src = dict((v, sum(1 for t in tr if t.get("leaf_src") == v)) for v in (1, 2, 3))
    a, b = leaf_dates()
    s = "Crowns: {} from the 1 m canopy height map".format(len(tr))
    if short:
        return s + (" ({} evergreen, {} deciduous; leaf type from CLC+ Backbone 2021 / Sentinel-2), the deciduous ones in "
                    "leaf from {} to {} (Sentinel-2 2019-2025).".format(k["olive"] + k["pine"], k["tree"], a, b)
                    if src[1] + src[2] + src[3] else " ({} evergreen, {} deciduous from the land-use zones), the deciduous "
                    "ones in leaf from {} to {}.".format(k["olive"] + k["pine"], k["tree"], a, b))
    if src[1] + src[2] + src[3]:
        s += (", {} evergreen broadleaf, {} needle-leaved and {} deciduous (leaf type: the Copernicus CLC+ Backbone 2021 "
              "tree class under {} of them, their own Sentinel-2 seasonality 2019-2025 for {}, the nearest CLC+ tree pixel "
              "for {})".format(k["olive"], k["pine"], k["tree"], src[1], src[2], src[3]))
    else:
        s += ", {} evergreen and {} deciduous (leaf type from the survey's land-use zones)".format(k["olive"] + k["pine"], k["tree"])
    return s + ("; the deciduous ones in leaf from {} to {} (Sentinel-2 2019-2025). Crown heights are modelled (Meta/WRI map v1, "
                "machine-learning estimates, mean absolute error 2.8 m; Tolan et al. 2024), not measured. An olive crown "
                "passes 15 % of the direct sun all year (Castillo-Ruiz et al. 2016: 13.3-24.6 %), any other crown in leaf "
                "3 %, a bare one 46 % (Konarska et al. 2014).".format(a, b))


def height_note(S):
    """Where the building heights come from, with the counts of this bake (one sentence for every sheet)."""
    mains = [u for u in S.bld if not u["annex"]]
    n = dict((k, len([u for u in mains if u["floors_src"] == k])) for k in ("survey", "neighbours", "published", "osm",
                                                                            "unlabelled"))   # v50 (P06.3)
    t = getattr(S, "floor_test", (0, 0.0, 0.0))
    s = ("Building heights: floors x typical storey height; {} buildings carry a surveyed floor count".format(n["survey"]))
    if n["neighbours"]:
        s += (", {} without one take the count shared by most of the {} nearest surveyed buildings (civic, sacred and "
              "industrial ones: the nearest of their own use); tried on each of the {} surveyed floor labels in turn, "
              "this rule gives the same count {:.0f} % of the time and is within one floor {:.0f} %".format(
                  n["neighbours"], NB_K, t[0], t[1], t[2]))
    if n["osm"]:
        s += ", {} from OpenStreetMap levels".format(n["osm"])
    if n["unlabelled"]:                                  # v50 (MIRAQUA 28 Oct, P06.3)
        s += ", {} house outlines the survey closed without a floor label count as one storey".format(n["unlabelled"])
    if n["published"]:
        s += "; the Red Basilica hall and rotundas at their published heights (19 m, 18 m)"
    return s + "."


def traffic_rows(S):
    """Per street type with traffic in the frame: (type name, km in the frame, how its flow was found, k, AADT used
    for a two-way street, source)."""
    plan = traffic_plan(S)
    F = S.F
    agg = {}
    for r, tr in zip(getattr(S, "roads_noise", []), plan):
        if tr is None:
            continue
        km = sum(pl_length(run) for run in F.clip_line(r["P"])) / 1000.0
        if km <= 0.0:
            continue
        if tr["kind"] == "counted":
            key = ("counted", tr["src"])
        else:
            key = (tr["kind"], tr["cat"], round(tr["k"], 4), tr["src"])
        a = agg.setdefault(key, dict(tr=tr, km=0.0))
        a["km"] += km
    rows = []
    for key, a in agg.items():
        tr = a["tr"]
        c = tr["cat"]
        day = GPG_D[c] + GPG_E[c] + GPG_N[c]
        if tr["kind"] == "counted":
            rows.append((GPG_NAMES[c], a["km"], "counted", None, None, tr["src"]))
        else:
            rows.append((GPG_NAMES[c], a["km"], tr["kind"], tr["k"], tr["k"] * day, tr["src"]))
    order = {"counted": 0, "correlated": 1, "default": 2}
    rows.sort(key=lambda r_: (order[r_[2]], GPG_NAMES.index(r_[0]), -r_[1]))
    return rows


def traffic_note(S):
    """Which roads carry traffic in the sound model, and from what (v16.3: every street, counted or correlated)."""
    parts = []
    for nm, km, kind, k, aadt, src in traffic_rows(S):
        if kind == "counted":
            parts.append("{} {:.2f} km: counted ({})".format(nm, km, src))
        elif kind == "correlated":
            parts.append("{}s {:.2f} km: CORRELATED, k = {:.2f} ({:+.1f} dB) from {} -> {:,.0f} veh/day".format(
                nm, km, k, 10.0 * math.log10(k), src, aadt))
        else:
            parts.append("{}s {:.2f} km: GPG DEFAULT, no count of this type in reach (k = 1) -> {:,.0f} veh/day".format(
                nm, km, aadt))
    return ("Traffic (v16.3): every street carries traffic. KGM counts where KGM counted (hours split by VBUS Table 2, "
            "row 3: day 06-18, evening 18-22, night 22-06); every other street takes the default flow of its type from the EU noise-mapping guidance ({}), "
            "multiplied by k = counted AADT / GPG default of the nearest KGM-counted road of the SAME type (DERIVED, "
            "not measured on that street; types KGM never counts keep the plain default). Heavy share: vehicles over "
            "3.5 t from KGM's class counts on the counted roads (KGM's OYTT class taken as heavy, an assumption); "
            "KGM's printed truck share on the correlated streets. One-way OSM ways carry half. "
            "Speed: the signed limit where mapped, else 50 km/h, the urban limit. ".format(GPG_SRC) + "; ".join(parts) + ".")


def water_grid(S):
    gW = Grid(30.0)
    for P in getattr(S, "water_outline", []):
        for k in range(len(P) - 1):
            a, b = P[k], P[k + 1]
            gW.add((a, b), (min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1])))
    return gW


def env_memo(S):
    """Small results reused within a bake and kept with the environment analyses for the next one."""
    m = S.env.get("memo")
    if m is None:
        m = S.env["memo"] = {}
    return m


def water_band(S, gW, x, y):
    """0 = within 50 m of the river's edge, 2 = farther than 150 m, 1 = between (the same test as the distance)."""
    segs = gW.query((x - 50.0, y - 50.0, x + 50.0, y + 50.0))
    if segs and min(seg_dist(x, y, a[0], a[1], b[0], b[1]) for a, b in segs) <= 50.0:
        return 0
    segs = gW.query((x - 150.0, y - 150.0, x + 150.0, y + 150.0))
    if segs and min(seg_dist(x, y, a[0], a[1], b[0], b[1]) for a, b in segs) <= 150.0:
        return 1
    return 2


def lst_tiles(S, season):
    """v38 (was lst_figures, a paragraph): the season's surface-temperature readings as tiles."""
    G = lst_grid(S, season)
    if not G:
        return []
    vals, nx, ny, cell = G
    F = S.F
    memo = env_memo(S)
    bands = memo.get(("lst_bands", nx, ny, cell))
    if bands is None:                                   # distance to the river: the same for every season
        gW = water_grid(S)
        bands = {}
        for j in range(0, ny, 2):
            for i in range(0, nx, 2):
                bands[(i, j)] = water_band(S, gW, *F.world(F.u0 + (i + 0.5) * cell, F.v0 + (j + 0.5) * cell))
        memo[("lst_bands", nx, ny, cell)] = bands
    allv, near, far = [], [], []
    for j in range(0, ny, 2):
        for i in range(0, nx, 2):
            v = vals[j][i]
            if v is None:
                continue
            allv.append(v)
            b_ = bands[(i, j)]
            if b_ == 0:
                near.append(v)
            elif b_ == 2:
                far.append(v)
    allv.sort()
    if not allv:
        return []
    out = [("heat", "COOLEST 5 % · BELOW", "{:.1f} °C".format(allv[len(allv) // 20]), "[1]"),
           ("heat", "HOTTEST 5 % · ABOVE", "{:.1f} °C".format(allv[19 * len(allv) // 20]), "[1]")]
    if near and far:
        a_, b_ = sum(near) / len(near), sum(far) / len(far)
        dd = a_ - b_
        out += [("water", "WITHIN 50 m OF STREAM", "{:.1f} °C".format(a_), "[1]"),
                ("ground", "BEYOND 150 m", "{:.1f} °C".format(b_), "[1]"),
                ("water", "AT THE STREAM", "{} °C".format("0.0" if abs(dd) < 0.05 else "%+.1f" % dd), "[1]")]
    return out


# ------------------------------------------------------------ renders for each analysis
def noise_pal():
    """The sound bands' colours: input noise_palette ("brussels": the Brussels noise map's colour order over 11 DIN-style
    5 dB classes, not its 8 classes or colours (v21, R01-17), "coloring": Coloring Noise /
    DIN 45682 draft, "din": DIN 18005-2), else the graded bands (v16.4: quiet pale, loud dark, one hue run)."""
    if NOISE_PALETTE == "brussels":
        return list(TECH_PAL["noise"])
    if NOISE_PALETTE in NOISE_PALS:
        return list(NOISE_PALS[NOISE_PALETTE])
    if NOISE_PALETTE:
        LOG.append("noise_palette '{}' not known (brussels, coloring or din): the graded bands were used.".format(
            NOISE_PALETTE))
    return list(TECH_PAL["noise_graded"])


def noise_np(nm, key):
    """A sound grid as values (NaN inside buildings) and the receivers with no counted road within reach (out)."""
    nx, ny = nm["nx"], nm["ny"]
    vals = np.full(nx * ny, np.nan)
    out = np.zeros(nx * ny, bool)
    for j, row in enumerate(nm["grid"]):
        for i, c in enumerate(row):
            if not c:
                continue
            if c.get("out"):
                out[j * nx + i] = True
            elif c.get(key) is not None:
                vals[j * nx + i] = c[key]
    return vals, out


def noise_render(S, key, path, res):
    nm = S.env["noise"]
    vals, out = noise_np(nm, key)
    edges = [35, 40, 45, 50, 55, 60, 65, 70, 75, 80]
    return render_tech(path, S, S.F, res, vals, nm["nx"], nm["ny"], nm["cell"], 0.0, lut_classes(edges, noise_pal()),
                       roof="white", canopy_alpha=0.30, nodata=out if out.any() else None,
                       rkey=fp(S.env["keys"]["noise"], key))


def lst_np(S, season):
    """The season's surface temperature on a 10 m grid of the frame: (values (NaN = no clear pixel), nx, ny, cell)."""
    G = lst_grid(S, season)
    if not G:
        return None
    g, nx, ny, cell = G
    return np_grid(g, nx, ny).ravel(), nx, ny, cell


def heat_scale(S, season):
    """The season's surface temperature, centred on its own median: (grid, median, low, high); None without data."""
    G = lst_np(S, season)
    if not G:
        return None
    vals = np.sort(G[0][np.isfinite(G[0])])
    if vals.size == 0:
        return None
    med = float(vals[vals.size // 2])
    span = max(1.0, float(vals[int(0.98 * (vals.size - 1))]) - med, med - float(vals[int(0.02 * (vals.size - 1))]))
    return G, med, med - span, med + span


def shade_scale(daylight):
    """Hours in shade in classes of one hour, from 0 to the day's daylight."""
    n = max(1, int(math.ceil(daylight - 1e-6)))
    cols = ramp_hex(TECH_PAL["shade"], n)
    edges = [float(k) for k in range(1, n)]
    return n, cols, edges


def ramp_hex(hexes, n):
    cols = [hexrgb(h_) for h_ in hexes]
    out = []
    for k in range(n):
        t = k * (len(cols) - 1) / float(max(1, n - 1))
        i = min(len(cols) - 2, int(t))
        f = t - i
        out.append(tuple(int(round(cols[i][q] * (1 - f) + cols[i + 1][q] * f)) for q in range(3)))
    return out


def near_stream(S, xx, yy, R):
    """Which of the points lie within R metres of the river's edge (memoised per point set and distance)."""
    memo = env_memo(S)
    mk = ("near_stream", xx.size, float(xx[0]) if xx.size else 0.0, float(yy[-1]) if yy.size else 0.0, R)
    r = memo.get(mk)
    if r is not None:
        return r
    gW = water_grid(S)
    out = np.zeros(xx.size, bool)
    for k in range(xx.size):
        x, y = float(xx[k]), float(yy[k])
        segs = gW.query((x - R, y - R, x + R, y + R))
        if segs and min(seg_dist(x, y, a[0], a[1], b[0], b[1]) for a, b in segs) <= R:
            out[k] = True
    memo[mk] = out
    return out


def shade_items(S):
    """The rows of the shade sheet: the four key days and the mean day of the year."""
    sh = S.env["shade"]
    items = []
    for sd in SEASONS:
        d = sh["days"][sd["key"]]
        items.append(dict(key=sd["key"], season=sd["key"], name=sd["event"].upper(), hours=d["hours"], daylight=d["daylight"],
                          sub="sun up {}-{} local · {} h daylight · every minute [1]".format(fmt_h(d["sunrise"]), fmt_h(d["sunset"]),
                                                                                    fmt_h(d["daylight"]))))
    y = sh["year"]
    items.append(dict(key="year", season=None, name="THE MEAN DAY OF THE YEAR · ALL 365 DAYS", hours=y["hours"],
                      daylight=y["daylight"], sub="all 365 days averaged · {} h daylight on the mean day [1]".format(
                          fmt_h(y["daylight"]))))
    return items


def shade_tiles(S, it):
    """v38 (was shade_figures, a paragraph): the open ground's shade readings as tiles."""
    sh = S.env["shade"]
    h = it["hours"]
    o = np.isfinite(h)
    v = h[o]
    if v.size == 0:
        return []
    mean = float(v.mean())
    half = 100.0 * float((v >= it["daylight"] / 2.0).mean())
    G = sh["grid"]
    xx, yy = G["xx"][o], G["yy"][o]
    step = 4                                              # every 4th open cell for the stream band (a large sample)
    near = near_stream(S, xx[::step], yy[::step], 30.0)
    out = [("shade", "OPEN GROUND · MEAN SHADE", "{} h".format(fmt_h(mean)), "[1]"),
           ("clock", "SHARE OF THE DAYLIGHT", "{:.0f} %".format(100.0 * mean / it["daylight"]), "[1]"),
           ("shade", "SHADED > HALF THE DAY", "{:.0f} %".format(half), "[1]")]
    if near.any():
        out.append(("water", "WITHIN 30 m OF STREAM", "{} h".format(fmt_h(float(v[::step][near].mean()))), "[1]"))
    return out


def rad_scale(S, n=9):
    """Classes holding about equal shares of the ground and roof cells over all four seasons, in kWh/m2 per day
    rounded to 0.1 (one scale for the four maps, so the seasons compare)."""
    rd = S.env["rad"]
    vals = np.sort(np.concatenate([rd["seasons"][sd["key"]]["kwh"] for sd in SEASONS]))
    edges = []
    for k in range(1, n):
        e = round(float(vals[int(k * (vals.size - 1) / float(n))]) * 10.0) / 10.0
        if not edges or e > edges[-1]:
            edges.append(e)
    return edges


def rad_tiles(S, season):
    """v38 (was rad_figures_top, a line of figures): the season's radiation means as tiles, kWh/m2 per day."""
    rd = S.env["rad"]
    s = rd["seasons"][season]
    v = s["kwh"]
    gr = np.sort(v[~rd["roof"]])
    return [("roof", "ROOFS · MEAN kWh/m²·day", "{:.2f}".format(s["roof_mean"] or 0.0), "[1]"),
            ("ground", "GROUND · MEAN kWh/m²·day", "{:.2f}".format(s["ground_mean"] or 0.0), "[1]"),
            ("shade", "LOWEST 10 % GROUND · BELOW", "{:.2f}".format(float(gr[gr.size // 10]) if gr.size else 0.0), "[1]"),
            ("sun", "OPEN FLAT GROUND", "{:.2f}".format(s["ghi"]), "[3]")]


# ------------------------------------------------------------ the sheets
def sheet_sound(S, B, X, Y, U, rects, d):
    L = "LU_TECH::Sound"
    B.begin("TECHNICAL T1 · Sound", "LU_TECH")
    nm = S.env["noise"]
    cal = ("Calibrated with {} on-site measurements ({:+.1f} dB).".format(nm["n_meas"], nm["offset"]) if nm.get("n_meas")
           else "Not yet calibrated with on-site measurements.")
    # v38: keyword subtitle; the method paragraph as the footer's numbered key ([1]-[9] on this sheet)
    top, bottom = tech_frame(S, B, X, Y, U, "T1", "SOUND · ROAD TRAFFIC NOISE",
                             "Lden dB(A) · 4 m above ground · annual mean · top view [1]",
                             ["Method: RLS-90 road emission and segment method with distance, air and ground terms.",
                              "Screening: building screening by an "
                              "RLS-90-type D_z with the ISO 9613-2 limits (20 / 25 dB) and sign, the larger of it and the ground "
                              "term counted (VBUS eq. 6); VBUS's weather and reflection terms are not used; the "
                              "screening of each building block over its roof and round its two sides (ISO 9613-2 lateral "
                              "diffraction, v16.4).",
                              "Receivers 4 m above ground on a 10 m grid; colours: 5 dB bands, each darker "
                              "than the one before (the loudest darkest); Lden = day 06-18, evening 18-22 (+5 dB), night 22-06 (+10 dB), the periods of the "
                              "VBUS Table 2 hourly shares, from the "
                              "annual average daily traffic. Grey: no counted road within 300 m, not computed.",
                              "Streets (the sources): "
                              + ("solid grey surfaces with their edges, over the colours (v16.7)." if ROAD_SOLID else
                                 "hatched, with their edges, over the colours (v16.6)."),
                              traffic_note(S), height_note(S), "Trees: Meta/WRI 1 m canopy height map. Terrain: survey.",
                              "WHO Environmental Noise Guidelines (2018): road traffic below 53 dB Lden and 45 dB at night.",
                              cal])
    x0, W = X + PM * U, (PW - 2 * PM) * U
    p = os.path.join(d, "T1_sound_lden.png")
    noise_render(S, "lden", p, 1.0)
    V, wv, hv = tech_map(S, B, S.F, p, x0, top, W, 19.5 * U, U, L, crop_bar=False)   # v40: bands and tiles beside the bar
    road_overlay(S, B, V, L, 7)                           # v16.6: the streets (the sources) over the sound colours
    edges = [35, 40, 45, 50, 55, 60, 65, 70, 75, 80]
    labels = ["< 35"] + ["%d-%d" % (edges[k], edges[k + 1]) for k in range(len(edges) - 1)] + ["> 80"]
    cells = [c for row in nm["grid"] for c in row if c and c.get("lden") is not None]
    n_out = sum(1 for row in nm["grid"] for c in row if c and c.get("out"))
    share = [0] * 11
    for c in cells:
        share[sum(1 for e in edges if c["lden"] >= e)] += 1
    ntot = max(1, len(cells) + n_out)
    ly = tech_bands(B, x0 + 12.0 * U, top - hv - 0.6 * U, W * 0.56, noise_pal(), labels, U, L,
                    title="Lden dB(A) · share of the open ground" + (
                        " · {:.0f} % not computed [3]".format(100.0 * n_out / ntot) if n_out else ""),
                    sub=["{:.0f}%".format(100.0 * s / ntot) for s in share])
    who_d = 100.0 * sum(1 for c in cells if c["lden"] > 53.0) / ntot
    who_n = 100.0 * sum(1 for c in cells if c["night"] is not None and c["night"] > 45.0) / ntot
    tx = x0 + 12.0 * U + W * 0.56 + 2.0 * U
    vis_tiles(B, tx, top - hv - 0.6 * U, x0 + W - tx, [           # v38: the WHO reading as tiles (was a paragraph)
        ("limit", "ABOVE WHO 53 dB · Lden", "{:.0f} %".format(who_d), "[8]"),
        ("limit", "ABOVE WHO 45 dB · NIGHT", "{:.0f} %".format(who_n), "[8]"),
        ("gauge", "CALIBRATION", "{} pts · {:+.1f} dB".format(nm["n_meas"], nm["offset"]) if nm.get("n_meas")
         else "none", "[9]")], U, L)
    yB = ly - 1.0 * U
    pw = (W - 2 * 2.0 * U) / 3.0
    ph = pw * S.F.h / S.F.w
    for k, (key, name) in enumerate((("day", "DAY 06-18 · Ld"), ("evening", "EVENING 18-22 · Le"), ("night", "NIGHT 22-06 · Ln"))):
        px_ = x0 + k * (pw + 2.0 * U)
        t_title(B, px_, yB, name, pw, U, L, h=0.5)
        pp = os.path.join(d, "T1_sound_%s.png" % key)
        noise_render(S, key, pp, 2.0)
        Vk, _w, _h = tech_map(S, B, S.F, pp, px_, yB - 0.9 * U, pw, ph, U, L, scale=False)
        road_overlay(S, B, Vk, L, 7)
    yC = yB - 0.9 * U - ph - 1.6 * U
    if S.selinus and yC - bottom > 6.0 * U:
        t_title(B, x0, yC, "Lden ALONG THE STREAM · upstream left · WHO 53 dB dashed", W, U, L, h=0.5)
        tech_profile(S, B, x0, yC - 0.9 * U, W, min(7.5 * U, yC - bottom - 2.8 * U), U, L, who_ref="[8]")
    rects.append(("T1 · Sound", (X, Y - PH * U, X + PW * U, Y)))


def tech_rows(S, B, X, Y, U, rects, num, title, subtitle, sources, layer, render_fn, side_fn, items=None):
    """A sheet of map rows (the four seasons, or the given items), each with its side panel."""
    items = items or SEASONS
    L = "LU_TECH::" + layer
    B.begin("TECHNICAL %s · %s" % (num, layer), "LU_TECH")
    top, bottom = tech_frame(S, B, X, Y, U, num, title, subtitle, sources)
    x0, W = X + PM * U, (PW - 2 * PM) * U
    rowh = (top - bottom) / float(len(items))
    mh = rowh - 1.4 * U
    mw = min(W * 0.6, mh * S.F.w / S.F.h)
    ps = par_renders([(lambda sd_=sd: render_fn(sd_)) for sd in items])      # v18: the pictures side by side
    for k, sd in enumerate(items):
        y = top - k * rowh
        p = ps[k]
        V, wv, hv = tech_map(S, B, S.F, p, x0, y, mw, mh, U, L, scale=(k == len(items) - 1))
        side_fn(sd, x0 + wv + 2.4 * U, y, x0 + W - (x0 + wv + 2.4 * U), L)
    rects.append(("%s · %s" % (num, layer), (X, Y - PH * U, X + PW * U, Y)))


def lst_note(S, season):
    """When the season's surface temperature was seen: the scenes behind the mean (or the single scene of v1 data)."""
    L_ = S.env["lst"].get(season, {})
    if L_.get("n_scenes"):                            # v38: keywords (was a sentence)
        return ("{} clear scenes · {} to {} · {} UTC ({} local)".format(
            L_["n_scenes"], L_["first"], L_["last"], L_["utc_mean"], "%02d:%s" % ((int(L_["utc_mean"][:2]) + 3) % 24, L_["utc_mean"][3:])))
    when = L_.get("datetime_utc", "")
    return "Landsat {} · {} {} UTC (one scene)".format(L_.get("scene", "")[3:4], when[:10], when[11:16])


def sheet_heat(S, B, X, Y, U, rects, d):
    multi = any(v.get("n_scenes") for v in S.env["lst"].values())

    def render(sd):
        r = heat_scale(S, sd["key"])
        p = os.path.join(d, "T2_surface_heat_%s.png" % sd["key"])
        if r:
            (g, nx, ny, cell), med, vmin, vmax = r
            render_tech(p, S, S.F, 1.5, g, nx, ny, cell, 0.5, lut_ramp(vmin, vmax, TECH_PAL["heat"]), roof="field",
                        season=sd["key"], canopy_alpha=0.22, nodata=~np.isfinite(g) if (~np.isfinite(g)).any() else None,
                        rkey=fp(S.env["E_fp"], site_prints(S)["frame"], "lst", sd["key"]))
        else:
            render_tech(p, S, S.F, 1.5, np.zeros(4), 2, 2, max(S.F.w, S.F.h), 0.0, lut_ramp(0.0, 1.0, TECH_PAL["heat"]),
                        nodata=np.ones(4, bool), rkey=fp("no lst", sd["key"]))
        return p

    def side(sd, x, y, w, L):
        months = {"spring": "MARCH-MAY", "summer": "JUNE-AUGUST", "autumn": "SEPTEMBER-NOVEMBER", "winter": "DECEMBER-FEBRUARY"}
        t_title(B, x, y, "{} · {}".format(sd["name"], months[sd["key"]]), w, S.U, L)
        B.fit(lst_note(S, sd["key"]) + " [1]", x, y - 0.9 * S.U, 0.3 * S.U, w, T_GREY, L)
        r = heat_scale(S, sd["key"])
        if not r:
            B.fit("No clear scene: map grey [1]", x, y - 1.6 * S.U, 0.3 * S.U, w, T_INK, L)
            return
        _, med, vmin, vmax = r
        yy = tech_colorbar(B, x, y - 1.6 * S.U, w, TECH_PAL["heat"], vmin, vmax, S.U, L,
                           title="LST °C · white = season median {:.2f} °C [3]".format(med), unit="")
        yy = vis_tiles(B, x, yy - 0.1 * S.U, w, lst_tiles(S, sd["key"]), S.U, L, h=0.9)   # v38: tiles (was a paragraph)
        hs = (seam_pack().get("heat") or {}).get("seasons", {}).get(sd["key"])
        if hs:
            heat_canopy_inset(B, hs, x, yy - 0.35 * S.U, w * 0.55, S.U, L, ref="[4]")
    tech_rows(S, B, X, Y, U, rects, "T2", "SURFACE HEAT · FOUR SEASONS",
              "LST °C · Landsat 8/9 · late morning · " + ("mean of the clear scenes" if multi else "one clear scene a season")
              + " · 3D site from above [1]",
              ["Landsat 8/9 Collection 2 Level-2 surface temperature (USGS), band 10, cloud-masked (QA_PIXEL); "
               + ("every scene of 2021-2026 with at least 95 % of the area clear, averaged per season (each cell over the scenes "
                  "that saw it clear)." if multi else "one cloud-free scene per season."),
               "Thermal pixels are 100 m (delivered at 30 m), so read whole blocks, not single roofs; surface temperature is "
               "not air temperature.", "Each season is centred on its own median. Roofs carry the satellite value.",
               "Under the trees: mean surface temperature of the 30 m cells by canopy cover, with the cells counted and "
               "Pearson's r."],
              "Surface heat", render, side)


def heat_canopy_inset(B, hs, x, y, w, U, L, ref=""):
    """v33 (plant analysis panel 6): mean surface temperature of the frame's 30 m cells by their canopy cover, one bar
    per cover class, with the cells counted and Pearson's r. An association at block scale, not cooling per tree.
    v35: the classes are re-binned from the cells (25-100 % in one class; v34's 50-100 % held 3 cells)."""
    bins = hs["bins"]
    pts = hs.get("points") or []
    if pts:
        bins = []
        for lab, lo, hi in (("0 %", None, None), ("0-10 %", 0.0, 0.10), ("10-25 %", 0.10, 0.25), ("25-100 %", 0.25, 1.01)):
            v = [t for c, t in pts if (c <= 0.0 if lo is None else (c > 0.0 and lo <= c < hi))]
            if v:
                bins.append(dict(label=lab, n=len(v), mean=sum(v) / len(v)))
    lo = min(b_["mean"] for b_ in bins) - 0.5
    hi = max(b_["mean"] for b_ in bins)
    B.fit("UNDER THE TREES · {:,} cells · {} scenes · Pearson r {:.2f} {}".format(        # v38: keywords + [n]
        hs["cells"], hs.get("scenes", "?"), hs["pearson_r"], ref), x, y, 0.28 * U, w, T_INK, L)
    y -= 0.75 * U
    lw, vw = 2.2 * U, 1.6 * U
    bw = w - lw - vw
    for b_ in bins:
        f = (b_["mean"] - lo) / max(1e-6, hi - lo)
        B.text(b_["label"] + " cover", x, y, 0.24 * U, T_GREY, L)
        B.fill([rect(x + lw, y, x + lw + bw * f, y + 0.26 * U)], mix(LEAF_COL[0], (200, 70, 30), f), L, 30)
        B.text("{:.2f} °C · {:,} cells".format(b_["mean"], b_["n"]),
               x + lw + bw * f + 0.15 * U, y, 0.24 * U, T_INK, L)
        y -= 0.42 * U
    return y


