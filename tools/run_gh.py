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
g = runpy.run_path(script, init_globals={"ghenv": gh, "run": True, "rhino_bake": False}, run_name="__main__")
print("\n#LOG#", str(g.get("log"))[:400].replace("\n", " | "))
