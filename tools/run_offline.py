"""Run one Bergama script offline (plain Python, no Rhino) with frozen time.
usage: run_offline.py <script.py> <fake_home>"""
import sys, os, time, runpy, random
script, home = sys.argv[1], sys.argv[2]
os.environ["HOME"] = home
os.environ["USERPROFILE"] = home
T0 = 1792940400.0  # fixed clock
_c = [0]
def ftime():
    _c[0] += 1
    return T0 + _c[0] * 0.001
_lt = time.localtime(T0); _gm = time.gmtime(T0)
time.time = ftime
time.perf_counter = ftime
time.localtime = lambda s=None: _lt
time.gmtime = lambda s=None: _gm
_sf = time.strftime
time.strftime = lambda f, t=None: _sf(f, _lt)
import datetime as _dt
class FDT(_dt.datetime):
    @classmethod
    def now(cls, tz=None): return cls(2026, 10, 25, 18, 0, 0)
    @classmethod
    def today(cls): return cls(2026, 10, 25, 18, 0, 0)
_dt.datetime = FDT
random.seed(0)
sys.argv = [script]
runpy.run_path(script, run_name="__main__")
