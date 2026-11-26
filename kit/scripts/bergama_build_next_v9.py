# -*- coding: utf-8 -*-
r"""Bergama: one-step AcBuild run with timings (build_next v9, 26 Nov 2026).
v9 (v8 runs of 26 Nov: every "open" took about 72 s and the start-up check 43 s, most of it waiting on closed ports;
proposal and context were built one after the other): the port scan waits 0.4 s per port (was 2.0 s) and the wait
loops look every 3 s (were 15 s and 10 s). --parallel builds _proposal and _context at the same time, each in its own
Archicad (two ports in 19723-19743, told apart by the project each one has open), with one hidden "_worker" process of
this launcher per file (AcBuild v2.16 takes its port from BERGAMA_AC_PORT and then writes
logs\bergama_acbuild_progress_<port>.txt and logs\bergama_acbuild_site_log_<port>.txt); the worker lines in the status
file start with [proposal] / [context]; the master follows as before, in one Archicad. When the second Archicad does
not come up or the two cannot be told apart: a FLAG line, and the files are built one after the other. Without
--parallel the run is the v8 run.
  py -3 bergama_build_next_v9.py build --only proposal,context --parallel
v8 (Aras 26 Nov 20:29 UTC "dont build v2.16 from an empty file ... perfect the code ... just after that i want you to
build from empty file"): test builds of one part only, --only proposal | context | master (comma list allowed): that
part is copied from the newest built file of the same part, the others are not touched, and the reopen + 3D test
runs only when the master is built.
  py -3 bergama_build_next_v8.py build --only proposal
v7 (Aras 25 Nov 10:16 UTC "you dont need to build from empty every time we that cleanup once it is fine"): the
default build starts from the newest built version again, and with split files each part is copied from the same
part of it (_proposal from _proposal, _context from _context, the master from the master), so AcBuild keeps what
did not change; --empty stays for a one-off clean start.
  py -3 bergama_build_next_v7.py build
v6 (Aras 25 Nov 08:42 UTC "cant we build a new file from ground up"): with --empty the files are not copies of the
source pln but of a new, empty project: Archicad opens the source, File > New (Tapir NewProject, from the template in
Archicad's New Project settings) and saves it as archicad\Bergama_empty_<date>_<time>.pln (the source is never saved);
that empty file is then copied to _proposal, _context and the master as before. AcBuild makes the layers, materials,
composites, overrides, sections and views itself; his layouts and publisher set are not in an empty file.
  py -3 bergama_build_next_v7.py build --cold --empty
v5 (v2.10 cold run 24-25 Nov: the final reopen was cut off and no DONE line or timings were written): as soon as the
three files are built and saved, a line "BUILT ..." and the timings json are written; the reopen + 3D test follows and
the timings are written again at the end.
v4 (Aras 24 Nov 17:42-17:49 UTC: proposal and context in two files hotlinked into one master; "do that run as a cold run
with all correct files"): when the AcBuild holds SPLIT_FILES = True, three copies of the source are built one after the
other, each in a fresh Archicad: Bergama_AC_v<ver>_proposal.pln, Bergama_AC_v<ver>_context.pln, then the master
Bergama_AC_v<ver>.pln (it hotlinks the other two); the reopen + 3D timing is done on the master.
  py -3 bergama_build_next_v4.py build --cold     first moves AcBuild's caches (cached\bergama_archicad_site,
      _proposal, _context, _buildings) and Archicad's cache folder into archicad\_coldrun_backup_<date>_<time>\ (moved,
      never deleted), so every element, section and view is made fresh
v3 (Aras 24 Nov 17:20 UTC: "use the letters like 2.01 is the latest edit according to my feedback ... edits in the night
it would go like 2.01a 2.01b and so on after 2.01z 2.01aa 2.01ab"): AcBuild names with a letter suffix
(bergama_acbuild_v2_09a.py) are found, ordered 2.09 < 2.09a < ... < 2.09z < 2.09aa, and build Bergama_AC_v2.09a.pln.
v2 (Aras 23 Nov 21:11 UTC "run this same script in both pc's ... do a speed comparison like time to build and open up 3D
window, saving and closing"): every step is timed and written to cached\bergama_archicad_site\speed_<PC>_<time>.json;
after the build: a timed save, a timed quit, a timed reopen of the built file, a timed 3D window, a timed quit.
  py -3 bergama_build_next_v2.py build --from Bergama_AC_v1.96.pln     a given source file (default: the newest)
  ... --acbuild bergama_acbuild_v2_02.py                                a given AcBuild version from main
(v1 text below)
Aras 23 Nov 20:41 UTC: "we do that launcher idea for your use just in case", "do the indexing and pointing to that so
you can run that". It does the know-how note's run recipe (library/_index/knowhow/archicad_acbuild.md) in one go:

  0. fetches the newest bergama_acbuild_v*.py from GitHub main into scripts\ (a different local copy of the same
     name is moved to scripts\_replaced\ first, never deleted)
  1. stops if Archicad is already running on this PC (one licence key: close Archicad on the OTHER PC yourself)
  2. moves the AutoSave-Archicad-30* folders and stale .lck files into archicad\_recovery_backup_<date>\ (moved,
     never deleted), so no hidden "Project Recovery" dialog blocks Tapir
  3. copies the newest archicad\Bergama_AC_v*.pln to Bergama_AC_v<AcBuild version>.pln (stops if that file exists)
  4. starts Archicad with the copy and waits until Tapir answers with that project open
  5. runs AcBuild (it saves the project itself at the end)
  6. counts the elements per type (read-only) and compares them with the last run
  7. quits Archicad (restart after every run)

  py -3 bergama_build_next_v1.py            the whole recipe
  py -3 bergama_build_next_v1.py check      only steps 1, 4 (newest Bergama_AC_v*.pln), 6, 7: reopen test + counts

Step lines go to logs\bergama_build_next_status.txt; its last line starts with DONE or ERROR.
Counts per run: cached\bergama_archicad_site\build_next_counts.json.
"""
import datetime, glob, hashlib, json, os, re, runpy, shutil, subprocess, sys, time, urllib.request

_BG = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
ROOT = os.path.join(_BG, "Project Files") if os.path.isdir(os.path.join(_BG, "Project Files", "scripts")) else _BG
SCRIPTS = os.path.join(ROOT, "scripts")
AC_DIR = os.path.join(ROOT, "archicad")
STATUS = os.path.join(ROOT, "logs", "bergama_build_next_status.txt")
COUNTS = os.path.join(ROOT, "cached", "bergama_archicad_site", "build_next_counts.json")
AUTOSAVE = os.path.join(os.path.expanduser("~"), "GRAPHISOFT")
GH_LIST = "https://api.github.com/repos/SupFlyn/BergamaProjectScripts/contents/kit/scripts?ref=main"
PORTS = range(19723, 19744)
OPEN_WAIT_MIN = 30          # minutes for Archicad to open the project (the v1.96 file is 868.5 MB)
QUIT_WAIT_MIN = 10
FROM = []                   # v2: --from source pln name
COLD = []                   # v4: --cold
EMPTY = []                  # v6: --empty
ONLY = []                   # v8: --only proposal,context,master (the parts built; none = all)
PIN = []                    # v2: --acbuild <bergama_acbuild_vX_YY.py> (default: the newest on main)
PARALLEL = []               # v9: --parallel (proposal and context at the same time, each in its own Archicad)
PART = []                   # v9: in a _worker process: its part name (the prefix of its status lines)
MULTI = []                  # v9: set while more than one Archicad may run (memory read-outs cover all of them)
T = {}                      # v2: step -> seconds
MEM = {}                    # v2: step -> Archicad working set (GB) after it
TYPES = ("Wall", "Column", "Beam", "Window", "Door", "Object", "Lamp", "Slab", "Roof", "Mesh", "Zone",
         "CurtainWall", "Shell", "Skylight", "Morph", "Stair", "Railing", "Opening")


def say(t):
    line = u"%s  %s%s" % (time.strftime("%H:%M:%S"), (u"[%s] " % PART[0]) if PART else u"", t)   # v9: worker prefix
    print(line, flush=True)
    with open(STATUS, "a", encoding="utf-8") as f:   # v9: one open + one write per line: two processes cannot mix lines
        f.write(line + u"\n")


def vkey(p):
    """v3: version order with letter suffixes: v2_09 < v2_09a < v2_09z < v2_09aa (also Bergama_AC_v2.09a.pln)"""
    m = re.search(r"v(\d+)[_.](\d+)([a-z]*)", os.path.basename(p))
    if not m:
        return [-1, -1, 0, u""]
    return [int(m.group(1)), int(m.group(2)), len(m.group(3)), m.group(3)]


def blob_sha(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def fetch_newest():
    """step 0: the newest AcBuild on GitHub main, in scripts\\ (Aras 17 Nov: every script comes from main)"""
    with urllib.request.urlopen(urllib.request.Request(GH_LIST, headers={"User-Agent": "bergama-build-next"}),
                                timeout=60) as f:
        items = json.loads(f.read().decode("utf-8"))
    ac = [i for i in items if re.match(r"bergama_acbuild_v\d+_\d+[a-z]*\.py$", i["name"])]
    if PIN:                                        # --acbuild <name>: that version from main, not the newest
        ac = [i for i in ac if i["name"] == PIN[0]]
        if not ac:
            raise RuntimeError(u"%s is not on GitHub main" % PIN[0])
    top = max(ac, key=lambda i: vkey(i["name"]))
    dst = os.path.join(SCRIPTS, top["name"])
    if os.path.isfile(dst):
        with open(dst, "rb") as f:
            if blob_sha(f.read()) == top["sha"]:
                say(u"AcBuild %s on this PC = GitHub main" % top["name"])
                return dst
        old = os.path.join(SCRIPTS, "_replaced", top["name"] + time.strftime(".%Y%m%d_%H%M%S"))
        os.makedirs(os.path.dirname(old), exist_ok=True)
        shutil.move(dst, old)
        say(u"FLAG local %s differed from main: moved to %s" % (top["name"], old))
    with urllib.request.urlopen(top["download_url"], timeout=300) as f:
        data = f.read()
    if blob_sha(data) != top["sha"]:
        raise RuntimeError(u"download of %s incomplete (checksum differs)" % top["name"])
    with open(dst, "wb") as f:
        f.write(data)
    say(u"AcBuild %s fetched from GitHub main" % top["name"])
    return dst


def timed(step, fn, *a):
    """v2: run one step, keep its seconds and Archicad's memory after it"""
    t0 = time.time()
    r = fn(*a)
    T[step] = round(time.time() - t0, 1)
    MEM[step] = ac_mem_gb()
    say(u"TIME %s: %.0f s%s" % (step, T[step], u"" if MEM[step] is None else u" (%s %.1f GB)" % (
        u"all Archicad instances" if MULTI else u"Archicad", MEM[step])))   # v9: tasklist sums every Archicad.exe
    return r


def ac_mem_gb():
    """v2: Archicad's working set from tasklist (GB), None when not running (v9: the sum over all instances)"""
    try:
        out = subprocess.run(["tasklist", "/FI", "IMAGENAME eq Archicad.exe", "/FO", "CSV", "/NH"],
                             capture_output=True, text=True).stdout
        kb = [int(re.sub(r"[^\d]", "", l.split('","')[-1]) or 0) for l in out.splitlines() if "archicad" in l.lower()]
        return round(sum(kb) / 1048576.0, 1) if kb else None
    except Exception:
        return None


def open_3d(url):
    """v2: open the 3D window and wait until Archicad answers again (3D built)"""
    tapir(url, "ChangeWindow", {"windowType": "3DModel"}, 7200.0)
    post(url, {"command": "API.IsAlive"}, 7200.0)


def save(url):
    tapir(url, "SaveProject", {}, 7200.0)


def archicad_running():
    out = subprocess.run(["tasklist", "/FO", "CSV", "/NH"], capture_output=True, text=True).stdout.lower()
    return u'"archicad.exe"' in out


def move_leftovers():
    """step 2: crash autosaves + stale locks aside (moved, never deleted)"""
    bk = os.path.join(AC_DIR, "_recovery_backup_" + time.strftime("%Y-%m-%d"))
    found = glob.glob(os.path.join(AUTOSAVE, "AutoSave-Archicad-30*")) + glob.glob(os.path.join(AC_DIR, "*.lck"))
    for p in found:
        os.makedirs(bk, exist_ok=True)
        dst = os.path.join(bk, os.path.basename(p))
        if os.path.exists(dst):
            dst += time.strftime(".%H%M%S")
        shutil.move(p, dst)
    say(u"leftovers moved to %s: %d" % (bk, len(found)) if found else u"no AutoSave folders or .lck files")


def newest_pln():
    fs = [f for f in glob.glob(os.path.join(AC_DIR, "Bergama_AC_v*.pln"))
          if not re.search(r"_(proposal|context)\.pln$", f, re.I)]   # v4: the master / single file only
    if not fs:
        raise RuntimeError(u"no Bergama_AC_v*.pln in %s" % AC_DIR)
    return max(fs, key=vkey)


def post(url, body, timeout):
    req = urllib.request.Request(url, json.dumps(body).encode("utf-8"), {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as f:
        return json.loads(f.read().decode("utf-8"))


def alive(url, timeout=0.4):
    """v9: True when the Archicad at url answers (0.4 s, was 2.0 s: on Windows a closed port costs the full timeout,
    21 ports = 42 s per scan with no Archicad up)"""
    try:
        return bool(post(url, {"command": "API.IsAlive"}, timeout).get("result", {}).get("isAlive"))
    except Exception:
        return False


def find_ac(skip=(), every=False):
    """the first answering Archicad, or None (v9: skip = urls not looked at; every = the list of all that answer)"""
    found = []
    for p in PORTS:
        u = "http://127.0.0.1:%d" % p
        if u in skip or not alive(u):
            continue
        if not every:
            return u
        found.append(u)
    return found if every else None


def tapir(url, name, params=None, timeout=600.0):
    p = {"addOnCommandId": {"commandNamespace": "TapirCommand", "commandName": name}}
    if params is not None:
        p["addOnCommandParameters"] = params
    r = post(url, {"command": "API.ExecuteAddOnCommand", "parameters": p}, timeout)
    if not r.get("succeeded"):
        raise RuntimeError(u"%s failed: %s" % (name, json.dumps(r.get("error"))[:300]))
    out = (r.get("result") or {}).get("addOnCommandResponse") or {}
    if isinstance(out, dict) and out.get("error"):
        raise RuntimeError(u"%s: %s" % (name, json.dumps(out["error"])[:300]))
    return out


def has_project(url, pln):
    """v9: True when the Archicad at url has pln open (the v8 test of open_in_archicad, also used to tell two apart)"""
    info = tapir(url, "GetProjectInfo")
    names = [re.sub(r"\.pln$", u"", os.path.basename(n or u"").lower())
             for n in (pln, info.get("projectPath"), info.get("projectName"))]   # "v2.00": never splitext
    return names[0] in names[1:]


def open_in_archicad(pln, skip=()):
    """step 4: start Archicad 30 with the project and wait for Tapir with that project open (v9: skip = the urls of
    Archicads already open with another file: a second instance is started and must answer on a new port)"""
    exe = sorted(glob.glob(r"C:\Program Files\GRAPHISOFT\Archicad 30*\Archicad.exe"))
    if exe:
        subprocess.Popen([exe[-1], pln])
    else:
        os.startfile(pln)
    say(u"Archicad starting with %s (waiting up to %d min)" % (os.path.basename(pln), OPEN_WAIT_MIN))
    t_end = time.time() + 60 * OPEN_WAIT_MIN
    while time.time() < t_end:
        time.sleep(3)                              # v9: was 15 ("open" was never under 30 s)
        url = find_ac(skip)
        if not url:
            continue
        try:
            if not has_project(url, pln):
                continue
        except Exception:
            continue
        say(u"project open, Tapir answers at %s" % url)
        return url
    raise RuntimeError(u"Archicad did not answer with %s open within %d min (a hidden dialog such as Project "
                       u"Recovery or License Information may be waiting)" % (os.path.basename(pln), OPEN_WAIT_MIN))


def count(url, pln, label):
    """step 6: elements per type (read-only), compared with the last entry"""
    try:
        tapir(url, "ChangeWindow", {"windowType": "FloorPlan"})   # counts list the active window's database
    except Exception as ex:
        say(u"FLAG floor plan not activated (%s): counts may cover only the active window" % ex)
    c = {}
    for t in TYPES:
        try:
            c[t] = len(tapir(url, "GetElementsByType", {"elementType": t}, 1800.0).get("elements") or [])
        except Exception:
            pass                                   # a type this Archicad / Tapir does not know
    c = {k: v for k, v in c.items() if v}
    os.makedirs(os.path.dirname(COUNTS), exist_ok=True)
    lock = COUNTS + u".lock"                       # v9: two workers may read + write the history at the same moment:
    for _ in range(120 if PART else 0):            # a lock file around it (a worker waits up to 60 s for the other)
        try:
            os.close(os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY))
            break
        except OSError:
            time.sleep(0.5)
    try:
        hist = []
        if os.path.isfile(COUNTS):
            with open(COUNTS, encoding="utf-8") as f:
                hist = json.load(f)
        prev = hist[-1]["counts"] if hist else {}
        rows = [u"%s %d%s" % (k, v, (u" (%+d)" % (v - prev[k])) if k in prev and prev[k] != v else u"")
                for k, v in sorted(c.items(), key=lambda kv: -kv[1])]
        mb = os.path.getsize(pln) / 1048576.0
        say(u"elements %d%s: %s" % (sum(c.values()), (u" (last: %d, %s)" % (sum(prev.values()), hist[-1]["file"]))
                                    if prev else u"", u", ".join(rows)))
        say(u"file %s: %.1f MB" % (os.path.basename(pln), mb))
        hist.append({"when": datetime.datetime.now().isoformat(timespec="seconds"), "label": label,
                     "file": os.path.basename(pln), "mb": round(mb, 1), "counts": c})
        with open(COUNTS, "w", encoding="utf-8") as f:
            json.dump(hist, f, indent=1)
    finally:
        try:
            if PART:
                os.remove(lock)
        except OSError:
            pass


def quit_archicad(url, own=False):
    """step 7: quit Archicad and wait until its process is gone (v9: url may be a list of urls, [] = only the wait;
    own = a worker's close: only until its own port stops answering, the other Archicad may still be building)"""
    for u in ([url] if isinstance(url, str) else url):
        try:
            tapir(u, "QuitArchicad", None, 120.0)
        except Exception:
            pass                                   # the connection may drop while Archicad quits
    t_end = time.time() + 60 * QUIT_WAIT_MIN
    while time.time() < t_end:
        time.sleep(3)                              # v9: was 10
        if (not alive(url, 2.0)) if own else (not archicad_running()):
            say(u"Archicad closed" if not own else u"Archicad at %s closed" % url)
            return
    raise RuntimeError(u"Archicad still running %d min after Quit (a dialog may be waiting)" % QUIT_WAIT_MIN)


def cold_move():
    """v4: AcBuild's caches and Archicad's cache folder into a backup folder (moved, never deleted)"""
    bk = os.path.join(AC_DIR, u"_coldrun_backup_%s" % time.strftime("%Y-%m-%d_%H%M"))
    src = [os.path.join(ROOT, "cached", "bergama_archicad_" + k) for k in ("site", "proposal", "context", "buildings")]
    src += glob.glob(os.path.join(os.environ.get("LOCALAPPDATA", u""), "Graphisoft", "Archicad Cache Folder*"))
    for x in src:
        if os.path.exists(x):
            os.makedirs(bk, exist_ok=True)
            shutil.move(x, os.path.join(bk, os.path.basename(x)))
            say(u"cold: moved %s -> %s" % (x, bk))
    return bk


def make_empty(src):
    """v6: Archicad opens src (never saved), File > New, Save As archicad/Bergama_empty_<date>_<time>.pln, quit"""
    emp = os.path.join(AC_DIR, u"Bergama_empty_%s.pln" % time.strftime("%Y-%m-%d_%H%M"))
    url = open_in_archicad(src)
    tapir(url, "NewProject", {"newAndReset": False}, 1800.0)
    tapir(url, "SaveProject", {"projectPath": emp, "overwrite": False}, 1800.0)
    info = {}
    try:
        info = tapir(url, "GetProjectInfo")
    except Exception:
        pass
    quit_archicad(url)
    if not os.path.isfile(emp):
        raise RuntimeError(u"the empty project was not saved as %s" % emp)
    say(u"empty project: %s (%.1f MB; Archicad now names it %s)" % (os.path.basename(emp), os.path.getsize(emp) / 1048576.0,
                                                                   info.get("projectName") or u"?"))
    return emp


def newest_part(part_):
    """v8: the newest built Bergama_AC_v*_<part>.pln (part_ = "_proposal" / "_context"), or None"""
    fs = glob.glob(os.path.join(AC_DIR, u"Bergama_AC_v*%s.pln" % part_))
    return max(fs, key=vkey) if fs else None


def build_one(acb, url, dst, port=None):
    """v4: AcBuild in the open project, saved, counted, Archicad quit (v9: port = a worker's own Archicad: AcBuild's
    progress and log files carry _<port>, and only that Archicad is closed)"""
    sfx = u"_%d" % port if port else u""           # v9: AcBuild v2.16 file names when BERGAMA_AC_PORT is set
    say(u"AcBuild %s running in %s (live steps: logs\\bergama_acbuild_progress%s.txt)" % (
        os.path.basename(acb), os.path.basename(dst), sfx))
    ns = runpy.run_path(acb, run_name="bergama_launcher")
    res = u"%s" % timed(u"build %s" % os.path.basename(dst), ns["_run"])
    try:
        ns["write_log"](res)
        lf = os.path.join(ROOT, "logs", u"bergama_acbuild_site_log%s.txt" % sfx)
        if os.path.isfile(lf):                     # v4: one log per file of the split
            shutil.copy2(lf, os.path.join(ROOT, "logs", u"bergama_acbuild_log_%s.txt" % os.path.basename(dst)[:-4]))
    except Exception:
        pass
    lines = [l for l in res.splitlines() if l.strip()]
    if res.startswith(u"ERROR"):
        raise RuntimeError(u"AcBuild stopped in %s: %s (Archicad left open; full log logs\\bergama_acbuild_site_log%s.txt)"
                           % (os.path.basename(dst), lines[0][:400], sfx))
    flags = [l for l in lines if l.startswith(u"FLAG")]
    say(u"AcBuild finished in %s: %s; %d FLAG lines" % (os.path.basename(dst), lines[-1][:300] if lines else u"", len(flags)))
    for l in flags[:10]:
        say(u"  " + l[:300])
    if not any(l.startswith(u"Archicad project saved (end of the run") for l in lines):   # AcBuild's last save
        tapir(url, "SaveProject", {}, 3600.0)
        say(u"project saved by build_next")
    timed(u"save %s" % os.path.basename(dst), save, url)
    count(url, dst, u"build")
    timed(u"close %s" % os.path.basename(dst), quit_archicad, url, bool(port))


def worker_json(port):
    return os.path.join(ROOT, "logs", u"bergama_build_next_worker_%d.json" % port)


def worker(args):
    """v9: _worker --acbuild <file> --port <port> --dst <pln>: one file of a parallel build, in the Archicad that has
    it open at that port: build_one (AcBuild, save, counts, file size, close of that Archicad only); exit code 0 or 1"""
    acb = os.path.join(SCRIPTS, args[args.index(u"--acbuild") + 1])   # a full path stays as it is
    port = int(args[args.index(u"--port") + 1])
    dst = args[args.index(u"--dst") + 1]
    m = re.search(r"_(proposal|context)\.pln$", dst, re.I)
    PART.append(m.group(1).lower() if m else u"master")
    MULTI.append(True)
    os.environ["BERGAMA_AC_PORT"] = u"%d" % port   # before runpy: AcBuild connects to this port only
    rc = 0
    try:
        build_one(acb, "http://127.0.0.1:%d" % port, dst, port)
    except Exception as ex:
        say(u"ERROR %s: %s" % (type(ex).__name__, ex))
        rc = 1
    try:
        with open(worker_json(port), "w", encoding="utf-8") as f:   # its timings, for the parent's speed json
            json.dump({"seconds": T, "archicad_gb_after": MEM}, f, indent=1)
    except Exception:
        pass
    sys.exit(rc)


def build_parallel(acb, d1, d2):
    """v9: --parallel: d1 (proposal) and d2 (context) each in its own Archicad, one _worker process per file. True
    when both are built and every Archicad is closed again; False (after a FLAG line, every Archicad closed) when the
    second Archicad does not come up or the two cannot be told apart: the caller then builds one after the other"""
    MULTI.append(True)
    url1 = timed(u"open %s" % os.path.basename(d1), open_in_archicad, d1)
    try:
        url2 = timed(u"open %s (second Archicad)" % os.path.basename(d2), open_in_archicad, d2, (url1,))
        if not has_project(url1, d1) or has_project(url1, d2) or has_project(url2, d1):
            raise RuntimeError(u"%s and %s do not each hold their own file" % (url1, url2))
    except Exception as ex:
        say(u"FLAG parallel build not possible (%s): closing Archicad, the files are built one after the other" % ex)
        quit_archicad(find_ac(every=True))
        del MULTI[:]
        return False
    t0 = time.time()
    jobs = []
    for url, d in ((url1, d1), (url2, d2)):
        port = int(url.rsplit(u":", 1)[1])
        if os.path.isfile(worker_json(port)):      # of an earlier run
            os.remove(worker_json(port))
        jobs.append((d, port, subprocess.Popen([sys.executable, os.path.abspath(__file__), u"_worker", u"--acbuild", acb,
                                                u"--port", u"%d" % port, u"--dst", d])))
        say(u"worker started: %s at %s (lines [%s]; live steps: logs\\bergama_acbuild_progress_%d.txt)" % (
            os.path.basename(d), url, u"proposal" if d == d1 else u"context", port))
    bad = [(d, port, rc) for d, port, rc in [(d, port, p.wait()) for d, port, p in jobs] if rc != 0]
    T[u"parallel build proposal + context"] = round(time.time() - t0, 1)
    say(u"TIME parallel build proposal + context: %.0f s" % T[u"parallel build proposal + context"])
    for d, port, p in jobs:                        # the workers' own timings (build, save, close per file)
        try:
            with open(worker_json(port), encoding="utf-8") as f:
                w = json.load(f)
            T.update(w["seconds"])
            MEM.update(w["archicad_gb_after"])
        except Exception:
            pass
    if bad:
        raise RuntimeError(u"AcBuild stopped in %s: see its ERROR line above (Archicad left open; full log "
                           u"logs\\bergama_acbuild_site_log_%d.txt)" % (os.path.basename(bad[0][0]), bad[0][1]))
    quit_archicad([])                              # both workers closed their own: until no Archicad process is left
    del MULTI[:]
    return True


def build():
    try:
        acb = fetch_newest()
    except Exception as ex:                        # no internet: the newest copy already on this PC
        if PIN and u"not on GitHub main" in u"%s" % ex:
            raise
        acb = max(glob.glob(os.path.join(SCRIPTS, "bergama_acbuild_v*.py")), key=vkey)
        say(u"FLAG GitHub not reached (%s): using %s already on this PC" % (ex, os.path.basename(acb)))
    if archicad_running() or find_ac():
        raise RuntimeError(u"Archicad is already running on this PC: save and close it first")
    move_leftovers()
    src = os.path.join(AC_DIR, FROM[0]) if FROM else newest_pln()
    if not os.path.isfile(src):
        raise RuntimeError(u"source %s not found in %s" % (FROM[0], AC_DIR))
    ver = re.search(r"v(\d+)_(\d+)([a-z]*)", os.path.basename(acb))
    dst = os.path.join(AC_DIR, u"Bergama_AC_v%s.%s%s.pln" % ver.groups())
    with open(acb, encoding="utf-8") as f:
        txt = f.read()
    split = re.search(r"^SPLIT_FILES = True", txt, re.M) is not None   # v4
    dsts = ([dst[:-4] + u"_proposal.pln", dst[:-4] + u"_context.pln"] if split else []) + [dst]
    if ONLY and split:                             # v8: only the named parts
        dsts = [d for d in dsts if (u"proposal" in ONLY and d.endswith(u"_proposal.pln"))
                or (u"context" in ONLY and d.endswith(u"_context.pln")) or (u"master" in ONLY and d == dst)]
        if not dsts:
            raise RuntimeError(u"--only %s names no part (proposal, context, master)" % u",".join(ONLY))
    for d in dsts:
        if os.path.exists(d):
            raise RuntimeError(u"%s already exists: this version was built before (rename or move it to rebuild)"
                               % os.path.basename(d))
    if COLD:
        timed(u"cold: caches moved", cold_move)
    if EMPTY:                                      # v6: start from a new, empty project
        src = timed(u"empty project made", make_empty, src)
    for d in dsts:
        s_ = src                                   # v7 (Aras 25 Nov 10:16 UTC "you dont need to build from empty every
        if split and not EMPTY:                    # time"): each part from the same part of the source build (its
            for part_ in (u"_proposal", u"_context"):   # _proposal / _context next to it), the master from the master
                if d.endswith(part_ + u".pln") and os.path.isfile(src[:-4] + part_ + u".pln"):
                    s_ = src[:-4] + part_ + u".pln"
                if ONLY and d.endswith(part_ + u".pln") and newest_part(part_):   # v8: the newest built file of
                    s_ = newest_part(part_)                                       # that part (a test build has no master)
        timed(u"copy source -> %s" % os.path.basename(d), shutil.copy2, s_, d)
        if os.path.getsize(d) != os.path.getsize(s_):
            raise RuntimeError(u"copy of %s incomplete" % os.path.basename(s_))
        say(u"copied %s -> %s" % (os.path.basename(s_), os.path.basename(d)))
    par = []                                       # v9: the files built by the parallel path
    if PARALLEL:
        pp = [d for d in dsts if d.endswith((u"_proposal.pln", u"_context.pln"))]
        if len(pp) != 2:
            say(u"FLAG --parallel needs the proposal and the context file in this run: built one after the other")
        elif u"BERGAMA_AC_PORT" not in txt:        # an older AcBuild would build both parts into the first Archicad
            say(u"FLAG --parallel needs an AcBuild that reads BERGAMA_AC_PORT (v2.16 on), %s does not: built one "
                u"after the other" % os.path.basename(acb))
        elif build_parallel(acb, pp[0], pp[1]):
            par = pp
    for d in dsts:                                 # v4: proposal, context, then the master (it hotlinks them)
        if d in par:
            continue
        url = timed(u"open %s" % os.path.basename(d), open_in_archicad, d)
        build_one(acb, url, d)
    say(u"BUILT %s (all files built and saved; reopen + 3D test next)" % u", ".join(os.path.basename(d) for d in dsts))
    write_speed(u"build (before the reopen)", T0[0])   # v5
    if dst not in dsts:                            # v8: a part-only test build: no master, no reopen test
        return dsts[-1]
    url = timed(u"reopen built file", open_in_archicad, dst)
    timed(u"open 3D window (fresh start)", open_3d, url)
    timed(u"save (after reopen)", save, url)
    timed(u"close after 3D", quit_archicad, url)
    return dst


def check():
    if archicad_running() or find_ac():
        raise RuntimeError(u"Archicad is already running on this PC: save and close it first")
    move_leftovers()
    pln = newest_pln()
    t0 = time.time()
    url = open_in_archicad(pln)
    say(u"reopen took %.0f s" % (time.time() - t0))
    count(url, pln, u"check")
    quit_archicad(url)
    return pln


T0 = [time.time()]                                 # v5: run start (for the timings written before the reopen)


def main():
    os.makedirs(os.path.dirname(STATUS), exist_ok=True)
    args = sys.argv[1:]
    if args and args[0] == u"_worker":             # v9: one file of a parallel build (the status file is not restarted)
        worker(args)
    if u"--parallel" in args:                      # v9
        PARALLEL.append(True)
    if u"--from" in args:
        FROM.append(args[args.index(u"--from") + 1])
    if u"--acbuild" in args:
        PIN.append(args[args.index(u"--acbuild") + 1])
    if u"--cold" in args:
        COLD.append(True)
    if u"--empty" in args:
        EMPTY.append(True)
    if u"--only" in args:                          # v8
        ONLY.extend(x.strip().lower() for x in args[args.index(u"--only") + 1].split(u",") if x.strip())
    mode = (args[0] if args and not args[0].startswith(u"--") else u"build").lower()
    with open(STATUS, "w", encoding="utf-8") as f:
        f.write(u"%s  build_next v9 started (%s%s)\n" % (time.strftime("%H:%M:%S"), mode, (u", cold" if COLD else u"") + (u", empty" if EMPTY else u"") + (u", only " + u",".join(ONLY) if ONLY else u"") + (u", parallel" if PARALLEL else u"")))
    t0 = time.time()
    T0[0] = t0
    try:
        pln = check() if mode == u"check" else build()
        say(u"DONE %s: %s in %.0f min" % (mode, os.path.basename(pln), (time.time() - t0) / 60.0))
    except Exception as ex:
        say(u"ERROR %s: %s" % (type(ex).__name__, ex))
        write_speed(mode, t0)
        sys.exit(1)
    write_speed(mode, t0)


def write_speed(mode, t0):
    """v2: the timings of this run, one file per PC and run"""
    try:
        import ctypes
        class MS(ctypes.Structure):
            _fields_ = [("l", ctypes.c_ulong), ("p", ctypes.c_ulong), ("tot", ctypes.c_ulonglong),
                        ("av", ctypes.c_ulonglong)] + [("x%d" % i, ctypes.c_ulonglong) for i in range(5)]
        m = MS()
        m.l = ctypes.sizeof(MS)
        ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
        ram = round(m.tot / 1073741824.0, 1)
    except Exception:
        ram = None
    pc = os.environ.get("COMPUTERNAME", u"PC")
    d = dict(pc=pc, ram_gb=ram, mode=mode, source=FROM[0] if FROM else u"newest", when=time.strftime("%Y-%m-%d %H:%M"),
             total_s=round(time.time() - t0, 1), seconds=T, archicad_gb_after=MEM)
    f = os.path.join(ROOT, "cached", "bergama_archicad_site", "speed_%s_%s.json" % (pc, time.strftime("%Y%m%d_%H%M")))
    os.makedirs(os.path.dirname(f), exist_ok=True)
    with open(f, "w", encoding="utf-8") as fh:
        json.dump(d, fh, indent=1)
    say(u"timings saved: %s" % f)


if __name__ == "__main__":
    main()
