"""Run one Bergama script as if in a GH Python 3 component: fake Rhino (tools/fakerhino.py), frozen clock.
usage: run_gh.py <script.py> <fake_home>"""
import sys, os, time, runpy, random, types
from unittest import mock
script, home = sys.argv[1], sys.argv[2]
os.environ["HOME"] = home; os.environ["USERPROFILE"] = home
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
# fake Rhino: the survey from $BERGAMA_SURVEY (pickle made by survey_to_pickle.py), else an empty file
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fakerhino
fakerhino.install(os.environ.get("BERGAMA_SURVEY") or None, home)
gh = mock.MagicMock(name="ghenv"); gh.Component.InstanceGuid = "00000000-test"; gh.Component.Params.Input = [types.SimpleNamespace(VariableName=n, NickName=n, Name=n) for n in ("run", "rhino_bake")]; gh.Component.Params.Output = []
sys.argv = [script]
if os.environ.get("DUPCALLS"):                # DUPCALLS=<file>: calls of the script's own functions with the same arguments
    import pickle, hashlib, collections, json as _js
    _seen = collections.Counter(); _cost = collections.Counter(); _tot = collections.Counter(); _skip = set()
    _ab = os.path.abspath(script)
    def _prof(frame, event, arg):
        if event != "call" or frame.f_code.co_filename != _ab: return
        c = frame.f_code; k0 = (c.co_name, c.co_firstlineno); _tot[k0] += 1
        if k0 in _skip or _tot[k0] > 400: return
        try:
            args = tuple(frame.f_locals.get(v) for v in c.co_varnames[:c.co_argcount + c.co_kwonlyargcount])
            b = pickle.dumps(args, 4)
        except Exception:
            _skip.add(k0); return
        _seen[k0 + (hashlib.md5(b).hexdigest(),)] += 1; _cost[k0] = max(_cost[k0], len(b))
    sys.setprofile(_prof)
if os.environ.get("PROFILE"):                 # PROFILE=<file>: cProfile stats of the run (tools/hot.py reads them)
    import cProfile
    _p = cProfile.Profile(); _p.enable()
g = runpy.run_path(script, init_globals={"ghenv": gh, "run": True, "rhino_bake": False}, run_name="__main__")
if os.environ.get("PROFILE"):
    _p.disable(); _p.dump_stats(os.environ["PROFILE"])
if os.environ.get("DUPCALLS"):
    sys.setprofile(None)
    rep = collections.Counter()
    for k, n in _seen.items():
        if n > 1: rep[k[:2]] += n - 1
    with open(os.environ["DUPCALLS"], "w") as f:
        _js.dump([dict(fn=k[0], line=k[1], repeats=n, calls=_tot[k], arg_bytes=_cost[k]) for k, n in rep.most_common()], f, indent=0)
print("\n#LOG#", str(g.get("log"))[:400].replace("\n", " | "))
