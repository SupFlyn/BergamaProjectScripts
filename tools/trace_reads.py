"""Run one Bergama script like tools/run_gh.py (fake Rhino, frozen clock) and record what it really reads and writes.
usage: trace_reads.py <script.py> <fake_home> <out.json>
Records every file opened (builtins/io open, PIL Image.open, fitz.open), every folder listed (os.listdir/scandir/walk,
glob) and every file written, under <fake_home>/Downloads/Bergama, plus "rhino" when the script reads Rhino document
objects. tools/make_script_reads.py turns these traces into kit/scripts/script_reads.txt (the board builder's read list).
"""
import sys, os, json, builtins, io, glob as _glob
script, home, out = sys.argv[1], os.path.realpath(sys.argv[2]), sys.argv[3]
ROOT = os.path.join(home, "Downloads", "Bergama")
REC = {"reads": set(), "writes": set(), "lists": set(), "rhino": False}


def _rel(p):
    try:
        p = os.path.realpath(os.fspath(p))
    except Exception:
        return None
    if p == ROOT or not p.startswith(ROOT + os.sep):
        return None
    return os.path.relpath(p, ROOT).replace(os.sep, "/")


def _note(p, mode="r"):
    r = _rel(p) if isinstance(p, (str, bytes, os.PathLike)) else None
    if r is None:
        return
    if any(c in str(mode) for c in "wax+"):
        REC["writes"].add(r)
    elif r not in REC["writes"]:           # a file this run wrote first and then reads back is its own output
        REC["reads"].add(r)


_open = builtins.open
def t_open(f, mode="r", *a, **k):
    _note(f, mode)
    return _open(f, mode, *a, **k)
builtins.open = t_open
io.open = t_open
_ld, _sd, _wk = os.listdir, os.scandir, os.walk
def t_list(p="."):
    r = _rel(p)
    if r is not None:
        REC["lists"].add(r)
    return _ld(p)
def t_scan(p="."):
    r = _rel(p)
    if r is not None:
        REC["lists"].add(r)
    return _sd(p)
def t_walk(top, *a, **k):
    r = _rel(top)
    if r is not None:
        REC["lists"].add(r)
    return _wk(top, *a, **k)
os.listdir, os.scandir, os.walk = t_list, t_scan, t_walk
_gl = _glob.glob
def t_glob(pat, *a, **k):
    r = _rel(os.path.dirname(pat) or ".")
    if r is not None:
        REC["lists"].add(r)
    return _gl(pat, *a, **k)
_glob.glob = t_glob
try:
    from PIL import Image as _Im
    _imo = _Im.open
    def t_imo(f, *a, **k):
        _note(f, "r")
        return _imo(f, *a, **k)
    _Im.open = t_imo
except Exception:
    pass
try:
    import fitz as _fz
    _fzo = _fz.open
    def t_fzo(f=None, *a, **k):
        if isinstance(f, (str, os.PathLike)):
            _note(f, "r")
        return _fzo(f, *a, **k)
    _fz.open = t_fzo
except Exception:
    pass

# fake Rhino with a read flag on the document's objects
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fakerhino
for _n in ("FindByLayer", "GetObjectList", "FindId", "Find"):
    _f = getattr(fakerhino.Objects, _n)
    def _w(self, *a, _f=_f, **k):
        REC["rhino"] = True
        return _f(self, *a, **k)
    setattr(fakerhino.Objects, _n, _w)
_it = fakerhino.Objects.__iter__
def _iter(self):
    REC["rhino"] = True
    return _it(self)
fakerhino.Objects.__iter__ = _iter


def _save():
    with _open(out, "w", encoding="utf-8") as fh:
        json.dump({"script": os.path.basename(script), "rhino": REC["rhino"], "reads": sorted(REC["reads"]),
                   "lists": sorted(REC["lists"]), "writes": sorted(REC["writes"])}, fh, indent=1)


import atexit
atexit.register(_save)

# the GH run (as tools/run_gh.py): frozen clock, fake Rhino; TWO solves, Button off then on, because the trigger's first
# solve of a document only notes the Button's state (common/trigger.py, round 5 C2)
import time, random, types, runpy
from unittest import mock
os.environ["HOME"] = home; os.environ["USERPROFILE"] = home
os.environ["WINDIR"] = os.path.join(home, "Windows")      # Arial = Liberation Sans (same metrics) under WINDIR/Fonts
_fd = os.path.join(home, "Windows", "Fonts")
os.makedirs(_fd, exist_ok=True)
for _a, _b in (("arial", "Regular"), ("arialbd", "Bold"), ("ariali", "Italic"), ("arialbi", "BoldItalic")):
    _t = os.path.join(_fd, _a + ".ttf")
    if not os.path.exists(_t):
        os.symlink("/usr/share/fonts/truetype/liberation/LiberationSans-%s.ttf" % _b, _t)
T0 = 1792940400.0; _c = [0]
def ftime():
    _c[0] += 1; return T0 + _c[0] * 0.001
_lt = time.localtime(T0); _gm = time.gmtime(T0)
time.time = ftime; time.perf_counter = ftime
time.localtime = lambda s=None: _lt; time.gmtime = lambda s=None: _gm
_sf = time.strftime; time.strftime = lambda f, t=None: _sf(f, _lt)
import datetime as _dt
class FDT(_dt.datetime):
    @classmethod
    def now(cls, tz=None): return cls(2026, 10, 25, 18, 0, 0)
    @classmethod
    def today(cls): return cls(2026, 10, 25, 18, 0, 0)
_dt.datetime = FDT
random.seed(0)
fakerhino.install(os.environ.get("BERGAMA_SURVEY") or None, home)
gh = mock.MagicMock(name="ghenv"); gh.Component.InstanceGuid = "00000000-test"
gh.Component.Params.Input = [types.SimpleNamespace(VariableName=n, NickName=n, Name=n, Sources=[]) for n in ("run", "rhino_bake")]
gh.Component.Params.Output = []
sys.argv = [script]
for _on in (False, True):
    g = runpy.run_path(script, init_globals={"ghenv": gh, "run": _on, "rhino_bake": False}, run_name="__main__")
print("\n#LOG#", str(g.get("log"))[:400].replace("\n", " | "))
